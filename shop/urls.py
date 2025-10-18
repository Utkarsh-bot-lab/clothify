from django.contrib import admin
from django.urls import path, re_path
from core import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as media_serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]

# Serve user-uploaded media in development (DEBUG)
if settings.DEBUG:
    # normal helper
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # extra explicit fallback (works even if the helper gets skipped)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', media_serve, {'document_root': settings.MEDIA_ROOT}),
    ]