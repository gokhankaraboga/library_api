from django.shortcuts import render
import requests
import json
from mylibraryapp.models import Author, Book
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv


# Create your views here.

def index(request):
    return HttpResponse("<h1>Hey</h1>")


@csrf_exempt
def library(request):
    if request.method == "POST":
        Book.objects.all().delete()
        Author.objects.all().delete()

        csv_file = csv.reader(request.FILES['upload_file'], delimiter=',',
                              quotechar='"')
        for data in csv_file:
            tmp_book_dict = {'title': data[0],
                             'lc_classification': data[1]}

            book_obj = Book.objects.create(**tmp_book_dict)

            for i in xrange(0, len(data[2:]), 3):
                tmp_author_dict = {'name': data[2:][i],
                                   'surname': data[2:][i + 1],
                                   'date_of_birth': data[2:][i + 2]}
                author_obj = Author.objects.create(**tmp_author_dict)
                book_obj.authors.add(Author.objects.get(pk=author_obj.id))

    elif request.method == "PATCH":
        pass

    return HttpResponse("<p>Surungenler Sehri</p>")


@csrf_exempt
def book(request, bid=None):
    if request.method == "GET":
        title_parameter = request.GET.get('title')
        liste = list()

        if bid:
            title = str(Book.objects.get(pk=bid).title)
            for a in Book.objects.get(title=title).authors.all():
                liste.append(a.name + ' ' + a.surname)

            return JsonResponse({'title': title, 'liste': liste})

        else:
            if title_parameter:
                book_obj = Book.objects.get(title=title_parameter)
                for a in book_obj.authors.all():
                    liste.append(a.name + ' ' + a.surname)

                return JsonResponse({'title': book_obj.title, 'liste': liste})
            else:
                for obj in Book.objects.all():
                    liste.append(obj.title)

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

    elif bid and request.method == "PATCH":
        update_dict = json.loads(request.body)
        authors = update_dict.get('authors', None)
        update_dict.pop('authors', None)
        if authors:
            book_obj = Book.objects.filter(pk=bid)
            book_obj.update(**update_dict)
            # !!!!!!!!!!!!!!book_obj.authors.remove()!!!!!!!!!!!!!
            for item in authors.split(','):
                rank = Author.objects.get(name=item.split(' ')[0],
                                          surname=item.split(' ')[1]).id
                book_obj.authors.add(Author.objects.get(pk=rank))
        else:
            Book.objects.filter(pk=bid).update(**update_dict)

    elif bid and request.method == "PUT":
        print 'Put calisti'

    else:
        print 'olmadi'
    return HttpResponse("<h1>Hey</h1>")


@csrf_exempt
def author(request, bid=None):
    if request.method == "GET":
        name_parameter = request.GET.get('name')
        surname_parameter = request.GET.get('surname')
        if not bid:
            if name_parameter and surname_parameter:
                author_obj = Author.objects.get(name=name_parameter,
                                                surname=surname_parameter)
                full_name = author_obj.name + " " + author_obj.surname
                return JsonResponse({'full_name': full_name})

            elif name_parameter:
                author_obj = Author.objects.get(name=name_parameter)
                full_name = author_obj.name + " " + author_obj.surname
                return JsonResponse({'full_name': full_name})
            elif surname_parameter:
                author_obj = Author.objects.get(surname=surname_parameter)
                full_name = author_obj.name + " " + author_obj.surname
                return JsonResponse({'full_name': full_name})
            else:
                name_list = list()
                for obj in Author.objects.all():
                    name_list.append(obj.name + " " + obj.surname)
                return JsonResponse({'name_list': name_list})

        else:
            author_obj = Author.objects.get(pk=bid)
            full_name = author_obj.name + " " + author_obj.surname
            return JsonResponse({'full_name': full_name})

    elif request.method == "POST":
        database_tmp = {'name': request.POST.get("name"),
                        'surname': request.POST.get("surname"),
                        'date_of_birth': request.POST.get("date_of_birth")}

        Author.objects.create(**database_tmp)

        return HttpResponse("<p>abc</p>")

    elif bid and request.method == "PUT":
        pass

    elif bid and request.method == "PATCH":
        update_dict = json.loads(request.body)
        Author.objects.filter(pk=bid).update(**update_dict)

        return HttpResponse("<p>abc</p>")
