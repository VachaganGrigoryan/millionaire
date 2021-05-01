"""millionaire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

from django.conf import settings
from django.conf.urls.static import static
"""

from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name='home'),
    path('404/', accounts_views.handle_404, name="handle-404"),
    path('login/', LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', accounts_views.signup, name='signup'),
    path('millionaire/', include('quiz.urls')),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
