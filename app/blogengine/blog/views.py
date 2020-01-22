from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin

#from django.http import HttpResponse

from .models import Post, Tag
from .utils import ObjectDetailMixin, ObjectCreateMixin, \
    ObjectUpdateMixin, ObjDeleteMixin
from .forms import TagForm, PostForm

# Create your views here.
def post_list(request):
    n = 'Alex'
    posts = Post.objects.all()
    # return HttpResponse("<h1>Hello World from blog</h1>")
    context={'name': n, 'posts': posts}
    return render(request, 'blog/index.html', context)


def tags_list(request):
    tags = Tag.objects.all()
    context = { 'tags': tags }
    return render(request, 'blog/tags_list.html', context)

#методы лучше переопределитьь в классы для 
#возможности наследования
#def post_detail(request, slug):
#    post = Post.objects.get(slug__iexact=slug)
#    context = { 'post': post }
#    return render(request, 'blog/post_detail.html', context)


class PostDetail(ObjectDetailMixin, View):
    '''

    Класс детализации поста наследуется от миксина, 
    который принимает две переменные для поиска инфы из
    БД и пересылки его в представление, эти переменные 
    нужно указать

    '''
    model = Post
    template = 'blog/post_detail.html'
    #переопределяю метод get у класса View
    #это прием get запроса все проверки делает View
    #def get(self, request, slug):
    #    #post = Post.objects.get(slug__iexact=slug)
    #    post = get_object_or_404(Post, slug__iexact=slug)
    #    context = { 'post': post }
    #    return render(request, 'blog/post_detail.html', context)


#def tag_detail(request, slug):
#    tag = Tag.objects.get(slug__iexact=slug)
#    context = {'tag': tag}
#    return render(request, 'blog/tag_detail.html', context)

  
class TagDetail(ObjectDetailMixin, View):
    '''

    Класс детализации поста наследуется от миксина, 
    который принимает две переменные для поиска инфы из
    БД и пересылки его в представление, эти переменные 
    нужно указать

    '''
    model = Tag
    template = 'blog/tag_detail.html'
    #переопределяю метод get у класса View
    #это прием get запроса все проверки делает View
    #def get(self, request, slug):
    #    #tag = Tag.objects.get(slug__iexact=slug)
    #    tag = get_object_or_404(Tag, slug__iexact=slug)
    #    context = {'tag': tag}
    #    return render(request, 'blog/tag_detail.html', context)

class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True
    #def get(self, request):
    #    form = TagForm()
    #    context = { 'form': form}
    #    return render(request, 'blog/tag_create.html', context)
    
    #def post(self, request):

    #    bound_form = TagForm(request.POST)

    #    if bound_form.is_valid():
    #        new_tag = bound_form.save()
    #        #redirect может принимать url шаблон, объект класса вьюхи и еще т.д.
    #        return redirect(new_tag) 

    #    context = { 'form': bound_form }
    #    return render(request, 'blog/tag_create.html', context)

class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True
    #def get(self, request):
    #    form = PostForm()
    #    context = { 'form': form }
    #    return render(request, 'blog/post_create_form.html', context)

    #def post(self, request):
    #    bound_form = PostForm(request.POST)
    #    if bound_form.is_valid():
    #        new_post = bound_form.save()
    #        return redirect(new_post)
    #    context = { 'form': bound_form }
    #    return render(request, 'blog/post_create_form.html', context)


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model=Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True

#удаление
class PostDelete(LoginRequiredMixin, ObjDeleteMixin, View):
        model = Post        
        template = 'blog/post_delete_form.html'
        redirect_url = 'posts_list_url'
        raise_exception = True

class TagDelete(LoginRequiredMixin, ObjDeleteMixin, View):
        model = Tag        
        template = 'blog/tag_delete_form.html'
        redirect_url = 'tags_list_url'
        raise_exception = True


