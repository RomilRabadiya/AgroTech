from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), 
    path('profile/', views.profile_view, name='profile'),
    path('scheme/', views.scheme_list, name='scheme_list'),
    
    path('yard_market/', views.product_list, name='product_list'),
    path('yard_market/add/', views.add_product, name='add_product'),
    path('yard_market/order/<int:product_id>/', views.order_product, name='order_product'),
    path('yard_market/add_category/', views.manage_categories, name='add_category'),
    path('yard_market/update/<int:product_id>/', views.update_product, name='update_product'),
    path('yard_market/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('yard_market/order_list', views.user_orders, name='user_orders'),
    path('yard_market/order_admin_list', views.all_user_orders, name='all_user_orders'),
    
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
