import magic
from django import forms
from django.core.exceptions import ValidationError

from .service import UploadService, BenfordsLawService


class UploadForm(forms.Form):

    column_name = forms.CharField(required=False, help_text="Specify column name.")
    column_index = forms.IntegerField(
        required=False,
        help_text="Or specify column index.",
        min_value=0,
    )
    with_header = forms.BooleanField(required=False, initial=False)
    data_file = forms.FileField(required=True)

    def clean_data_file(self):
        data = self.files["data_file"]
        mime_type = magic.from_buffer(data.file.read(2048 * 2), mime=True)
        if mime_type not in UploadService.MIMES_MAPPING:
            raise ValidationError(
                "Incorrect mime_type detected, was %(mime_type)s",
                code="data_file",
                params={"mime_type": mime_type},
            )
        self.cleaned_data["mime_type"] = mime_type
        return data

    def clean(self):
        if self.cleaned_data["column_index"] and self.cleaned_data["column_name"]:
            raise ValidationError("Cannot specify both index and column name")
        self.cleaned_data["parsed_input"] = UploadService.parse(**self.cleaned_data)
        return self.cleaned_data

    def process(self):
        return BenfordsLawService.get_plot(self.cleaned_data["parsed_input"])
