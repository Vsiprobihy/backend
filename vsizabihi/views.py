from django.shortcuts import render


def api_root_view(request):
    return render(request, 'index.html')
