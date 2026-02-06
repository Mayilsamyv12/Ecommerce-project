"""
WSGI config for Eshop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eshop.settings')

application = get_wsgi_application()

app = application

# Vercel Migration for SQLite in /tmp
if os.environ.get('VERCEL'): 
    try:
        from django.core.management import call_command
        print("Running migrations for Vercel...")
        call_command('migrate')
        print("Migrations completed.")
        
        # Load initial data if available
        if os.path.exists('initial_data.json'):
            print("Loading initial data...")
            call_command('loaddata', 'initial_data.json')
            print("Initial data loaded.")
    except Exception as e:
        print(f"Migration/Data load failed: {e}")
