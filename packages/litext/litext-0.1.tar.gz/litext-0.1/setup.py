import setuptools
from pathlib import Path
import re


def get_version(fn) -> str:
    code = Path(fn).read_text()
    match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", code)
    assert match is not None
    return match.group(1)


version = get_version("./litext.py")

setuptools.setup(
    name="litext",
    version=version,
    author="Ricardo Ander-Egg Aguilar",
    author_email="rsubacc@gmail.com",
    description="Simple search engine built on top of SQLite",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/litements/litext",
    py_modules=["litext"],
    classifiers=[
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["sqlite-spellfix", "sqlite-utils"],
)
