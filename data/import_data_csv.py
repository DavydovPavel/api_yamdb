#!/usr/bin/env python
"""
    Script to import book data from .csv file to Model Database DJango
    To execute this script run: 
                                1) manage.py shell
                                2) exec(open('data/import_data_csv.py').read())
"""


import csv
from api.models import Category, Comment, Genre, Review, Title
from users.models import User


CSV_PATH = 'data/users.csv'

countSuccess = 0

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    print('Loading...')
    for row in reader:
        if countSuccess > 0:
            User.objects.create(
                id=int(row[0]),
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )
        countSuccess += 1
    print(f'{str(countSuccess)} inserted successfully! ')


CSV_PATH = 'data/category.csv'

countSuccess = 0

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    print('Loading...')
    for row in reader:
        if countSuccess > 0:
            Category.objects.create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        countSuccess += 1
    print(f'{str(countSuccess)} inserted successfully! ')


CSV_PATH = 'data/genre.csv'

countSuccess = 0

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    print('Loading...')
    for row in reader:
        if countSuccess > 0:
            Genre.objects.create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        countSuccess += 1
    print(f'{str(countSuccess)} inserted successfully! ')


CSV_PATH = 'data/titles.csv'

countSuccess = 0

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    print('Loading...')
    for row in reader:
        if countSuccess > 0:
            try:
                Title.objects.create(
                    id=row[0],
                    name=row[1],
                    year=int(row[2]),
                    category=Category.objects.get(pk=row[3])
                )
            except ValueError:
                print(row)
        countSuccess += 1
    print(f'{str(countSuccess)} inserted successfully! ')


CSV_PATH = 'data/review.csv'

countSuccess = 0

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    print('Loading...')
    for row in reader:
        if countSuccess > 0:
            Review.objects.create(
                id=row[0],
                title=Title.objects.get(pk=row[1]),
                text=row[2],
                author=User.objects.get(pk=row[3]),
                score=row[4],
                pub_date=row[5]
            )
        countSuccess += 1
    print(f'{str(countSuccess)} inserted successfully! ')


CSV_PATH = 'data/comments.csv'

countSuccess = 0

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    print('Loading...')
    for row in reader:
        if countSuccess > 0:
            Comment.objects.create(
                id=row[0],
                review=Review.objects.get(pk=row[1]),
                text=row[2],
                author=User.objects.get(pk=row[3]),
                pub_date=row[4]
            )
        countSuccess += 1
    print(f'{str(countSuccess)} inserted successfully! ')


CSV_PATH = 'data/genre_title.csv'

countSuccess = 0

with open(CSV_PATH, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    print('Loading...')
    for row in reader:
        if countSuccess > 0:
            title = Title.objects.get(pk=row[1])
            genre = Genre.objects.get(pk=row[2])
            title.genre.add(genre)
        countSuccess += 1
    print(f'{str(countSuccess)} inserted successfully! ')
