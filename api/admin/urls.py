from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('blog/',include('api.admin.blog.urls')),
    path('common/',include('api.admin.common.urls')),
    path('users/', include('api.admin.users.urls')),
    path('storages/', include('api.admin.storages.urls')),
    path('testmedia/', include('api.admin.testmedia.urls'),)
    # path('testing/',include('api.testing.urls')),
]
