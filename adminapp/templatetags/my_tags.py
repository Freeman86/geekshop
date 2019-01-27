from django import template

register = template.Library()

from django.conf import settings

MEDIA_URL = settings.MEDIA_URL


def media_folder_products(string):
    if not string:
        string = 'products_images/default.jpg'
    return f"{MEDIA_URL}{string}"


@register.filter(name='media_folder_users')
def media_folder_users(string):
    if not string:
        string = 'users_avatars/default.jpg'
    return f"{MEDIA_URL}{string}"


register.filter('media_folder_products', media_folder_products)
# register.filter('media_folder_users', media_folder_users)