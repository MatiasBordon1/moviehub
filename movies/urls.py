from django.urls import path
from . import views
from .views import FavoriteListView, FavoriteDeleteView
from django.contrib.auth import views as auth_views
from movies import views as movie_views


urlpatterns = [
    path('', views.movie_search, name='movie_search'),
    path('add/', views.add_favorite, name='add_favorite'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite_list'),
    path('favorites/delete/<int:pk>/', views.FavoriteDeleteView.as_view(), name='favorite_delete'),
    path('favoritas/', FavoriteListView.as_view(), name='favorite-list'),
    path('eliminar/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
    path('favoritas/<int:favorite_id>/comentario/nuevo/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comentario/<int:pk>/editar/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comentario/<int:pk>/eliminar/', views.CommentDeleteView.as_view(), name='comment_delete'),
     path('login/', auth_views.LoginView.as_view(template_name='movies/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='movie_search'), name='logout'),
    path('register/', movie_views.register, name='register'),

]
