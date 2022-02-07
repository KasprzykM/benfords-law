from django.contrib import admin
from django.urls import path
from .views import IndexFormView

urlpatterns = [
    path("", IndexFormView.as_view(), name="home"),
    path("admin/", admin.site.urls),
]
