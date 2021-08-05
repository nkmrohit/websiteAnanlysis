"""
WSGI config for itnsweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
from django.conf import settings

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itnsweb.settings')
sys.path.append(os.path.join(settings.BASE_DIR, "backend"))
sys.path.append(os.path.join(settings.BASE_DIR, "frontend"))
sys.path.append(os.path.join(settings.BASE_DIR, "customer"))

application = get_wsgi_application()
