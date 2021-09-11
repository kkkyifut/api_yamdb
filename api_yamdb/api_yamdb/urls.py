from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

handler404 = 'reviews.views.page_not_found'
handler500 = 'reviews.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redoc/', TemplateView.as_view(template_name='redoc.html'),
         name='redoc'),
    path('api/', include('api.urls', namespace='api-v1')),
    path('', include('reviews.urls', namespace='reviews')),
]
