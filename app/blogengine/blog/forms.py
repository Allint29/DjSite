from django import forms
from django.core.exceptions import ValidationError

from .models import Tag, Post


class TagForm(forms.ModelForm): #(forms.Form):
    #title = forms.CharField(max_length=50)
    #slug = forms.CharField(max_length=150)

    #title.widget.attrs.update({ 'class': 'form-control' })
    #slug.widget.attrs.update({ 'class': 'form-control' })
    class Meta:
        model = Tag
        fields = ['title','slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
            }



    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower() # self.cleaned_data.get('slug')
        #фильтрация слов которые нельза импортировать в бд - систнемные слова
        #например слово пути маршрута 'create'
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        #проверим слаг на наличие в словаре хранимых слов зарегистрированных
        #если count > 0 то возвращается true если count == 0  то false
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}" slug already'.format(new_slug))

        return new_slug


    #переопределим метод save()
    #при наследовании от forms.ModelForm этот метод нельзя переопределить,
    #так как у него есть свой универсальный метод save()
    #def save(self):
    #    new_tag=Tag.objects.create(title=self.cleaned_data['title'],
    #                               slug=self.cleaned_data['slug']
    #                               )
    #    return new_tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['title','slug', 'body', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
                        
            }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower() # self.cleaned_data.get('slug')
        #фильтрация слов которые нельза импортировать в бд - систнемные слова
        #например слово пути маршрута 'create'
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        #здесь не делаем проверку на уникальность, так
        #так как позже сделаем чтобы слаг генерировался 
        #уникальным автоматически
        #if Tag.objects.filter(slug__iexact=new_slug).count():
        #    raise ValidationError('Slug must be unique. We have "{}" slug already'.format(new_slug))
        return new_slug

