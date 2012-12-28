from django.conf.urls import include, patterns, url
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lugons.views.home', name='home'),
    # url(r'^lugons/', include('lugons.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^edit/(?P<filename>.*)/$', views.edit),
    url(r'^new/(?P<filename>.*)/$', views.new),
    url(r'^(?P<filename>.*)/$', views.article),
)
