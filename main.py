# >> Imports
import os

from django.core.wsgi import get_wsgi_application
from bots import green


# >> Run
# Web
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()

# Bots
print("botbot")
green.main()
