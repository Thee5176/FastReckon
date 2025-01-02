from django.urls import path

from .views import TransactionListView, TransactionDetailView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView

urlpatterns = [
    path("transaction/", TransactionListView.as_view(), name="transaction_list"),
    path("transaction/create/", TransactionCreateView.as_view(), name="transaction_create"),
    path("transaction/<int:pk>/", TransactionDetailView.as_view(), name="transaction_detail"),
    path("transaction/<int:pk>/update/", TransactionUpdateView.as_view(), name="transaction_update"),
    path("transaction/<int:pk>/delete/", TransactionDeleteView.as_view(), name="transaction_delete"),
]