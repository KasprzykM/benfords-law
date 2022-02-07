import csv
import logging
from enum import Enum
from typing import Any, Optional

import numpy as np
from benfordslaw import benfordslaw
from django.core.exceptions import ValidationError
from django.core.files import File
from matplotlib import pyplot
from numpy.core.multiarray import ndarray

logger = logging.getLogger(__name__)


class BenfordsLawService:
    @staticmethod
    def get_plot(data: ndarray) -> pyplot:
        pyplot.clf()
        bl = benfordslaw(method="ks")
        bl.fit(data)
        return bl.plot(title="Benfords law leading digits")


class FileType(str, Enum):
    CSV_FILE = "csv_file"


class UploadService:
    MIMES_MAPPING = {
        "text/plain": FileType.CSV_FILE,
        "text/csv": FileType.CSV_FILE,
    }

    @classmethod
    def parse(
        cls,
        data_file: File,
        mime_type: str,
        with_header: bool,
        column_name: Optional[str] = None,
        column_index: Optional[int] = None,
    ) -> Any:

        file_type = cls.MIMES_MAPPING[mime_type]
        data_file.file.seek(0)
        if file_type == FileType.CSV_FILE:
            data = cls.parse_csv(data_file, with_header, column_name, column_index)
        else:
            raise ValueError(
                f"Incorrect file supplied, it's {mime_type=} not supported."
            )
        return data

    @staticmethod
    def parse_csv(
        data_file: File,
        with_header: bool,
        column_name: Optional[str] = None,
        column_index: Optional[int] = None,
    ) -> ndarray:
        decoded = data_file.file.read().decode("utf-8", errors="ignore")
        lines = decoded.split("\n")

        dialect = csv.Sniffer().sniff(lines[0])
        expected_col_number = len(lines[0].split(dialect.delimiter))
        reader = csv.reader(
            lines,
            dialect,
        )

        # Take the first column_name if header and column_name name are not specified.
        index = 0
        if with_header:
            header = next(reader)
            if column_name and column_name not in header:
                raise ValidationError(f"Column_name name not found in header")
            elif column_name:
                index = header.index(column_name)

        if column_index:
            if not column_index <= expected_col_number - 1:
                raise ValidationError(f"Column index higher than number of columns")
            index = column_index

        data = []
        for row in reader:
            cols = len(row)
            if cols != expected_col_number or index >= cols or not row[index]:
                logger.warning(f"Skipping row, incorrect index or number of rows.")
                continue
            try:
                data.append(float(row[index]))
            except ValueError:
                raise ValidationError(
                    f"Not a number in given data row: `%(value)s`",
                    params={"value": row[index]},
                    code="row",
                )

        return np.array(data)
