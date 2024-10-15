# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
# from scalable_chat_app.scalable_chat_app import settings
# from .views import index  # Ensure you include the index view
from django.conf.urls.static import static

from app import views
urlpatterns = [
    # path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'), 
    # path('register/', views.register, name='register'),  # Registration page
    # path('home/', views.home, name='home'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # other paths...

    path('', views.home, name='home'),  # Home page after login
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)