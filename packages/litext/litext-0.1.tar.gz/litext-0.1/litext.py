from __future__ import annotations
import json

import logging
import re
import textwrap
import inspect
import sys
from enum import Enum
from typing import Callable, List, Optional, Tuple, Union

import sqlite_spellfix

try:
    import pysqlite3 as sqlite3
    import pysqlite3.dbapi2

    OperationalError = pysqlite3.dbapi2.OperationalError
except ImportError:
    logging.info("Using default sqlite3 module")
    import sqlite3  # noqa

    OperationalError = sqlite3.OperationalError


from contextlib import contextmanager

# sqlite_utils is Licensed under Apache 2.0
# license available at:
# https://github.com/simonw/sqlite-utils/blob/main/LICENSE
# https://github.com/simonw/sqlite-utils/blob/54191d4dc114d7dc21e849b48a4d5ae4f9e601ca/LICENSE
from sqlite_utils.db import Database as xDatabase
from sqlite_utils.db import View
from sqlite_utils.db import validate_column_names
from sqlite_utils.db import Table as xTable

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    # level=logging.INFO,
)

__version__ = "0.1"

__all__ = ("Database", "Table")


# SQLite works better in autocommit mode when using short DML (INSERT / UPDATE / DELETE) statements
# source: https://charlesleifer.com/blog/going-fast-with-sqlite-and-python/
@contextmanager
def transaction(conn: sqlite3.Connection):
    # We must issue a "BEGIN" explicitly when running in auto-commit mode.
    conn.execute("BEGIN")
    try:
        # Yield control back to the caller.
        yield conn
    except BaseException as e:
        logging.error(f"Query failed: {repr(e)}")
        conn.rollback()  # Roll back all changes if an exception occurs.
        raise
    else:
        conn.commit()


def get_sqlite_version() -> Tuple[int, int, int]:
    sqlite_ver = sqlite3.sqlite_version.split(".")

    v_major = int(sqlite_ver[0])
    v_min = int(sqlite_ver[1])
    v_bug = int(sqlite_ver[2])

    assert v_major == 3

    return (v_major, v_min, v_bug)


class UnsupportedSQLiteVersion(Exception):
    pass


class Database(xDatabase):

    conn: sqlite3.Connection

    def __init__(
        self,
        filename_or_conn=None,
        memory=False,
        recreate=False,
        recursive_triggers=True,
        tracer=None,
        use_counts_table=False,
    ):

        if get_sqlite_version() < (3, 34, 0):
            raise UnsupportedSQLiteVersion(
                f"Usupported SQLite version, you're using version {sqlite3.sqlite_version}. At least version 3.34.0 is needed"
            )

        super().__init__(
            filename_or_conn=filename_or_conn,
            memory=memory,
            recreate=recreate,
            recursive_triggers=recursive_triggers,
            tracer=tracer,
            use_counts_table=use_counts_table,
        )

    def __getitem__(self, table_name: str):
        return self.table(table_name)

    def table(self, table_name, **kwargs) -> Union[View, Table]:
        klass = View if table_name in self.view_names() else Table
        return klass(self, table_name, **kwargs)

    def vacuum(self: "Database"):
        self.conn.execute("VACUUM;")

    def close(self: "Database"):
        self.conn.close()

    def fast_pragmas(self: "Database"):
        self.conn.execute("PRAGMA journal_mode = 'WAL';")
        self.conn.execute("PRAGMA temp_store = 2;")
        self.conn.execute("PRAGMA synchronous = 1;")
        self.conn.execute(f"PRAGMA cache_size = {-1 * 64_000};")
        return True

    def _load_spellfix(self: "Database"):
        self.conn.enable_load_extension(True)
        spellfix_path = sqlite_spellfix.extension_path()
        assert spellfix_path, "There was an error finding the spellfix path"
        self.conn.load_extension(spellfix_path)
        self.conn.enable_load_extension(False)
        return True

    def to_memory(self: "Database"):
        """
        Copy database to memory.

        This closes the current connection and substitutes
        it with another in-memory one.
        """

        def progress(status, remaining, total):
            logging.info(f"Copied {total-remaining} of {total} pages...")

        dest = Database(":memory:")
        self.conn.backup(dest.conn, progress=progress)
        self.close()
        self.conn = dest.conn
        return self

    def to_disk(self: "Database", new_db_or_conn):
        """
        Copy database to disk.

        This closes the current connection and substitutes
        it with another in-memory one.
        """

        def progress(status, remaining, total):
            logging.info(f"Copied {total-remaining} of {total} pages...")

        dest = Database(new_db_or_conn)
        self.conn.backup(dest.conn, progress=progress)
        self.conn = dest.conn
        return self

    def register_function(
        self: "Database",
        fn: Optional[Callable] = None,
        arity: Optional[int] = None,
        deterministic: Optional[bool] = None,
        replace: Optional[bool] = False,
    ):
        def register(fn):
            name = fn.__name__

            nonlocal arity

            if not arity:
                arity = len(inspect.signature(fn).parameters)

            if not replace and (name, arity) in self._registered_functions:
                return fn
            kwargs = {}
            if deterministic and sys.version_info >= (3, 8):
                kwargs["deterministic"] = True
            self.conn.create_function(name, arity, fn, **kwargs)
            self._registered_functions.add((name, arity))
            return fn

        if fn is None:
            return register
        else:
            register(fn)


def re_tokenize(s, re_splitter=re.compile(r"\W+")):

    return json.dumps(re_splitter.split(s))


def re_tokenize2(s):

    re_splitter = re.compile(r"\W+")

    return json.dumps(re_splitter.split(s))


class FTS5VocabEnum(str, Enum):
    row = "row"
    col = "col"
    instance = "instance"


class FTSQueryError(Exception):
    pass


class SearchFilters:

    __slots__ = ("clause", "args")

    def __init__(self, clause: str, query_args: dict):
        """

        Example:
        s = SearchFilters("where :column > 2", {"column": "foobar"})
        """

        if "?" in clause:
            raise FTSQueryError(
                f"Where clause needs to use the ':' syntax. For example: {clause.replace('?', ':someval')}"
            )

        for parameter, _value in query_args.items():

            if parameter not in clause:
                raise FTSQueryError(
                    f"The parameter '{parameter}' in the query arguments is not in the query clause."
                )

        clause_parameters = re.finditer(r":(\w+)\s", clause)

        if clause_parameters:
            for match in clause_parameters:
                parameter = match.group(1)
                if parameter not in query_args:
                    raise FTSQueryError(
                        f"The parameter '{parameter}' in the clause is not in the query arguments."
                    )

        self.clause = clause
        self.args = query_args


class FTSSearchOperator(str, Enum):
    like = "like"
    glob = "glob"
    match = "match"


class FTSTokenizers(str, Enum):
    unicode = "unicode"
    trigram = "trigram"


class Table(xTable):

    db: Database

    def enable_fts5(
        self: "Table",
        columns,
        tokenizer: FTSTokenizers = FTSTokenizers.unicode,
        replace=False,
    ) -> "Table":
        "Enables FTS on the specified columns."

        validate_column_names(columns)

        try:
            tokenizer = FTSTokenizers[tokenizer]
        except KeyError as e:
            logging.error(
                f"Tokenizer must be one of: {[x.name for x in FTSTokenizers]}"
            )
            raise e

        if tokenizer == FTSTokenizers.unicode:
            # remove_diacritics 2 -> old bug in SQLite, the default is 1 to keep
            # backwards compatibility (for SQLite)
            tokenize_clause = "unicode61 remove_diacritics 2"
        else:
            tokenize_clause = "trigram case_sensitive 0"

        create_triggers = True

        create_fts_sql = """
CREATE VIRTUAL TABLE [{table}_fts] USING FTS5 (
    {columns},{tokenize}
    content=[{table}]
)
        """.format(
            table=self.name,
            columns=", ".join("[{}]".format(c) for c in columns),
            tokenize="\n    tokenize='{}',".format(tokenize_clause)
            if tokenize_clause
            else "",
        )

        should_recreate = False

        if replace and self.db["{}_fts".format(self.name)].exists():

            # Does the table need to be recreated?
            fts_schema = self.db["{}_fts".format(self.name)].schema

            if fts_schema != create_fts_sql:
                should_recreate = True

            expected_triggers = {self.name + suffix for suffix in ("_ai", "_ad", "_au")}
            existing_triggers = {t.name for t in self.triggers}
            has_triggers = existing_triggers.issuperset(expected_triggers)

            if has_triggers != create_triggers:
                should_recreate = True

            if not should_recreate:
                # Table with correct configuration already exists
                return self

        if should_recreate:
            self.disable_fts()

        self.db.executescript(create_fts_sql)
        self.populate_fts(columns)

        if create_triggers:
            old_cols = ", ".join("old.[{}]".format(c) for c in columns)
            new_cols = ", ".join("new.[{}]".format(c) for c in columns)
            triggers = """
CREATE TRIGGER [{table}_ai] AFTER INSERT ON [{table}] BEGIN
  INSERT INTO [{table}_fts] (rowid, {columns}) VALUES (new.rowid, {new_cols});
END;
CREATE TRIGGER [{table}_ad] AFTER DELETE ON [{table}] BEGIN
  INSERT INTO [{table}_fts] ([{table}_fts], rowid, {columns}) VALUES('delete', old.rowid, {old_cols});
END;
CREATE TRIGGER [{table}_au] AFTER UPDATE ON [{table}] BEGIN
  INSERT INTO [{table}_fts] ([{table}_fts], rowid, {columns}) VALUES('delete', old.rowid, {old_cols});
  INSERT INTO [{table}_fts] (rowid, {columns}) VALUES (new.rowid, {new_cols});
END;
            """.format(
                table=self.name,
                columns=", ".join("[{}]".format(c) for c in columns),
                old_cols=old_cols,
                new_cols=new_cols,
            )
            self.db.executescript(triggers)
        return self

    def _enable_fts5_vocab(self: "Table", vocab: FTS5VocabEnum) -> "Table":

        create_fts_vocab = textwrap.dedent(
            """
CREATE VIRTUAL TABLE IF NOT EXISTS [{table}_fts_vocab_{vocab_type}]
USING fts5vocab({fts_table}, {vocab_type})
        """
        ).format(
            table=self.name,
            fts_table=f"{self.name}_fts",
            vocab_type=vocab,
        )

        self.db.executescript(create_fts_vocab)

        return self

    def enable_spellfix(self: "Table", columns: List[str]):

        validate_column_names(columns)

        # TODO: check spellfix1 has been loaded?
        # Mayebe I should create a "metadata" table
        # to store some lightsearch-specific metadata?
        self.db._load_spellfix()

        self.db.register_function(
            re_tokenize, arity=1, deterministic=True, replace=False
        )

        create_fts_spellfix = f"CREATE VIRTUAL TABLE IF NOT EXISTS [{self.name}_fts_spellfix1data] USING spellfix1"

        self.db.executescript(create_fts_spellfix)

        logging.info(f"Table {self.name}_fts_spellfix1data created")
        logging.info("Populating spellfix table")

        self._populate_spellfix_vocabulary(columns=columns)

        logging.info("Spellfix data loaded")

        return self

    def _populate_spellfix_vocabulary(self: "Table", columns: List[str]):

        # check spellfix is enabled
        if f"{self.name}_fts_spellfix1data" not in {x.name for x in self.db.tables}:
            raise Exception(
                f"""
    spellfix1 table '{self.name}_fts_spellfix1data' not found in DB.
    Try using '{self.name}.enable_spellfix()'
    """.strip()
            )

        create_fts_spellfix = f"""
WITH texts AS (
    SELECT re_tokenize({" || ' ' || ".join("[{}]".format(c) for c in columns)}) as concat_text
    FROM docs
),

tokens AS (
    SELECT DISTINCT value
      FROM texts, json_each(texts.concat_text)
)

INSERT INTO [{self.name}_fts_spellfix1data](word)

        SELECT value FROM tokens
        WHERE value not in (
                            SELECT word from [{self.name}_fts_spellfix1data_vocab]
                            )
            """

        self.db.executescript(create_fts_spellfix)

        return self

    def find_close_words(
        self: "Table",
        word: str,
        edit_distance: int = 300,
        max_results: int = 20,
        filter_same: bool = True,
    ):

        if filter_same:
            same_word_filter = "AND word != :w"
        else:
            same_word_filter = ""

        cursor = self.db.execute(
            f"""
SELECT word FROM docs_fts_spellfix1data
WHERE editdist3(word, :w) <= :editdist
{same_word_filter}
ORDER BY editdist3(word, :w)
LIMIT :max_results
""",
            {"w": word, "editdist": edit_distance, "max_results": max_results},
        )

        for row in cursor:
            yield row[0]

    def _search_sql(
        self: "Table",
        search_operator: str,
        columns: Optional[List[str]] = None,
        matching_column: Optional[str] = None,
        filters_clause: Optional[str] = None,
        order_by: Optional[str] = None,
        order_by_extra: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        return_rank_score: bool = False,
    ):

        search_operator = search_operator.lower()

        if search_operator not in {"glob", "like", "match"}:
            raise FTSQueryError(
                f"Search operator must be one of: 'like', 'glob' or 'match'. Value passed was: '{search_operator}'"
            )

        if search_operator in {"glob", "like"} and not matching_column:
            raise FTSQueryError(
                "'glob' and 'like' queries must use a column to filter using `matching_column`"
            )

        if not filters_clause:

            filters_clause = ""

        # Pick names for table and rank column that don't clash
        original = "original_" if self.name == "original" else "original"

        if columns:
            columns_sql = ",\n        ".join("[{}]".format(c) for c in columns)
            columns_with_prefix_sql = ",\n    ".join(
                "[{}].[{}]".format(original, c) for c in columns
            )

        else:
            columns_sql = "*"
            columns_with_prefix_sql = "[{}].*".format(original)

        fts_table = self.detect_fts()
        assert fts_table, "Full-text search is not configured for table '{}'".format(
            self.name
        )

        if return_rank_score:

            columns_with_prefix_sql += f",\n [{fts_table}].rank"

        matching = "[{fts_table}]".format(fts_table=fts_table)

        if matching_column:

            assert (
                '"' not in matching_column
            ), "Matching column can't include the '\"' symbol"

            matching += f'."{matching_column}"'

        # virtual_table_using = self.db[fts_table].virtual_table_using

        sql = """
with {original} as (
    select
        rowid,
        {columns}
    from [{dbtable}]
    {filters_clause}
)
select
    {columns_with_prefix}
from
    [{original}]
    join [{fts_table}] on [{original}].rowid = [{fts_table}].rowid
where
    {matching} {search_operator} :query
order by
    {order_by}
{limit_offset}
        """

        rank_implementation = "[{}].rank".format(fts_table)

        if order_by_extra:
            rank_implementation += f" {order_by_extra}"

        limit_offset = ""
        if limit is not None:
            limit_offset += " limit {}".format(int(limit))

        if offset is not None:
            limit_offset += " offset {}".format(int(offset))

        final_query = sql.format(
            dbtable=self.name,
            original=original,
            filters_clause=filters_clause,
            columns=columns_sql,
            columns_with_prefix=columns_with_prefix_sql,
            fts_table=fts_table,
            matching=matching,
            search_operator=search_operator,
            order_by=order_by or rank_implementation,
            limit_offset=limit_offset.strip(),
        ).strip()

        logging.debug(final_query)

        return final_query

    def search(
        self: "Table",
        q,
        search_operator: Union[str, FTSSearchOperator] = FTSSearchOperator.match,
        columns: Optional[List[str]] = None,
        matching_column: Optional[str] = None,
        filters: Optional[SearchFilters] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        return_rank_score: bool = False,
    ):
        """Execute full-text search query

        Args:
            self (Table): [description]
            q (str): FTS query string
            search_operator (Union[str, FTSSearchOperator], optional): FTS operator to use in the query. Defaults to FTSSearchOperator.match.
            columns (Optional[List[str]], optional): Columns to retrieve from the rows matching the FTS query. Defaults to None.
            matching_column (Optional[str], optional): Column to use for matching. Must be used when the match operator is "glob" or "like". Defaults to None.
            filters (Optional[SearchFilters], optional): Extra filters to apply to columns. Defaults to None.
            order_by (Optional[str], optional): Results ordering. Defaults to None.
            limit (Optional[int], optional): Number of results to retrieve. Defaults to None.
            offset (Optional[int], optional): Offset. Defaults to None.

        Yields:
            dict: Dictionaries mapping column -> value off all the matching rows
        """

        if columns:
            validate_column_names(columns)

        query_params = {"query": q}

        if filters:
            query_params.update(**filters.args)

        cursor = self.db.execute(
            self._search_sql(
                search_operator=search_operator,
                columns=columns,
                matching_column=matching_column,
                filters_clause=filters.clause if filters else None,
                order_by=order_by,
                limit=limit,
                offset=offset,
                return_rank_score=return_rank_score,
            ),
            query_params,
        )
        columns = [c[0] for c in cursor.description]
        for row in cursor:
            yield dict(zip(columns, row))

    @classmethod
    def prefix(cls, query: str):
        return f'"{query}" *'
