"""
WSGI config for medicinal project.
"""

import os
from django.core.wsgi import get_wsgi_application

# Ensure correct settings module is used
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicinal.settings')

application = get_wsgi_application()

# Vercel / serverless compatibility alias
app = application