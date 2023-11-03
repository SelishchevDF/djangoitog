from django.urls import path
from .views import IndexView, registration_user, login_user, logout_user, add_recipe, my_recipes, all_recipes, redact_recipe, recipe

urlpatterns = [

    path('', IndexView.as_view(), name='index'),
    path('index/', IndexView.as_view(), name='index'),
    path('registration/', registration_user, name='registration'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add_recipe/', add_recipe, name='add_recipe'),
    path('my_recipes/', my_recipes, name='my_recipes'),
    path('all_recipes/', all_recipes, name='all_recipes'),
    path('redact_recipe/<int:id_recipe>/', redact_recipe, name='redact_recipe'),
    path('recipe/<int:id_recipe>/', recipe, name='recipe'),
    
]