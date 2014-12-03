from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'womenTech.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^techCalendar/', include('techCalendar.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
