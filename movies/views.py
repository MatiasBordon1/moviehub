from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .tmdb_api import search_movies, get_popular_movies
from .models import FavoriteMovie, Comment

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


# ------------------- REGISTRO -------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Registro exitoso. ¡Ahora podés iniciar sesión!")
            return redirect("login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"❌ {field.capitalize()}: {error}")
    else:
        form = UserCreationForm()

    return render(request, "movies/register.html", {"form": form})


# ------------------- BÚSQUEDA DE PELÍCULAS -------------------
@login_required
def movie_search(request):
    results = []

    if request.method == "POST":
        query = request.POST.get("query", "").strip()
        min_rating = request.POST.get("min_rating")
        release_year = request.POST.get("release_year")
        genre_filter = request.POST.get("genre")

        if query:
            results = search_movies(query)
        else:
            results = get_popular_movies(pages=5)

        # Filtros
        if min_rating:
            try:
                min_rating = float(min_rating)
                results = [r for r in results if r["rating"] >= min_rating]
            except ValueError:
                pass

        if release_year:
            try:
                release_year = int(release_year)
                results = [
                    r for r in results 
                    if r["release_date"] and int(r["release_date"][:4]) >= release_year
                ]
            except ValueError:
                pass

        if genre_filter:
            try:
                genre_filter = int(genre_filter)
                results = [r for r in results if genre_filter in r.get("genre_ids", [])]
            except ValueError:
                pass

    return render(request, "movies/search.html", {"results": results})


# ------------------- AGREGAR FAVORITA -------------------
@login_required
def add_favorite(request):
    if request.method == "POST":
        tmdb_id = request.POST.get("tmdb_id")
        if not tmdb_id or not tmdb_id.isdigit():
            messages.error(request, "ID de película inválido.")
            return redirect("movie_search")

        tmdb_id = int(tmdb_id)

        title = request.POST.get("title", "")
        overview = request.POST.get("overview", "")
        poster_url = request.POST.get("poster_url") or None
        release_date = request.POST.get("release_date", "")
        genre_ids = request.POST.get("genre_ids", "")
        rating = float(request.POST.get("rating") or 0)

        if not FavoriteMovie.objects.filter(tmdb_id=tmdb_id, user=request.user).exists():
            FavoriteMovie.objects.create(
                user=request.user,
                tmdb_id=tmdb_id,
                title=title,
                overview=overview,
                poster_url=poster_url,
                release_date=release_date,
                genre_ids=genre_ids,
                rating=rating,
            )
            messages.success(request, f"{title} fue agregada a tus favoritas.")
        else:
            messages.info(request, f"{title} ya estaba en tus favoritas.")

    return redirect("movie_search")


# ------------------- LISTAR FAVORITAS -------------------
@method_decorator(login_required, name='dispatch')
class FavoriteListView(ListView):
    model = FavoriteMovie
    template_name = "movies/favorite_list.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return FavoriteMovie.objects.filter(user=self.request.user)


# ------------------- ELIMINAR FAVORITA -------------------
@method_decorator(login_required, name='dispatch')
class FavoriteDeleteView(DeleteView):
    model = FavoriteMovie
    template_name = "movies/favorite_confirm_delete.html"
    success_url = reverse_lazy("favorite_list")

    def get_queryset(self):
        return FavoriteMovie.objects.filter(user=self.request.user)


# ------------------- COMENTARIOS -------------------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'movies/comment_form.html'

    def form_valid(self, form):
        favorite = get_object_or_404(FavoriteMovie, pk=self.kwargs['favorite_id'], user=self.request.user)
        form.instance.favorite = favorite
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('favorite_list')


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'movies/comment_form.html'

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('favorite_list')


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'movies/comment_confirm_delete.html'
    success_url = reverse_lazy('favorite_list')

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
