from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DogProfile, HealthRecord, DietPlan, MealLog, Vaccination, Medication

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DogProfileForm(forms.ModelForm):
    class Meta:
        model = DogProfile
        fields = ['name', 'breed', 'age', 'weight', 'disease', 'medications']

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['date', 'notes', 'report']

class DietPlanForm(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ['daily_calorie_goal', 'recommended_foods', 'recommended_supplements']

class MealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['date', 'meal_description', 'calories']

class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['name', 'last_given', 'frequency_days']

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'last_given', 'frequency_days']