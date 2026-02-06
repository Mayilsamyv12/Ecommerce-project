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
        from django.conf import settings
        init_data_path = os.path.join(settings.BASE_DIR, 'initial_data.json')
        if os.path.exists(init_data_path):
            print(f"Loading initial data from {init_data_path}...")
            call_command('loaddata', init_data_path)
            print("Initial data loaded.")
        else:
            print(f"Initial data not found at {init_data_path}")
    except Exception as e:
        print(f"Migration/Data load failed: {e}")
