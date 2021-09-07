from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls import handler404, handler500

handler404 = 'reviews.views.page_not_found'
handler500 = 'reviews.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls', namespace='reviews')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/', include('api.urls')),
]
