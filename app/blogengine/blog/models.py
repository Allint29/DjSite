from time import time
from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + "-" + str(int(time()))




# Create your models here.
class Post(models.Model):
    """Модель поста страницы"""
    #заголовок индексирую для более быстрого поиска
    title = models.CharField(max_length=150, db_index=True)
    #SlugField позволяет использовать буквы цифры ниж
    #подчеркивание и дефисы все остальное валидатор непропустит
    slug = models.SlugField(max_length=150, blank=True, unique=True)
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
      
    def get_update_url(self):
        '''
        Это кастомный генератор ссылки на страницу 
        редактирования объекта.
        '''
        return reverse('post_update_url', kwargs = {'slug': self.slug})

    def get_delete_url(self):
        '''
        Это кастомный генератор ссылки на страницу 
        редактирования объекта.
        '''
        return reverse('post_delete_url', kwargs = {'slug': self.slug})

    #переопределяю функцию save() -чтобы сделать свой алгоритм сохранения
    def save(self, *args, **kwargs):
        #если данный экземпляр есть только в оперативке ноеще не сохранен в БД 
        #то есть не имеет id тогда вызываю gen_slug
        if not self.id:
            self.slug = gen_slug(self.title)

        super().save(*args, **kwargs)

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
        
    def get_update_url(self):
        '''
        Это кастомный генератор ссылки на страницу 
        редактирования объекта.
        '''
        return reverse('tag_update_url', kwargs = {'slug': self.slug})

    def get_delete_url(self):
        '''
        Это кастомный генератор ссылки на страницу 
        редактирования объекта.
        '''
        return reverse('tag_delete_url', kwargs = {'slug': self.slug})

    def __str__(self):
        return 'Tag: {}'.format(self.title)

