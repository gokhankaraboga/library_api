from django.shortcuts import render
import requests
from mylibraryapp.models import Author, Book
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    return HttpResponse("<h1>Hey</h1>")


@csrf_exempt
def book(request, bid=None):
    if request.method == "GET":
        liste = []
        if not bid:
            for obj in Book.objects.all():
                liste.append(obj.title)

            return JsonResponse({'liste': liste})
        else:
            title = str(Book.objects.get(pk=bid).title)
            for a in Book.objects.get(title=title).authors.all():
                liste.append(a.name + ' ' + a.surname)

            return JsonResponse({'liste': liste})

    elif request.method == "POST":
        database_tmp = {'title': request.POST.get('title'),
                        'lc_classification': request.POST.get(
                            'lc_classification')}

        my_obj = Book.objects.create(**database_tmp)
        authors_list = request.POST.get('authors').split(',')
        for item in authors_list:
            rank = Author.objects.get(name=item.split(' ')[0],
                                      surname=item.split(' ')[1]).id
            my_obj.authors.add(Author.objects.get(pk=rank))

    elif request.method == "PATCH":
        print 'patch calisti!'

    elif request.method == "PUT":
        print 'Put calisti'

    return HttpResponse("<h1>Hey</h1>")


@csrf_exempt
def author(request, bid=None):
    if request.method == "GET":
        if not bid:
            name_list = list()
            for obj in Author.objects.all():
                name_list.append(obj.name + " " + obj.surname)
            return JsonResponse({'name_list': name_list})
        else:
            name = Author.objects.get(pk=bid).name + Author.objects.get(
                pk=bid).surname
            return JsonResponse({'name': name})

    elif request.method == "POST":
        database_tmp = {'name': request.POST.get("name"),
                        'surname': request.POST.get("surname"),
                        'date_of_birth': request.POST.get("date_of_birth")}

        Author.objects.create(**database_tmp)

        return HttpResponse("<p>abc</p>")

    elif request.method == "PUT":
        pass

    elif request.method == "PATCH":
        pass
