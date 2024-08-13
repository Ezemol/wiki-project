from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
import random

# Vista para mostrar el índice de todas las entradas
def index(request):
    entries = util.list_entries()  # Obtiene todas las entradas
    return render(request, 'encyclopedia/index.html', {
        "entries": entries  # Pasa las entradas al template
    })

# Vista para mostrar una entrada específica
def entry(request, name):
    content = util.get_entry(name)  # Obtiene el contenido de la entrada
    return render(request, "encyclopedia/entry.html", {
        "content": content,  # Pasa el contenido al template
        "name": name.capitalize()  # Pasa el nombre capitalizado al template
    }) 

# Vista para manejar la búsqueda de entradas
def search(request):
    query = request.GET.get('q', None)  # Obtiene el parámetro de búsqueda
    if query is None or query == '':
        return redirect('entries:index')  # Redirige al índice si no hay búsqueda

    content = util.get_entry(query)  # Intenta obtener el contenido de la entrada exacta
    if content is not None:
        # Si se encuentra una coincidencia exacta, renderiza la página de la entrada
        return render(request, 'encyclopedia/entry.html', {
            "name": query.capitalize(),  # Pasa el nombre capitalizado al template
            "content": content  # Pasa el contenido al template
        })

    all_entries = util.list_entries()  # Obtiene todas las entradas
    matching_entries = [entry for entry in all_entries if query.lower() in entry.lower()]  # Filtra las entradas que contienen la consulta
    return render(request, 'encyclopedia/search_results.html', {
        "query": query,  # Pasa la consulta al template
        "entries": matching_entries  # Pasa las entradas coincidentes al template
    })

# Permite al usuario crear una nueva página
def new_page(request):
    if request.method == "POST":
        title = request.POST.get('title')  # Obtiene el título del formulario
        content = request.POST.get('content')  # Obtiene el contenido del formulario

        # Verificar si ya existe una entrada con el mismo título
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new_page.html", {
                "error": "An entry with this title already exists."
            })
        
        # Guardar la nueva entrada
        util.save_entry(title, content)
        return redirect('entries:entry', name=title)
    
    # Mostrar el formulario para crear una nueva entrada
    return render(request, "encyclopedia/new_page.html")

# Vista para manejar la edición de una página existente
def edit_page(request, name):
    if request.method == "POST":
        content = request.POST.get('content')  # Obtiene el contenido del formulario
        util.save_entry(name, content)  # Guarda la entrada actualizada
        return redirect('entries:entry', name=name)  # Redirige a la página de la entrada

    content = util.get_entry(name)  # Obtiene el contenido de la entrada
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

    # Renderiza el formulario de edición con el contenido actual de la entrada
    return render(request, "encyclopedia/edit_page.html", {
        "name": name,
        "content": content
    })

# Te lleva a una entrada aleatoria
def random_page(request):
    entries = util.list_entries() # Lista de todas las entradas
    if entries:  # Verifica si hay entradas disponibles
        random_entry = random.choice(entries)
        return redirect('entries:entry', name=random_entry)
    else:
        return render(request, 'encyclopedia/error.html', {
            "message": "There are no entries available."
        })