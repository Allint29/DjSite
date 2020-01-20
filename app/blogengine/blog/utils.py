from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Post, Tag

class ObjectDetailMixin:
    """
    Миксин для вывода информации на страницу.
    
    Передаем в него переменные - на выходе получаем рендер
    страницы с конкретными подставленными типами.

    переменные:
    obj - объект для вывода на страницу.
    self.model - Модель объекта - класс БД.
    self.template - путь доя страницы html
    self.model.__name__.lower() - имя класса-модели с маленькой
               буквы для элемента словаря. Данное имя использует 
               конкретный html. На выходе получаю например:
               context = { 'post': post }
    """
    model = None
    template = None

    def get(self, request, slug):
        #post = Post.objects.get(slug__iexact=slug)
        obj = get_object_or_404(self.model, slug__iexact=slug)
        context = { self.model.__name__.lower(): obj }
        return render(request, self.template, context)
