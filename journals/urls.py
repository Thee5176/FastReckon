from django.urls import path

from .views import CreateRecordView, ListRecordView

urlpatterns = [
    path("create/", CreateRecordView.as_view(), name="create_record"),
    path("view/", ListRecordView.as_view(), name="view_record"),
]
