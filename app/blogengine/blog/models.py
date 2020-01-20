from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Post(models.Model):
    """Модель поста страницы"""
    #заголовок индексирую для более быстрого поиска
    title = models.CharField(max_length=150, db_index=True)
    #SlugField позволяет использовать буквы цифры ниж
    #подчеркивание и дефисы все остальное валидатор непропустит
    slug = models.SlugField(max_length=150, unique=True)
    #blank=true - поле может быть пустым
    body = models.TextField(blank=True, db_index=True)
    #related_name='posts' - как будет отображаться данная связь в таблице Tag
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        '''
        Этот метод по дефолту ищет джанга, но можно определить 
        любое имя, но тогда джанга не сможет выполнить некоторые 
        функции.
        
        Этот метод возвращает ссылку на конкретный объект этого 
        класса. Url-reverse.
        '''
        return reverse('post_detail_url', kwargs={'slug': self.slug})
        

    def __str__(self):
        return 'Post: {}'.format(self.title)

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        '''
        Этот метод по дефолту ищет джанга, но можно определить 
        любое имя, но тогда джанга не сможет выполнить некоторые 
        функции.
        
        Этот метод возвращает ссылку на конкретный объект этого 
        класса. Url-reverse.
        '''
        return reverse('tag_detail_url', kwargs={'slug': self.slug})
        

    def __str__(self):
        return 'Tag: {}'.format(self.title)

