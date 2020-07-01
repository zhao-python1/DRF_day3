from django.urls import path

from ssrview import views

urlpatterns = [

    path("books/<str:id>/",views.BookAPIView.as_view()),
    path("books/", views.BookAPIView.as_view()),

    path("g/books/<str:id>/",views.BookGenericAPIView.as_view()),
    path("g/books/", views.BookGenericAPIView.as_view()),

    path("l/books/<str:id>/",views.BookListAPIView.as_view()),
    path("l/books/", views.BookListAPIView.as_view()),

    #登录的
    path("d/books/<str:id>/",views.BookGenericsViewSet.as_view({"post":"login"})),
    path("d/books/", views.BookGenericsViewSet.as_view({"post":"login"})),

    path("d/books/<str:id>/", views.BookGenericsViewSet.as_view({"post": "login"})),
    path("d/books/", views.BookGenericsViewSet.as_view({"post": "login"})),


]