from benfordslaw import benfordslaw
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.files.base import File

from codepoets.service import UploadService

FLOATING_ERROR = 0.00001


class BenfordTestCase(TestCase):
    def setUp(self) -> None:
        self.sample_file = File(open("codepoets/tests/sample/census_2009b.dms", "rb"))
        self.bl = benfordslaw(method="ks")
        self.expected_percent_values = [
            29.40573,
            18.15105,
            12.00328,
            9.47034,
            7.99364,
            7.02456,
            5.97857,
            5.34277,
            4.63006,
        ]

    def tearDown(self) -> None:
        self.sample_file.close()

    def test_correct_census_file_column_name(self) -> None:
        data = UploadService.parse(
            self.sample_file,
            mime_type="text/csv",
            column_name="7_2009",
            with_header=True,
        )
        res = self.bl.fit(data)
        percentages = res["percentage_emp"]
        for i, value in enumerate(self.expected_percent_values):
            self.assertTrue(abs(value - percentages[i][1]) <= FLOATING_ERROR)

    def test_correct_census_file_column_index(self) -> None:
        data = UploadService.parse(
            self.sample_file,
            mime_type="text/csv",
            column_index=2,
            with_header=True,
        )
        res = self.bl.fit(data)
        percentages = res["percentage_emp"]
        for i, value in enumerate(self.expected_percent_values):
            self.assertTrue(abs(value - percentages[i][1]) <= FLOATING_ERROR)
        self.assertTrue(True)

    def test_incorrect_header(self) -> None:
        with self.assertRaisesMessage(
            ValidationError, "Not a number in given data row: `State`"
        ):
            _ = UploadService.parse(
                self.sample_file,
                mime_type="text/csv",
                column_name="7_2009",
                with_header=False,
            )

    def test_incorrect_mime(self) -> None:
        with self.assertRaisesMessage(ValueError, "Incorrect file supplied"):
            _ = UploadService.parse(
                self.sample_file,
                mime_type="application/json",
                column_name="7_2009",
                with_header=True,
            )

    def test_incorrect_index(self) -> None:
        with self.assertRaisesMessage(
            ValidationError, "Column index higher than number of columns"
        ):
            _ = UploadService.parse(
                self.sample_file,
                mime_type="text/csv",
                column_index=123123,
                with_header=True,
            )

    def test_incorrect_column_name(self) -> None:
        with self.assertRaisesMessage(
            ValidationError, "Column_name name not found in header"
        ):
            _ = UploadService.parse(
                self.sample_file,
                mime_type="text/csv",
                column_name="MyIncorrectColumn",
                with_header=True,
            )
