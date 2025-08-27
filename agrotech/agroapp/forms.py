from django import forms
from .models import User, FarmerProfile,AdministratorProfile 




from django.contrib.auth.forms import UserCreationForm
class SignupForm(UserCreationForm):         #By defaut UserCreationForm has username, password1, password2

    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)  # choices are defined in User model
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    zip_code = forms.CharField(max_length=10, required=False)
    farm_size = forms.FloatField(required=False)
    farm_type = forms.CharField(max_length=100, required=False)
    crops_grown = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), required=False)
    department = forms.CharField(max_length=255, required=False)
    admin_level = forms.IntegerField(required=False)


    class Meta:
        model = User # Using custom User model
        fields = ['username', 'email', 'password1', 'password2', 'role', 
                  'phone_number', 'address', 'city', 'state', 'zip_code'] # Common fields for all users

    def save(self, commit=True):    # Override save method to handle custom fields
        user = super().save(commit=False) # Get the unsaved User instance
        #username and password and email are already handled by UserCreationForm No need to set them again
        user.role = self.cleaned_data['role']   
        user.phone_number = self.cleaned_data['phone_number']
        user.address = self.cleaned_data['address']
        user.city = self.cleaned_data['city']
        user.state = self.cleaned_data['state']
        user.zip_code = self.cleaned_data['zip_code']

        if commit: #commit is True by default Then save the user instance to DB And create associated profile
            user.save() 
            self.create_role_profile(user)  # Ensure profiles are created safely

        return user

    def create_role_profile(self, user):
       
        role = user.role
        #This will change in Form of User instance
        #Check if profile already exists to avoid duplicates
        #Else create new profile based on role

        if role == 'farmer' and not FarmerProfile.objects.filter(user=user).exists():
            #Call FarmerProfile.objects.create() To CONSTRUCTOR with necessary fields
            #FarmerProfile Is a model defined in models.py
            FarmerProfile.objects.create(
                user=user,
                farm_size=self.cleaned_data.get('farm_size', 0),
                farm_type=self.cleaned_data.get('farm_type', ""),
                crops_grown=self.cleaned_data.get('crops_grown', "")
            )
       
        elif role == 'administrator' and not AdministratorProfile.objects.filter(user=user).exists():
            AdministratorProfile.objects.create(
                user=user,
                department=self.cleaned_data.get('department', ""),
                admin_level=self.cleaned_data.get('admin_level', 1)
            )
        

    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

       
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['role'].initial = user.role








from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    #Class based form for login page And is A form-control by Django
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))




#This form is for updating user profile information
class ProfileUpdateForm(forms.ModelForm):
    #Meta class to specify model and fields Is a ModelForm De
    class Meta:
        model = User
        fields = ['profile_picture', 'bio']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
        # Make fields optional
        help_texts = {
            'profile_picture': 'Optional',
            'bio': 'Optional',
        }
        

        
      





from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']

from .models import Category




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']