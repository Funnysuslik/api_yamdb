"""Filler."""
from csv import DictReader
from django.core.management.base import BaseCommand

from titles.models import (
    Category,
    Comment,
    User,
    Genre,
    GenreTitle,
    Review,
    Title,
)


class Command(BaseCommand):
    """Importing csv file in local db."""

    help = (
        'Import list of files from static/data/:'
        + 'category.csv, comment.csv, genre.csv, genre_title.csv, review.csv,'
        + ' title.csv and user.csv'
    )

    def import_csv(self, file):
        """Filler."""
        print("Loading childrens data")

        for row in DictReader(open('.static/data/user.csv')):
            user = User(
                pk=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()

        print('Users done..')

        for row in DictReader(open('.static/data/category.csv')):
            category = Category(
                pk=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            category.save()

        print('Categories done..')

        for row in DictReader(open('.static/data/genre.csv')):
            genre = Genre(
                pk=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            genre.save()

        print('Genres done..')

        for row in DictReader(open('.static/data/title.csv')):
            title = Title(
                pk=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.filter(pk=row['category'])
            )
            title.save()

        print('Tiltes done..')

        for row in DictReader(open('.static/data/genre_title.csv')):
            genre_title = GenreTitle(
                pk=row['id'],
                genre=Genre.objects.filter(pk=row['genre_id']),
                title=Title.objects.filter(pk=row['title_id'])
            )
            genre_title.save()

        print('Genres of titles done..')

        for row in DictReader(open('.static/data/review.csv')):
            review = Review(
                pk=row['id'],
                title=Title.objects.filter(pk=row['title_id']),
                text=row['text'],
                author=User.objects.filter(pk=row['author']),
                score=row['score'],
                pub_date=row['pub_date']
            )
            review.save()

        print('Reviews done..')

        for row in DictReader(open('.static/data/comment.csv')):
            comment = Comment(
                author=User.objects.filter(pk=row['author']),
                review=Review.objects.filter(pk=row['review_id']),
                text=row['text'],
                pub_date=row['pub_date']
            )
            comment.save()

        print('Comments done..')
        print('DB filled')
