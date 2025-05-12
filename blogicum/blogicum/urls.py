from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView
from django.conf.urls import handler404, handler403, handler500
from django.conf.urls.static import static
from django.conf import settings
from blog.forms import BlogicumUserCreationForm


urlpatterns = [
    path('pages/', include('pages.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=BlogicumUserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
    path('', include('blog.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler500 = 'pages.views.permissions_denied'
handler404 = 'pages.views.page_not_found'
handler403 = 'pages.views.server_error'
