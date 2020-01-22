from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
#from django.views.generic import View

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
        context = { 
            self.model.__name__.lower(): obj,
            'admin_object': obj,
            'detail': True
           }
        return render(request, self.template, context)


class ObjectCreateMixin:
    model_form = None
    template = None

    def get(self, request):
        form = self.model_form()
        context = { 'form': form}
        return render(request, self.template, context)
    
    def post(self, request):

        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            #redirect может принимать url шаблон, объект класса вьюхи и еще т.д.
            return redirect(new_obj) 

        context = { 'form': bound_form }
        return render(request, self.template, context)


class ObjectUpdateMixin:
    model=None
    model_form = None
    template = None
    

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        bound_form = self.model_form(instance=obj)            
        context = {'form': bound_form, self.model.__name__.lower(): obj}
        return render(request, self.template, context)

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        #чтобы получить из формы данные и сохранить их в базу нужен request.POST
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        context = { 'form': bound_form, self.model.__name__.lower(): new_obj }
        return render(request, self.template, context)


class ObjDeleteMixin:
    model = None   
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        context ={ self.model.__name__.lower() : obj }
        return render(request, self.template, context)

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))

