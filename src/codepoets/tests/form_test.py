from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from codepoets.forms import UploadForm


class UploadFormTest(TestCase):
    def setUp(self) -> None:
        self.sample_file = open("codepoets/tests/sample/census_2009b.dms", "rb")
        self.files_dict = {
            "data_file": SimpleUploadedFile(
                self.sample_file.name, self.sample_file.read()
            )
        }

    def tearDown(self) -> None:
        self.sample_file.close()

    def test_correct_context_column_name(self):
        form = UploadForm(
            files=self.files_dict,
            data={"column_name": "7_2009", "with_header": True},
        )
        self.assertTrue(form.is_valid())

    def test_correct_context_column_index(self):
        form = UploadForm(
            files=self.files_dict,
            data={"column_index": 2, "with_header": True},
        )
        self.assertTrue(form.is_valid())

    def test_incorrect_context(self):
        form = UploadForm(
            files=self.files_dict,
            data={"column_name": "7_2009", "with_header": True, "column_index": 1},
        )
        self.assertFalse(form.is_valid())

    def test_incorrect_context_header(self):
        form = UploadForm(
            files=self.files_dict,
            data={"column_name": "7_2009", "with_header": False},
        )
        self.assertFalse(form.is_valid())

    def test_incorrect_column_index(self):
        form = UploadForm(
            files=self.files_dict,
            data={"column_index": 123123, "with_header": False},
        )
        self.assertFalse(form.is_valid())
