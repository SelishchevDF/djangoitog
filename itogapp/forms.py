from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    
class AddRecipeForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField()
    steps = forms.CharField()
    cooking_time = forms.CharField(max_length=100)
    picture = forms.ImageField()
    category_name = forms.CharField(max_length=100)
    
class RedactRecipeForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField()
    steps = forms.CharField()
    cooking_time = forms.CharField(max_length=100)
    picture = forms.ImageField()