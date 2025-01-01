from django.urls import path

from .views import AccountListView, AccountDetailView, AccountCreateView, AccountUpdateView, AccountDeleteView

urlpatterns = [
    path("account/", AccountListView.as_view(), name="account_list"),
    path("account/create/", AccountCreateView.as_view(), name="account_create"),
    path("account/<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("account/<int:pk>/update/", AccountUpdateView.as_view(), name="account_update"),
    path("account/<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),
]