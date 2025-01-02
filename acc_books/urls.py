from django.urls import path

from .views import BookListView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path("book/", BookListView.as_view(), name="book_list"),
    path("book/create/", BookCreateView.as_view(), name="book_create"),
    path("book/<int:pk>/update/", BookUpdateView.as_view(), name="book_update"),
    path("book/<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),
]