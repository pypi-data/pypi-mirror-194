from rest_framework import routers

from dvadmin_third.views.third_users import (
    ThirdUsersViewSet,
    ThirdUsersLoginViewSet,
    static,
    index,
    ConfirmLoginViewSet,
    check_file
)
from django.urls import re_path

router = routers.SimpleRouter()

router.register(r'third_users', ThirdUsersViewSet)
router.register(r'login', ThirdUsersLoginViewSet)
router.register(r'confirm', ConfirmLoginViewSet)
urlpatterns = [
    re_path('^index/static/.*$', static, name='static'),
    re_path('^index/(?P<file_name>[A-Za-z0-9]+)\.txt$', check_file, name='index'),
    re_path('^index/', index, name='index'),
]
urlpatterns += router.urls
