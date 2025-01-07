from django.urls import path

from .views import (
    TransactionListView, 
    TransactionDetailView, 
    TransactionCreateView, 
    TransactionUpdateView, 
    TransactionDeleteView,
)

urlpatterns = [
    path("", TransactionListView.as_view(), name="transaction_list"),
    path("create/", TransactionCreateView.as_view(), name="transaction_create"),
    path("<slug:slug>", TransactionDetailView.as_view(), name="transaction_detail"),
    path("<slug:slug>/update/", TransactionUpdateView.as_view(), name="transaction_update"),
    path("<slug:slug>/delete/", TransactionDeleteView.as_view(), name="transaction_delete"),
]
