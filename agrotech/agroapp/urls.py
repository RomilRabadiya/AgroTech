from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),#Handle name="signup" requests and go to signup view IN VIEWS.PY  
    # URL is 'signup/' for only displaying signup page no other work in background

    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), 
    path('profile/', views.profile_view, name='profile'),
    path('scheme/', views.scheme_list, name='scheme_list'),
    

    path('yard_market/', views.product_list, name='product_list'),#At Home

    path('yard_market/add/', views.add_product, name='add_product'),#When user is administrator And add product IN product_list.html Button
    path('yard_market/order/<int:product_id>/', views.order_product, name='order_product'),#When Buy Product
    path('yard_market/update/<int:product_id>/', views.update_product, name='update_product'),#When Update Product by admin
    path('yard_market/delete/<int:product_id>/', views.delete_product, name='delete_product'),#When Delete Product by admin

    
    path('yard_market/order_list', views.user_orders, name='user_orders'),#When user is farmer And see his orders , Button in product_list.html
    path('yard_market/order_admin_list', views.all_user_orders, name='all_user_orders'),#When user is administrator And see all orders , Button in product_list.html
    

    path('yard_market/add_category/', views.manage_categories, name='add_category'), #For add category CLick By Add category Button in Navbar of Admin\
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'), #For delete category CLick By Delete category Button in Category List When Admin Add Category

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
