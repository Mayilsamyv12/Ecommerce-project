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

@register.filter(name='order_status_step')
def order_status_step(status, step_name):
    ordering = ['Placed', 'Shipped', 'Out For Delivery', 'Delivered']
    try:
        current_index = ordering.index(status)
        step_index = ordering.index(step_name)
        return current_index >= step_index
    except ValueError:
        return False

@register.filter(name='order_progress_class')
def order_progress_class(status):
    mapping = {
        'Placed': 'w-0',
        'Shipped': 'w-33',
        'Out For Delivery': 'w-66',
        'Delivered': 'w-100'
    }
    return mapping.get(status, 'w-0')
