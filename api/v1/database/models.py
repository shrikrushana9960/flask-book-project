from mongoengine import Document, ReferenceField, StringField, ListField, DecimalField


class Todo(Document):
    title = StringField(required=True, max_length=200)
    content = StringField(required=True)

class Book(Document):
    book_name = StringField(required=True, max_length=200)
    category = ListField(StringField(max_length=100))
    rent_per_day = DecimalField(min_value=0)

class Transaction(Document):
    book = ReferenceField(Book)
    date = StringField()
    type = StringField(max_length=8,min_length=6)
    person_name = StringField(max_length=100)
    rent = DecimalField(min_value=0)

    meta = {'allow_inheritance': True}
