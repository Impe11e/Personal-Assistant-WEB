from django import template
from ..models import Author

register = template.Library()

def authors(author):
    if isinstance(author, Author):  # Проверяем, что передан объект модели Author
        return author.fullname
    return str(author)  # Если это строка, просто возвращаем её

register.filter('authors', authors)
