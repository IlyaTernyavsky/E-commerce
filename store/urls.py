from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name = 'process_order'),

    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('register',views.register_view,name='register'),
    

] 
