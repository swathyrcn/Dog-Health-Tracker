from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class DogProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dogs')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    weight = models.FloatField(help_text="Weight in kilograms", blank=True, null=True)
    disease = models.CharField(max_length=255, blank=True, null=True)
    medications = models.CharField(max_length=255, blank=True, null=True)
    
    
    # You could also make disease/medications TextField if you expect longer entries.

    def __str__(self):
        return f"{self.name} ({self.breed})"

class DietPlan(models.Model):
    dog = models.OneToOneField(DogProfile, on_delete=models.CASCADE, related_name='diet_plan')
    daily_calorie_goal = models.FloatField(blank=True, null=True)
    recommended_foods = models.TextField(blank=True, null=True)
    recommended_supplements = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Diet Plan for {self.dog.name}"

class MealLog(models.Model):
    dog = models.ForeignKey(DogProfile, on_delete=models.CASCADE, related_name='meal_logs')
    date = models.DateField()
    meal_description = models.TextField()
    calories = models.FloatField()

    def __str__(self):
        return f"Meal on {self.date} for {self.dog.name}"

class HealthRecord(models.Model):
    dog = models.ForeignKey(DogProfile, on_delete=models.CASCADE, related_name='health_records')
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    report = models.FileField(upload_to='reports/', blank=True, null=True)
    def __str__(self):
        return f"Health Record for {self.dog.name} on {self.date}"
    
class ActivityLog(models.Model):
    dog = models.ForeignKey(DogProfile, on_delete=models.CASCADE, related_name="activities")
    date = models.DateField(auto_now_add=True)
    walk_minutes = models.PositiveIntegerField(default=0)
    playtime_minutes = models.PositiveIntegerField(default=0)
    mental_stimulation_minutes = models.PositiveIntegerField(default=0)
    
    def total_activity_time(self):
        return self.walks + self.playtime + self.mental_stimulation
    
    def __str__(self):
        return f"{self.dog.name} - {self.date}: Walks({self.walks} min), Playtime({self.playtime} min), Mental Stimulation({self.mental_stimulation} min)"

def log_activity(request, dog_id):
    
    dog = DogProfile.objects.get(id=dog_id)

    if request.method == "POST":
        # Capture input values
        walks = request.POST.get("walks", 0)
        playtime = request.POST.get("playtime", 0)
        mental_stimulation = request.POST.get("mental_stimulation", 0)

        # Save activity log
        ActivityLog.objects.create(
            dog=dog,
            walks=walks,
            playtime=playtime,
            mental_stimulation=mental_stimulation
        )

        # Fetch exercise suggestions based on breed
        exercise_suggestions = get_exercise_suggestions(dog.breed)

        # Render updated template
        return render(request, "healthapp/activity.html", {
            "dog": dog,
            "activity_logs": ActivityLog.objects.filter(dog=dog),
            "exercise_suggestions": exercise_suggestions
        })

    # Default exercise suggestions if no POST request
    exercise_suggestions = get_exercise_suggestions(dog.breed)
    return render(request, "healthapp/activity.html", {
        "dog": dog,
        "activity_logs": ActivityLog.objects.filter(dog=dog),
        "exercise_suggestions": exercise_suggestions
    })

def get_exercise_suggestions(breed):
    suggestions = {
        "golden retriever": [
            "Daily walks for 30–60 minutes",
            "Fetch games to stimulate their retrieval instincts",
            "Swimming and agility training",
            "Hiking for stamina and endurance"
        ],
        "pug": [
            "Short walks for 20–30 minutes",
            "Indoor play with lightweight toys",
            "Gentle fetch or tug-of-war games",
            "Interactive food puzzles for mental stimulation"
        ],
        # Add more breed-specific suggestions here
    }
    return suggestions.get(breed.lower(), ["General exercise recommendations available."])

class Vaccination(models.Model):
    dog = models.ForeignKey(DogProfile, on_delete=models.CASCADE, related_name="dog_vaccinations")
    name = models.CharField(max_length=100)
    last_given = models.DateField()
    frequency_days = models.IntegerField()

    def next_due_date(self):
        return self.last_given + timedelta(days=self.frequency_days)


class Medication(models.Model):
    dog = models.ForeignKey(DogProfile, on_delete=models.CASCADE, related_name="dog_medications")
    name = models.CharField(max_length=100)
    last_given = models.DateField()
    frequency_days = models.IntegerField()

    def next_due_date(self):
        return self.last_given + timedelta(days=self.frequency_days)