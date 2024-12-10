from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import include, path, reverse_lazy

urlpatterns = [
    path('profile/', include('django.contrib.auth.urls')),
    path('', include('audioconf.urls', namespace='audioconf')),
    path("admin/", admin.site.urls),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('audioconf:index'),
        ),
        name='registration',
    ),
]
