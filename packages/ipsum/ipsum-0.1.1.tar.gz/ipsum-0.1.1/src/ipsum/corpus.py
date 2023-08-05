import re
from typing import Generator
from zipfile import ZipFile


class Corpus:
    """Used to iterate over text files in a zip archive that match a pattern."""

    def __init__(
        self,
        path: str,
        valid_filename_regex: str = r".*\.txt",
        encoding: str = "utf-8",
    ) -> None:
        """Initialize a new corpus.

        Args:
            path: A string path to a zip file.
            valid_filename_regex: A regex pattern. Corpus iterates over files
                whose names fully match the pattern.
            encoding: The encoding with which to decode the matching files.
        """
        self._archive = ZipFile(path, "r")
        self._encoding = encoding
        self._filename_validator = re.compile(valid_filename_regex)
        self._txt_filenames = [
            name
            for name in self._archive.namelist()
            if self._filename_validator.fullmatch(name)
        ]

    def __iter__(self) -> Generator[str, None, None]:
        """Iterate over files (returning content) in archive that match pattern."""
        for name in self._txt_filenames:
            content = self._archive.read(name).decode(self._encoding)
            yield content
