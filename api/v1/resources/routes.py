from v1.resources.todos import todos
from v1.resources.books import books
from v1.resources.transactions import transactions


def initialize_routes(api):
    api.add_namespace(todos)
    api.add_namespace(books)
    api.add_namespace(transactions)
