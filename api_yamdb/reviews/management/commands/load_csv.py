import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('static/data/users.csv', newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.create(**row)

        with open('static/data/category.csv', newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            obj_list = []
            for row in reader:
                obj = Category(**row)
                obj_list.append(obj)
            Category.objects.bulk_create(obj_list)

        with open('static/data/titles.csv', newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            obj_list = []
            for row in reader:
                category_id = row.pop('category')
                obj = Title(**row, category_id=category_id)
                obj_list.append(obj)
            Title.objects.bulk_create(obj_list)

        with open('static/data/genre.csv', newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            obj_list = []
            for row in reader:
                obj = Genre(**row)
                obj_list.append(obj)
            Genre.objects.bulk_create(obj_list)

        with open('static/data/genre_title.csv', newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            obj_list = []
            for row in reader:
                obj = TitleGenre(**row)
                obj_list.append(obj)
            TitleGenre.objects.bulk_create(obj_list)

        with open('static/data/review.csv', newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            obj_list = []
            for row in reader:
                author_id = row.pop('author')
                obj = Review(**row, author_id=author_id)
                obj_list.append(obj)
            Review.objects.bulk_create(obj_list)

        with open('static/data/comments.csv', newline='',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            obj_list = []
            for row in reader:
                author_id = row.pop('author')
                obj = Comment(**row, author_id=author_id)
                obj_list.append(obj)
            Comment.objects.bulk_create(obj_list)

        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены в БД'))
