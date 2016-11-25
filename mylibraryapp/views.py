from django.shortcuts import render
import json
from mylibraryapp.models import Author, Book
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
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
                if not Author.objects.filter(name=tmp_author_dict['name'],
                                             surname=tmp_author_dict[
                                                 'surname']).exists():
                    author_obj = Author.objects.create(**tmp_author_dict)

                else:
                    author_obj = Author.objects.get(
                        name=tmp_author_dict['name'],
                        surname=tmp_author_dict['surname'])

                book_obj.authors.add(Author.objects.get(pk=author_obj.id))

    elif request.method == "PATCH":
        content = request.body.split('\n')[4:-3]
        book_list = [x.split(',') for x in content]

        with open('/Users/gokhankaraboga/Desktop/new_books.csv', 'wb')as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(x.split(',') for x in content)
            f.close()

        for book in book_list:
            tmp_book_dict = {'title': book[0],
                             'lc_classification': book[1]}
            if not Book.objects.filter(title=tmp_book_dict['title']).exists():
                book_obj = Book.objects.create(**tmp_book_dict)
            else:
                book_obj = Book.objects.get(title=tmp_book_dict['title'])

            for i in xrange(0, len(book[2:]), 3):
                tmp_author_dict = {'name': book[2:][i],
                                   'surname': book[2:][i + 1],
                                   'date_of_birth': book[2:][i + 2]}

                if not Author.objects.filter(name=tmp_author_dict['name'],
                                             surname=tmp_author_dict[
                                                 'surname']).exists():
                    author_obj = Author.objects.create(**tmp_author_dict)

                    book_obj.authors.add(author_obj.id)
                else:
                    author_obj = Author.objects.get(
                        name=tmp_author_dict['name'],
                        surname=tmp_author_dict[
                            'surname'])
                    if not Book.objects.filter(pk=book_obj.pk,
                                               authors__pk=author_obj.pk).exists():
                        book_obj.authors.add(author_obj.id)

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
            book_obj[0].authors.clear()
            for item in authors.split(','):
                rank = Author.objects.get(name=item.split(' ')[0],
                                          surname=item.split(' ')[1]).id
                book_obj[0].authors.add(Author.objects.get(pk=rank))
        else:
            Book.objects.filter(pk=bid).update(**update_dict)

    elif bid and request.method == "PUT":
        update_dict = json.loads(request.body)
        book_obj = Book.objects.filter(pk=bid)

        if "authors" in update_dict:
            authors_list = update_dict.pop("authors").split(",")

        book_obj.name = None
        book_obj.surname = None
        book_obj[0].authors.clear()

        book_obj.update(**update_dict)

        if authors_list:
            for i in xrange(0, len(authors_list),3):
                try:
                    author_obj = Author.objects.get(name=authors_list[i],
                                                    surname=authors_list[
                                                        i + 1],
                                                    date_of_birth=authors_list[
                                                        i + 2])
                except ObjectDoesNotExist:
                    author_obj = Author.objects.create(name=authors_list[i],
                                                       surname=authors_list[
                                                           i + 1],
                                                       date_of_birth=
                                                       authors_list[i + 2])

                rank = author_obj.id

                book_obj[0].authors.add(Author.objects.get(pk=rank))

        return HttpResponse("<p>abc</p>")

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

    elif bid and request.method == "PATCH":
        author_info = [request.body.split('\n')[i].strip('\r') for i in
                       xrange(3, len(request.body.split('\n')), 4)]

        key_info = [
            request.body.split('\n')[i].strip('\r').split(" name=")[1].strip(
                "\"")
            for i in xrange(1, len(request.body.split("\n")) - 3, 4)]

        tmp_author_dict = {}
        for i in xrange(len(key_info)):
            tmp_author_dict[key_info[i]] = author_info[i]

        author_obj = Author.objects.filter(pk=bid)
        author_obj.update(**tmp_author_dict)

        return HttpResponse("<h1>Selam</h1>")

    elif bid and request.method == "PUT":
        update_dict = json.loads(request.body)
        author_obj = Author.objects.filter(pk=bid)

        author_obj.name = None
        author_obj.surname = None
        author_obj.date_of_birth = None

        author_obj.update(**update_dict)

        return HttpResponse("<p>abc</p>")
