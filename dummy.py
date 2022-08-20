from pprint import pp
from api.v1.database.models import Book, Todo, Transaction
from mongoengine import connect
from mongoengine.queryset.visitor import Q


connect('app', host='mongodb://mongodb/dev')
#
# Book(book_name="Book1", category=["book1", "book"], rent_per_day=23.3).save()
# Book(book_name="Book2", category=["book1", "book"], rent_per_day=20.3).save()
# Book(book_name="Book3", category=["book1", "book"], rent_per_day=13.3).save()
# Book(book_name="Book4", category=["bo1", "book", "ook1"], rent_per_day=23.3).save()
# Book(book_name="Book5", category=["bo1", "book", "ook2"], rent_per_day=23.3).save()
# Book(book_name="Book6", category=["bo1", "book", "ook3"], rent_per_day=23.3).save()
# Book(book_name="Book7", category=["bo1", "book", "ook4"], rent_per_day=23.3).save()
# Book(book_name="Bookk", category=["bo1", "book", "ook5"], rent_per_day=23.3).save()
# Book(book_name="Book7", category=["bo1", "book", "ook6"], rent_per_day=23.3).save()
# Book(book_name="Book8", category=["bo1", "book", "ook7"], rent_per_day=23.3).save()
# Book(book_name="Book0", category=["bo1", "book", "ooka"], rent_per_day=23.3).save()
# Book(book_name="Bookr", category=["bo1", "book", "ookca"], rent_per_day=23.3).save()
# Book(book_name="Bookq", category=["bo1", "book", "ooka"], rent_per_day=23.3).save()
# Book(book_name="Booka", category=["bo1", "book", "ooka"], rent_per_day=23.3).save()
# Book(book_name="Bookq", category=["book1", "book"], rent_per_day=23.3).save()
# Todo(title="todo1", content="Abc").save()

# book_list = Book.objects(
#     Q(rent_per_day__lte = 25) &
#     Q(rent_per_day__gte = 20)
# )
# pp(book_list.to_json())
book=Book.objects(book_name__exact='Book2')
print(book)
# t=Transaction(book=book, date='2022-08-16', type="issued", person_name='mia')
# t.save()
t=Transaction.objects(book__in = book)[0]
print(t.book.book_name)
