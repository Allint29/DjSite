from django.shortcuts import render
#from django.http import HttpResponse


# Create your views here.
def post_list(request):
    n = 'Alex'
    list_names = ['Olga','Pavel','Nikolay']
    # return HttpResponse("<h1>Hello World from blog</h1>")
    context={'name': n, 'list_names': list_names}
    return render(request, 'blog/index.html', context)


    