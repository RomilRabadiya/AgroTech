from django.shortcuts import render, redirect ,  get_object_or_404
from django.contrib.auth import login , logout 
from .models import Product, Order
from .forms import ProductForm
from .forms import SignupForm


def home(request):
    return render(request, 'home.html')


def product_list(request):
    products = Product.objects.all() #Add model Attribute to fetch all products
    return render(request, 'yard_market/product_list.html', {'products': products})


def signup(request):
    if request.method == 'POST': #When form is submitted via POST
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home') 
    else:#If the request method is GET When user first visits the signup page 
        form = SignupForm()


        #Passing form to the template allows:
        # Displaying the form fields.
        # Prefilling them (with initial values or previous input).
        # Showing form validation errors.
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request) 
    return redirect('home')  #




from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})







from django.templatetags.static import static

def scheme_list(request):
    schemes = [
        {
            'id': 1,
            'title': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
            'short_description': 'Crop insurance for farmers against natural disasters.',
            'full_description': 'PMFBY provides financial protection...',
            'image_url': static('scheme1.jpg'),  
        },
        {
            'id': 2,
            'title': 'Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)',
            'short_description': 'Income support to small and marginal farmers.',
            'full_description': 'PM-KISAN provides ₹6,000 per year...',
            'image_url': static('scheme2.jpeg'),
        },
        
    ]
    return render(request, 'scheme.html', {'schemes': schemes}) 




#All view For functionality of Buy Product By User(Farmer And Admin)    And    Add , Update ,Delete Product Bu Admin   And   Add,Delete Category Of product By Admin


#When user is farmer
@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)  #request.user is the currently logged-in user
  
    return render(request, 'yard_market/order_admin_list.html', {'orders': orders})


#When user is administrator And see all orders
@login_required
def all_user_orders(request):
   
    orders1 = Order.objects.all()
    return render(request, 'yard_market/order_admin_list.html', {'orders': orders1})



def product_list(request):
    products = Product.objects.all()
    return render(request, 'yard_market/product_list.html', {'products': products})



#WHen User Buy Product
@login_required
def order_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  #product_id is dynamic argument
    order = Order(user=request.user, product=product) #Make New Order Pass Product access by product_id and current user 
    order.save()
    return redirect('product_list')



#When user is administrator And add product And Button in product_list.html
@login_required
def add_product(request):
    if request.user.role != 'administrator':
        return redirect('home')
    
    #After submitting the form
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    
    #If the request method is GET When user first visits the add product page
    else:
        form = ProductForm()
    
    return render(request, 'yard_market/add_product.html', {'form': form})




from .models import Product
from .forms import ProductForm

@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Only admin can edit
    if request.user.role != "administrator":
        return redirect('product_list')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'yard_market/update_product.html', {'form': form})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.role != "administrator":
        return redirect('product_list')

    if request.method == "POST":
        product.delete()
        return redirect('product_list')

    return render(request, 'yard_market/delete_product.html', {'product': product})







from .models import Category
from .forms import CategoryForm  # Ensure you have this form


#For add category CLick By Add category Button in Navbar of Admin
@login_required
def manage_categories(request):
    if request.user.role != 'administrator':
        return redirect('home')

    categories = Category.objects.all()
    form = CategoryForm(request.POST or None)  # Prefill the form if submitted

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('add_category')  # Reload the same page to show updates

    return render(request, 'yard_market/add_category.html', {'form': form, 'categories': categories})

#For Delete category CLick By Add category Button in Navbar of Admin
@login_required
def delete_category(request, category_id):
    if request.user.role != 'administrator':
        return redirect('home')

    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('add_category')










def scheme_search(request):

    scheme = scheme_list.objects.filter()