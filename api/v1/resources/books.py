import json
from flask import abort
from flask_restx import Namespace, Resource
from v1.database.models import Book
from mongoengine import DoesNotExist
from mongoengine.queryset.visitor import Q



books = Namespace('v1/books', description='Books namespace')

books_params = books.parser()
books_params.add_argument('book_name', type=str, help='Book name', location='args')
books_params.add_argument('category', type=str, help='Book category name', location='args')
books_params.add_argument('rent_per_day', type=str, help='Rent range min,max eg. 5,10', location='args')


@books.route('/')
@books.response(404, 'Books not found')
class BooksApi(Resource):
    @books.expect(books_params)
    def get(self):
        '''List all Books'''
        try:
            args = books_params.parse_args()
            book_name, category, rent_per_day_range = args.values()
            qset = Book.objects
            if rent_per_day_range:
                rent_min, rent_max = map(lambda x: float(x), rent_per_day_range.split(','))
                if rent_min > rent_max:
                    rent_min, rent_max = rent_max, rent_min
                qset.filter(Q(rent_per_day__lte = rent_max) and Q(rent_per_day__gte = rent_min))
            if book_name:
                qset.filter(book_name__icontains=book_name)
            if category:
                qset.filter(category__contains = category)
            return json.loads(qset.to_json()), 200
        except(DoesNotExist):
            abort(404)
        except:
            abort(500)

