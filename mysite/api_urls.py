
from rest_framework import routers

from accounts.views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
