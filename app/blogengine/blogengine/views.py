from django.http import HttpResponse
from django.shortcuts import redirect

def redirect_blog(request):
    #создаем постоянный редирект на приложение blog из корня
    return redirect('posts_list_url', permanent=True)
