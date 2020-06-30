from django.urls import path

from library import views

urlpatterns = [

    path("books/<str:id>/",views.BookAPIView.as_view()),
    path("books/", views.BookAPIView.as_view()),
    path("2/books/<str:id>/",views.BookAPIView2.as_view()),
    path("2/books/", views.BookAPIView2.as_view()),

]