from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from myapp import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.INDEX, name='index'),
    path('cab-list/', views.CAB, name='cab_list'),
    path('cab-detail/', views.CAB_DETAIL, name='cab-detail'),
    path('cab-booking/', views.CAB_BOOKING, name='cab-booking'),
    path('confirm/', views.CONFIRM, name='confirm'),
    path('calculate-fare/', views.calculate_fare, name='calculate-fare'),

    path('login/', views.LOGIN, name='login'),
    path('for-password/', views.PASSWORD, name='password'),
    path('profile/', views.PROFILE, name='profile'),
    path('', include('myapp.urls')),





]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)


