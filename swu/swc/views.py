from django.shortcuts import render

# Create your views here.
def collections(request):
    new_context = {}
    return render(request, 'swapi/collections.html', new_context)