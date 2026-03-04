import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Eshop.settings")
django.setup()

from django.test import Client

c = Client(raise_request_exception=True, SERVER_NAME='127.0.0.1')
session = c.session
session['customer'] = 1
session.save()

try:
    response = c.get('/cart/', HTTP_HOST='127.0.0.1')
    print("Status Code:", response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
