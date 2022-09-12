"""Filler."""
from csv import DictReader
from django.core.management.base import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
)
from users.models import User


class Command(BaseCommand):
    """Importing csv file in local db."""

    help = (
        'Import list of files from static/data/:'
        + 'category.csv, comment.csv, genre.csv, genre_title.csv, review.csv,'
        + ' title.csv and user.csv'
    )

    def handle(self, *args, **option):
        """Filler."""
        print("Loading DB data")

        for row in DictReader(open('./static/data/users.csv')):
            print(row)
            user = User.objects.get_or_create(
                pk=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
            print(user)

        print('Users done..')

        for row in DictReader(open('./static/data/category.csv')):
            print(row)
            category = Category.objects.get_or_create(
                pk=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            print(category)

        print('Categories done..')

        for row in DictReader(open('./static/data/genre.csv')):
            genre = Genre.objects.get_or_create(
                pk=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            print(genre)

        print('Genres done..')

        for row in DictReader(open('./static/data/titles.csv')):
            title = Title.objects.get_or_create(
                pk=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.filter(pk=row['category'])
            )
            print(title)

        print('Tiltes done..')

        for row in DictReader(open('./static/data/genre_title.csv')):
            genre_title = GenreTitle.objects.get_or_create(
                pk=row['id'],
                genre=Genre.objects.filter(pk=row['genre_id']),
                title=Title.objects.filter(pk=row['title_id'])
            )
            print(genre_title)

        print('Genres of titles done..')

        for row in DictReader(open('./static/data/review.csv')):
            review = Review.objects.get_or_create(
                pk=row['id'],
                title=Title.objects.filter(pk=row['title_id']),
                text=row['text'],
                author=User.objects.filter(pk=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            print(review)

        print('Reviews done..')

        for row in DictReader(open('./static/data/comment.csv')):
            comment = Comment.objects.get_or_create(
                author=User.objects.filter(pk=row['author']),
                review=Review.objects.filter(pk=row['review_id']),
                text=row['text'],
                pub_date=row['pub_date']
            )
            print(comment)

        print('Comments done..')
        print('DB filled')
