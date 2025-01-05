from django.urls import path

from .views import TransactionListView, TransactionDetailView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView

urlpatterns = [
    path("transactions/", TransactionListView.as_view(), name="transaction_list"),
    path("transactions/create/", TransactionCreateView.as_view(), name="transaction_create"),
    path("transactions/<slug:slug>", TransactionDetailView.as_view(), name="transaction_detail"),
    path("transactions/<slug:slug>/update/", TransactionUpdateView.as_view(), name="transaction_update"),
    path("transactions/<slug:slug>/delete/", TransactionDeleteView.as_view(), name="transaction_delete"),
]
