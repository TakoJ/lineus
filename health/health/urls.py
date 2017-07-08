
from django.conf.urls import url, include
from django.contrib import admin
# from fitness.admin import admin_site

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('fitness.urls')),
    url(r'^authentication/', include('authentication.urls', namespace='authentication')),
]
