from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tips/', views.tips, name='tips'),
    

    # Auth
    path('register/', views.user_register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # Dog management
    path('dogs/', views.dog_list, name='dog_list'),
    path('dogs/add/', views.add_dog, name='add_dog'),
    path('dogs/<int:dog_id>/edit/', views.edit_dog, name='edit_dog'),
    path('dogs/<int:dog_id>/delete/', views.delete_dog, name='delete_dog'),

    # Health Records
    path('dogs/<int:dog_id>/health-records/', views.health_records, name='health_records'),
    path('dogs/<int:dog_id>/diet-nutrition/', views.diet_nutrition, name='diet_nutrition'),
    path('dogs/<int:dog_id>/tips/', views.dog_tips, name='dog_tips'),
    path('tips/', views.tips_view, name='tips'),
    path('tips/<int:dog_id>/', views.dog_tips, name='dog_tips'),
    path('diet-nutrition/', views.diet_nutrition_overview, name='diet_nutrition_overview'),
    path('dogs/<int:dog_id>/activity-exercise/', views.activity_exercise, name='activity_exercise'),
    path('dogs/<int:dog_id>/vaccination-medication/', views.vaccination_medication, name='vaccination_medication'),
    path("dogs/<int:dog_id>/activity/", views.log_activity, name="log_activity"),
    path('dogs/<int:dog_id>/vaccinations/', views.vaccination_list, name='vaccination_list'),
    path('dogs/<int:dog_id>/add-vaccination/', views.add_vaccination, name='add_vaccination'),
    path('dogs/<int:dog_id>/medications/', views.medication_list, name='medication_list'),
    path('dogs/<int:dog_id>/add-medication/', views.add_medication, name='add_medication'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("dogs/<int:dog_id>/activity-exercise/", views.activity_and_tips, name="activity_exercise"),
    path('dogs/<int:dog_id>/activity/', views.activity_and_tips, name='activity_and_tips'),

]
