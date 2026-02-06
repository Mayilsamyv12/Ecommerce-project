from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "Rs "+str(number)



@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1

from store.models import Category
@register.simple_tag
def get_categories():
    return Category.get_all_categories()

