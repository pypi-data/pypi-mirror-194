# =============================================================================
# Casanova Utils
# =============================================================================
#
# Miscellaneous utility functions.
#
import re
import csv
import gzip
from io import StringIO, DEFAULT_BUFFER_SIZE
from platform import python_version_tuple
from file_read_backwards.file_read_backwards import FileReadBackwardsIterator
from collections.abc import Mapping

from casanova.exceptions import Py310NullByteWriteError, LtPy311ByteReadError

PY_310 = python_version_tuple()[:2] == ("3", "10")
LT_PY311 = python_version_tuple()[:2] <= ("3", "10")


def py310_wrap_csv_writerow(writer):
    if not PY_310:
        return writer.writerow

    def wrapped(*args, **kwargs):
        try:
            writer.writerow(*args, **kwargs)
        except csv.Error as e:
            if str(e).lower() == "need to escape, but no escapechar set":
                raise Py310NullByteWriteError(
                    "Cannot write row containing null byte. This error only happens on python 3.10 (see https://github.com/python/cpython/issues/56387). Consider using the strip_null_bytes_on_write=True kwarg or change python version."
                )

            raise

    return wrapped


def ltpy311_csv_reader(input_file, **kwargs):
    reader = csv.reader(input_file, **kwargs)

    if not LT_PY311:
        return reader

    def wrapped():
        try:
            for item in reader:
                yield item
        except csv.Error as e:
            if "line contains nul" in str(e).lower():
                raise LtPy311ByteReadError(
                    "python < 3.11 cannot read CSV files containing null bytes. Consider using the strip_null_bytes_on_read=True kwarg or upgrade your python version."
                )

            raise

    return wrapped()


def ensure_open(p, encoding="utf-8", mode="r"):
    if not isinstance(p, str):
        return p

    if p.endswith(".gz"):
        if "b" in mode:
            return gzip.open(p, mode=mode)

        mode += "t"
        return gzip.open(p, encoding=encoding, mode=mode)

    if "b" in mode:
        return open(p, mode=mode)

    return open(p, encoding=encoding, mode=mode)


BOM_RE = re.compile(r"^\ufeff")


def suppress_BOM(string):
    return re.sub(BOM_RE, "", string)


def has_null_byte(string):
    return "\0" in string


def strip_null_bytes(string):
    return string.replace("\0", "")


def lines_without_null_bytes(iterable):
    for line in iterable:
        yield strip_null_bytes(line)


def first_cell_index_with_null_byte(row):
    for i, cell in enumerate(row):
        if has_null_byte(cell):
            return i

    return None


def strip_null_bytes_from_row(row):
    if any(has_null_byte(cell) for cell in row if isinstance(cell, str)):
        return [strip_null_bytes(cell) for cell in row]

    return row


def rows_without_null_bytes(iterable):
    for row in iterable:
        yield strip_null_bytes_from_row(row)


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def size_of_row_in_memory(row):
    """
    Returns the approximate amount of bytes needed to represent the given row into
    the python's program memory.

    The magic numbers are based on `sys.getsizeof`.
    """
    a = 64 + 8 * len(row)  # Size of the array
    a += sum(49 + len(cell) for cell in row)  # Size of the contained strings

    return a


def size_of_row_in_file(row):
    """
    Returns the approximate amount of bytes originally used to represent the
    given row in its CSV file. It assumes the delimiter uses only one byte.

    I also ignores quotes (-2 bytes) around escaped cells if they were
    originally present.

    I also don't think that it counts 16 bit chars correctly.
    """
    a = max(0, len(row) - 1)
    a += sum(len(cell) for cell in row)

    return a


class CsvIOBase(StringIO):
    def __init__(self):
        super().__init__()
        self.writer = csv.writer(
            self, dialect=csv.unix_dialect, quoting=csv.QUOTE_MINIMAL
        )


class CsvCellIO(CsvIOBase):
    def __init__(self, value, column=None):
        super().__init__()

        if column is not None:
            self.fieldnames = [column]
            self.writer.writerow(self.fieldnames)

        self.writer.writerow([value])

        self.seek(0)


class CsvRowIO(CsvIOBase):
    def __init__(self, row, fieldnames=None):
        super().__init__()

        self.fieldnames = fieldnames

        if isinstance(row, Mapping):
            if self.fieldnames is None:
                self.fieldnames = list(row.keys())

            row = [row.get(f) for f in self.fieldnames]

        if self.fieldnames is not None:
            self.writer.writerow(self.fieldnames)

        self.writer.writerow(row)

        self.seek(0)


class CsvIO(CsvIOBase):
    def __init__(self, rows, fieldnames=None):
        super().__init__()

        self.fieldnames = fieldnames

        if fieldnames is not None:
            self.writer.writerow(fieldnames)

        for row in rows:
            self.writer.writerow(row)

        self.seek(0)


def create_csv_aware_backwards_lines_iterator(
    input_file, quotechar=None, strip_null_bytes_on_read=False
):
    encoding = input_file.encoding if hasattr(input_file, "encoding") else "utf-8"
    quotechar = quotechar if quotechar is not None else '"'

    backwards_file = ensure_open(input_file.name, mode="rb")

    backwards_iterator = FileReadBackwardsIterator(
        backwards_file, encoding, DEFAULT_BUFFER_SIZE
    )

    def correctly_escaped_backwards_iterator():
        acc = None

        for line in backwards_iterator:
            if strip_null_bytes_on_read:
                line = strip_null_bytes(line)

            if acc is not None:
                acc = line + "\n" + acc
            else:
                acc = line

            if acc.count(quotechar) % 2 == 0:
                yield acc
                acc = None

        if acc is not None:
            yield acc

    return backwards_file, correctly_escaped_backwards_iterator()
