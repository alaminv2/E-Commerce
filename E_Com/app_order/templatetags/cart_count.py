from django import template
from app_order.models import Order

register = template.Library()


@register.filter
def item_count(user):
    obj = Order.objects.filter(user=user, ordered=False)
    if obj.exists():
        return obj[0].orderitems.count()
    else:
        return 0
