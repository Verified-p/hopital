"""
WSGI config for medicinal project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicinal.settings')

application = get_wsgi_application()

# Vercel compatibility
