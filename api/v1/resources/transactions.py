import json
from flask import abort
from flask_restx import Namespace, Resource
from v1.database.models import Book, Transaction
from mongoengine import DoesNotExist
from datetime import datetime



transactions = Namespace('v1/transactions', description='Transaction namespace')


transaction_params = transactions.parser()
transaction_params.add_argument('date', type=str, help='Date', location='args')
transaction_params.add_argument('person_name', type=str, help='Person Name', location='args')
transaction_params.add_argument('book_name', type=str, help='Book Name', location='args')

@transactions.route('/issue')
@transactions.response(404, 'Transaction not found')
class TransactionIssueApi(Resource):
    @transactions.expect(transaction_params)
    def get(self):
        try:
            args = transaction_params.parse_args()
            date, person_name, book_name = args.values()
            if not (date and person_name and book_name):
                return {"msg": "Please enter all params"}, 200
            book=Book.objects(book_name__exact=book_name)[0]
            t=Transaction(book=book, date=date, type="issued", person_name=person_name)
            t.save()
            return {"msg": "success"}, 200
        except(DoesNotExist):
            abort(404)
        except:
            abort(500)

@transactions.route('/return')
@transactions.response(404, 'Transaction not found')
class TransactionReturnApi(Resource):
    @transactions.expect(transaction_params)
    def get(self):
        try:
            args = transaction_params.parse_args()
            date, person_name, book_name = args.values()
            if not (date and person_name and book_name):
                return {"msg": "Please enter all params"}, 200
            book=Book.objects(book_name__exact=book_name)
            t = Transaction.objects(book__in=book, person_name=person_name, type="issued")[0]
            days = (datetime.strptime(t.date, '%d/%m/%y') - datetime.strptime(date, '%d/%m/%y')).days
            rent = days * t.book.rent_per_day if days else t.book.rent_per_day
            t.type = "returned"
            t.date = date
            t.rent = rent
            t.save()
            return {"msg": "success", "rent": f"Total rent {rent}"}, 200
        except(DoesNotExist):
            abort(404)
        except:
            abort(500)
            
transaction_params1 = transactions.parser()
transaction_params1.add_argument('book_name', type=str, help='Book name', location='args')

@transactions.route('/api1')
@transactions.response(404, 'Transaction not found')
class Transaction1Api(Resource):
    @transactions.expect(transaction_params1)
    def get(self):
        try:
            args = transaction_params.parse_args()
            book_name = args['book_name']
            book=Book.objects(book_name=book_name)
            t1=Transaction.objects(book__in = book)
            t2=Transaction.objects(book__in = book, type='issued')
            return {"msg": "success", "total_count": t1.count(), "currently_issued_only": t2.count()}, 200
        except(DoesNotExist):
            abort(404)
        except:
            abort(500)
            
transaction_params2 = transactions.parser()
transaction_params2.add_argument('book_name', type=str, help='Book name', location='args')

@transactions.route('/api2')
@transactions.response(404, 'Transaction not found')
class Transaction2Api(Resource):
    @transactions.expect(transaction_params2)
    def get(self):
        try:
            args = transaction_params.parse_args()
            book_name = args['book_name']
            book=Book.objects(book_name=book_name)
            t1=Transaction.objects(book__in = book)
            total_rent = 0
            for t in t1:
                if t.rent:
                    total_rent+= t.rent
            return {"msg": "success", "total_rent": total_rent}, 200
        except(DoesNotExist):
            abort(404)
        except:
            abort(500)
            
transaction_params3 = transactions.parser()
transaction_params3.add_argument('person_name', type=str, help='Person name', location='args')

@transactions.route('/api3')
@transactions.response(404, 'Transaction not found')
class Transaction3Api(Resource):
    @transactions.expect(transaction_params3)
    def get(self):
        try:
            args = transaction_params.parse_args()
            person_name = args['person_name']
            t1=Transaction.objects(person_name=person_name)
            list_of_books = []
            for t in t1:
                list_of_books.append(t.book.book_name)
            return {"msg": "success", "list_of_books": list_of_books}, 200
        except(DoesNotExist):
            abort(404)
        except:
            abort(500)
            
transaction_params4 = transactions.parser()
transaction_params4.add_argument('date_range', type=str, help='Range of date', location='args')

@transactions.route('/api4')
@transactions.response(404, 'Transaction not found')
class Transaction4Api(Resource):
    @transactions.expect(transaction_params4)
    def get(self):
        try:
            args = transaction_params.parse_args()
            date_min, date_max = args['date_range'].split(',')
            date_min, date_max = datetime.strptime(date_min, '%d/%m/%y'),datetime.strptime(date_max, '%d/%m/%y') 
            if date_min > date_max:
                date_min, date_max = date_max, date_min
            t1 = Transaction.objects(date__lte=date_max, date__gte=date_min, type="issued")
            list_of_books = []
            for t in t1:
                list_of_books.append(t.book.book_name)
            return {"msg": "success", "list_of_books": list_of_books}, 200
        except(DoesNotExist):
            abort(404)
        except:
            abort(500)
