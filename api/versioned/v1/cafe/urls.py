from django.urls import path, re_path, include
from common.routers import CustomSimpleRouter
from .views import CafeViewSet

router = CustomSimpleRouter(trailing_slash=False)
router.register(r'', CafeViewSet)
urlpatterns = [

]
urlpatterns += router.urls