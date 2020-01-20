from django.shortcuts import render, get_object_or_404
from django.views.generic import View
#from django.http import HttpResponse

from .models import Post, Tag
from .utils import ObjectDetailMixin

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
