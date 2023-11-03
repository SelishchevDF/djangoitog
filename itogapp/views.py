import random
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from .forms import LoginForm, AddRecipeForm, RedactRecipeForm
from .models import Recipe, Recipe_category, Relationship_of_recipe_and_category

# Create your views here.

class IndexView(View):
    def get(self, request):
        context={}
        recipes = Recipe.objects.all()
        recipies_list = []
        for i in range(5):
            r=random.choice(recipes)
            recipies_list.append(r)
        context['recipes'] = recipies_list
        return render(request, 'itogapp/index.html', context)
    
def registration_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username, None, password)
            user.save()
            return render(request, 'itogapp/message.html', {'message': 'Пользователь добавлен'})
    else:
        form = UserCreationForm()
    return render(request, 'itogapp/registration.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()
            if user:
                if user.check_password(password):
                    login(request, user)
                    return redirect('/')
                else: 
                    return render(request, 'itogapp/message.html', {'message': 'Пароль неверный'})
            else: return render(request, 'itogapp/message.html', {'message': 'Пользователь не найден'})     
    else:
        form = LoginForm()
    return render(request, 'itogapp/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('/')

def add_recipe(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddRecipeForm(request.POST, request.FILES)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                description = form.cleaned_data.get('description')
                steps = form.cleaned_data.get('steps')
                cooking_time = form.cleaned_data.get('cooking_time')
                picture = form.cleaned_data.get('picture')
                category_name = form.cleaned_data.get('category_name')
                fs = FileSystemStorage()
                fs.save(picture.name, picture)
                category = Recipe_category.objects.filter(name=category_name).first()
                if category:
                    relation = Relationship_of_recipe_and_category.objects.filter(cat=category).first()
                    if not relation:
                        relation = Relationship_of_recipe_and_category.objects.create(cat=category)
                    recipe = Recipe.objects.create(name=name, description=description, steps=steps, cooking_time=cooking_time, picture=picture.name, author=request.user)
                    recipe.save()
                    relation.rec.add(recipe)
                    relation.save()
                else:
                    category = Recipe_category.objects.create(name=category_name, description="очень вкусно, наверное")
                    category.save()
                    relation = Relationship_of_recipe_and_category.objects.filter(cat=category).first()
                    if not relation:
                        relation = Relationship_of_recipe_and_category.objects.create(cat=category)
                    recipe = Recipe.objects.create(name=name, description=description, steps=steps, cooking_time=cooking_time, picture=picture.name, author=request.user)
                    recipe.save()
                    relation.rec.add(recipe)
                    relation.save()
                return render(request, 'itogapp/message.html', {'message': 'Рецепт добавлен'})
        else:
            form = AddRecipeForm()
        return render(request, 'itogapp/registration.html', {'form': form})
    else: 
        return render(request, 'itogapp/message.html', {'message': 'Пользователь не авторизован'})
    
def my_recipes(request):
    context={}
    context['recipes'] = Recipe.objects.filter(author=request.user).all()
    return render(request, 'itogapp/list.html', context)
    
    
def all_recipes(request):
    context={}
    context['recipes'] = Recipe.objects.all()
    return render(request, 'itogapp/list.html', context)

def recipe(request, id_recipe):
    context={}
    context['r'] = Recipe.objects.filter(pk=id_recipe).first()
    return render(request, 'itogapp/recipe.html', context)

def redact_recipe(request, id_recipe):
    if request.user.is_authenticated:
        recipe = Recipe.objects.filter(pk=id_recipe).first()
        if recipe.author == request.user:
            if request.method == 'POST':
                form = RedactRecipeForm(request.POST, request.FILES)
                if form.is_valid():
                    recipe.name = form.cleaned_data.get('name')
                    recipe.description = form.cleaned_data.get('description')
                    recipe.steps = form.cleaned_data.get('steps')
                    recipe.cooking_time = form.cleaned_data.get('cooking_time')
                    recipe.picture = form.cleaned_data.get('picture')
                    fs = FileSystemStorage()
                    fs.save(recipe.picture.name, recipe.picture)
                    recipe.save()
                    return render(request, 'itogapp/message.html', {'message': 'Рецепт изменен'})
            else:
                form = RedactRecipeForm()
            return render(request, 'itogapp/registration.html', {'form': form})
        else:
            return render(request, 'itogapp/message.html', {'message': 'У Вас нет права редактировать этот рецепт'}) 
    else: 
        return render(request, 'itogapp/message.html', {'message': 'Пользователь не авторизован'})
    
        