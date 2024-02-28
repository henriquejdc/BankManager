"""
ASGI config for bank_manager project.

It exposes the ASGI callable as a module-level variable named ``application``.

"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_manager.settings')

application = get_asgi_application()
