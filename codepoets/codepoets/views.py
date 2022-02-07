import base64
import io
import urllib

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView

from .forms import UploadForm


class IndexFormView(FormView):

    template_name = "upload.html"
    form_class = UploadForm
    success_url = "graph.html"

    def form_valid(self, form: UploadForm) -> HttpResponseRedirect:
        fig, ax = form.process()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        return render(self.request, "graph.html", {"data": uri})
