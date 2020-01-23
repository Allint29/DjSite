from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

#from django.views.generic import View

from .models import Post, Tag


# Create your views here.
class ObjListMixin:  
    model = None
    template = None    
    search_url = None
    search_key = 'search'
    items_per_page = 3
    name_page = 'page'

    def get(self, request):
        search_query = request.GET.get(self.search_key, '')
        #_is_title = True if self.model.title else False
        #_is_body = True if self.model.title else False
        if search_query and self.model.title and self.model.body:
            objs = self.model.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        else:                                 
            objs = self.model.objects.all()
        paginator = Paginator(objs, self.items_per_page)

    #если запрос будет на несущ страницу переадресация на первую
        page_number = request.GET.get(self.name_page, 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?{}={}'.format(self.name_page, page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?{}={}'.format(self.name_page, page.next_page_number())
        else:
            next_url = ''

        last_page = paginator.count


        # return HttpResponse("<h1>Hello World from blog</h1>")
        context={            
            'page_object': page,
            'is_paginated': is_paginated,
            'prev_url': prev_url,
            'next_url': next_url,
            'last_page': last_page,
            'search_url': self.search_url,
            }
        return render(request, self.template, context=context)

    
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

