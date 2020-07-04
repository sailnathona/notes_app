from django.contrib import admin
from django.urls import path, include
from notes.views import index, example, dashboard, dologout
# or do
# from notes.views import *
# but better to enumerate them

from tastypie.api import Api
from .models import NoteResource

v1_api = Api(api_name='v1')
v1_api.register(NoteResource())


# note these are notes app urls
# look at appsuite/urls.py also!
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path(url(r’^notes/‘, include('notes.urls'))),
    path('index/', index, name='index'),
    path('example/', example, name='example'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', dologout, name='logout'),
    path('api/', include(v1_api.urls)),
]
