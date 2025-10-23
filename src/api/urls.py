from django.urls import path

from api.views.document_view import DocumentView

urlpatterns = [path("documents/", DocumentView.as_view(), name="documents")]
