from django.urls import path
from . import views

app_name = 'entries'

urlpatterns = [
    path("", views.index, name="index"),  # Ruta para el índice
    path("new_page/", views.new_page, name="new_page"),  # Ruta para crear una nueva página
    path("search/", views.search, name="search"),  # Ruta para la búsqueda
    path("edit/<str:name>/", views.edit_page, name="edit_page"),  # Ruta para editar una página
    path("random/", views.random_page, name="random_page"),  # Ruta para seleccionar una página aleatoria
    path("<str:name>/", views.entry, name="entry"),  # Ruta para ver una entrada específica
]
