from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .suggestions import get_diet_suggestions 



from .forms import UserRegisterForm, DogProfileForm, HealthRecordForm, VaccinationForm, MedicationForm
from .models import DogProfile, HealthRecord, DietPlan, ActivityLog, Vaccination, Medication

def home(request):
    """Homepage with the big hero section - 'Track Your Dog's Health'."""
    return render(request, 'healthapp/index.html')

def about(request):
    """About page."""
    return render(request, 'healthapp/about.html')

def tips(request):
    """Tips page."""
    return render(request, 'healthapp/tips.html')

def health_records(request, dog_id):
    dog = get_object_or_404(DogProfile, id=dog_id, owner=request.user)
    records = dog.health_records.all()
    if request.method == 'POST':
        form = HealthRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.dog = dog
            record.save()
            return redirect('health_records', dog_id=dog.id)
    else:
        form = HealthRecordForm()
    return render(request, 'healthapp/health_records.html', {
        'dog': dog,
        'records': records,
        'form': form
    })


def diet_nutrition(request, dog_id):
    dog = get_object_or_404(DogProfile, id=dog_id, owner=request.user)
    breed = dog.breed or ""
    age = dog.age or 0
    weight = dog.weight or 0

    suggestions = get_diet_suggestions(breed, age, weight)
    recommended_foods = suggestions.get('food', [])
    recommended_treats = suggestions.get('treats', [])
    recommended_supplements = suggestions.get('supplements', [])

    from math import pow
    daily_calories = 70 * pow(weight, 0.75) if weight > 0 else None

    return render(request, 'healthapp/diet_nutrition.html', {
        'dog': dog,
        'daily_calories': daily_calories,
        'recommended_foods': recommended_foods,
        'recommended_treats': recommended_treats,
        'recommended_supplements': recommended_supplements,
    })

def diet_nutrition_overview(request):
    """
    Shows a simple page with a list of the user's dogs, each linking to
    the dog-specific diet_nutrition page.
    """
    dogs = DogProfile.objects.filter(owner=request.user)
    return render(request, 'healthapp/diet_nutrition_overview.html', {'dogs': dogs})

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically authenticate and log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Because the form is valid
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to dog profiles
                return redirect('dog_list')
    else:
        form = UserRegisterForm()
    return render(request, 'healthapp/register.html', {'form': form})

from datetime import timedelta
from django.utils.timezone import now
from .models import DogProfile
@login_required
def tips_view(request):
    # Fetch all dogs created by the logged-in user
    dogs = DogProfile.objects.filter(owner=request.user)

    return render(request, 'healthapp/tips.html', {'dogs': dogs})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to dog profiles after login
            return redirect('dog_list')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'healthapp/login.html')

def logout_user(request):
    """Log out."""
    logout(request)
    return redirect('home')

@login_required
def dog_list(request):
    """List of all dogs for the logged-in user."""
    dogs = DogProfile.objects.filter(owner=request.user)
    return render(request, 'healthapp/dog_list.html', {'dogs': dogs})


@login_required
def add_dog(request):
    if request.method == 'POST':
        form = DogProfileForm(request.POST)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.owner = request.user  # Associate the dog with the logged-in user
            dog.save()
            return redirect('dog_list')
    else:
        form = DogProfileForm()
    return render(request, 'healthapp/add_dog.html', {'form': form})



@login_required
def edit_dog(request, dog_id):
    """Edit an existing dog profile."""
    dog = get_object_or_404(DogProfile, id=dog_id, owner=request.user)
    if request.method == 'POST':
        form = DogProfileForm(request.POST, instance=dog)
        if form.is_valid():
            form.save()
            return redirect('dog_list')
    else:
        form = DogProfileForm(instance=dog)
    return render(request, 'healthapp/edit_dog.html', {'form': form, 'dog': dog})

@login_required
def delete_dog(request, dog_id):
    """Delete dog profile."""
    dog = get_object_or_404(DogProfile, id=dog_id, owner=request.user)
    if request.method == 'POST':
        dog.delete()
        return redirect('dog_list')
    return render(request, 'healthapp/delete_dog.html', {'dog': dog})

@login_required
def health_records(request, dog_id):
    """List or add health records for a dog."""
    dog = get_object_or_404(DogProfile, id=dog_id, owner=request.user)
    records = dog.health_records.all()
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.dog = dog
            record.save()
            return redirect('health_records', dog_id=dog.id)
    else:
        form = HealthRecordForm()
    return render(request, 'healthapp/health_records.html', {
        'dog': dog,
        'records': records,
        'form': form
    })
    
def activity_exercise(request, dog_id):
    dog = get_object_or_404(DogProfile, id=dog_id)
    return render(request, 'healthapp/activity_exercise.html', {'dog': dog})

def vaccination_medication(request, dog_id):
    dog = get_object_or_404(DogProfile, id=dog_id)
    return render(request, 'healthapp/vaccination_medication.html', {'dog': dog})


def dog_tips(request, dog_id):
    # Fetch the dog's details
    dog = DogProfile.objects.get(id=dog_id)

    # Define extra tips and recommendations
    grooming_tips = {
        "bath": f"Bathe your {dog.breed} every {random.randint(7, 14)} days to keep its coat clean and healthy.",
        "brushing": f"Brush your dog's coat every {random.randint(2, 5)} days to prevent tangles and mats.",
        "ear_cleaning": f"Clean your dog's ears every {random.randint(10, 20)} days to prevent infections.",
        "nail_clipping": f"Clip your dog's nails every {random.randint(15, 30)} days to avoid discomfort.",
    }

    recommended_products = [
        f"{dog.breed}-specific shampoo",
        "Detangling spray",
        "Ear cleaner solution",
        "Nail clippers",
        "Dental chews for healthy teeth",
    ]

    # Shuffle the recommendations to make them dynamic
    random.shuffle(recommended_products)

    return render(request, 'healthapp/tips.html', {
        'dog': dog,
        'grooming_tips': grooming_tips,
        'recommended_products': recommended_products[:3]  # Show top 3 products
    })



def log_activity(request, dog_id):
    dog = get_object_or_404(DogProfile, id=dog_id)

    tips = {}  # To store tips for each category

    if request.method == "POST":
        # Capture input values
        walk_minutes = int(request.POST.get("walks", 0))
        playtime_minutes = int(request.POST.get("playtime", 0))
        mental_stimulation_minutes = int(request.POST.get("mental_stimulation", 0))

        # Save the activity log
        ActivityLog.objects.create(
            dog=dog,
            walk_minutes=walk_minutes,
            playtime_minutes=playtime_minutes,
            mental_stimulation_minutes=mental_stimulation_minutes,
        )

        # Generate tips based on the input
        tips["walks"] = generate_tips(walk_minutes, 30, 60)  # Ideal range: 30-60 minutes
        tips["playtime"] = generate_tips(playtime_minutes, 15, 45)  # Ideal range: 15-45 minutes
        tips["mental_stimulation"] = generate_tips(mental_stimulation_minutes, 10, 30)  # Ideal range: 10-30 minutes

    # Retrieve all activity logs for the dog
    activity_logs = ActivityLog.objects.filter(dog=dog).order_by('-date')

    # Render the page with the activity logs and tips
    return render(request, "healthapp/log_activity.html", {
        "dog": dog,
        "activity_logs": activity_logs,
        "tips": tips,
    })

def generate_tips(minutes, min_time, max_time):
    """
    Generate tips based on logged minutes compared to ideal range.
    """
    if minutes < min_time:
        return f"Too low. Try increasing to at least {min_time} minutes."
    elif minutes > max_time:
        return f"Too high. Reduce to no more than {max_time} minutes."
    else:
        return "Perfect! Maintain this level."



def activity_view(request, dog_id):
    
    dog = get_object_or_404(DogProfile, id=dog_id)
    
    # Define exercise suggestions for breeds
    exercise_suggestions_data = {
        "golden retriever": [
            "Daily walks for 30–60 minutes.",
            "Interactive playtime, such as fetch or tug-of-war.",
            "Mental stimulation with puzzle toys.",
            "Weekly visits to a dog park for socialization.",
            "Agility training for physically active breeds."
        ],
        "pug": [
            "Short daily walks (10–20 minutes).",
            "Indoor playtime with soft toys.",
            "Mental stimulation with treat puzzles.",
            "Avoid strenuous exercises due to their breathing issues."
        ],
        "labrador retriever": [
            "Daily runs or long walks.",
            "Swimming for muscle strength and low-impact exercise.",
            "Fetch with high-energy toys.",
            "Socialization at dog parks."
        ],
        # Add more breeds as needed
    }

    # Fetch suggestions for the dog's breed or provide a default
    exercise_suggestions = exercise_suggestions_data.get(
        dog.breed.lower(), ["General playtime and light walks."]
    )

    return render(request, 'healthapp/activity.html', {
        'dog': dog,
        'exercise_suggestions': exercise_suggestions,
    })

def vaccination_list(request, dog_id):
    dog = get_object_or_404(DogProfile, id=dog_id)
    vaccinations = dog.vaccinations.all()
    return render(request, 'healthapp/vaccination_list.html', {'dog': dog, 'vaccinations': vaccinations})

def add_vaccination(request, dog_id):
    dog = get_object_or_404(DogProfile, id=dog_id)
    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            vaccination = form.save(commit=False)
            vaccination.dog = dog
            vaccination.save()
            return redirect('vaccination_list', dog_id=dog.id)
    else:
        form = VaccinationForm()
    return render(request, 'healthapp/add_vaccination.html', {'form': form, 'dog': dog})

def medication_list(request, dog_id):
    dog = get_object_or_404(DogProfile, id=dog_id)
    medications = dog.medications.all()
    return render(request, 'healthapp/medication_list.html', {'dog': dog, 'medications': medications})

def add_medication(request, dog_id):
    dog = get_object_or_404(DogProfile, id=dog_id)
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save(commit=False)
            medication.dog = dog
            medication.save()
            return redirect('medication_list', dog_id=dog.id)
    else:
        form = MedicationForm()
    return render(request, 'healthapp/add_medication.html', {'form': form, 'dog': dog})

from datetime import date

def dashboard(request):
    dogs = DogProfile.objects.all()
    upcoming_vaccinations = []
    upcoming_medications = []

    for dog in dogs:
        for vaccination in dog.vaccinations.all():
            if vaccination.next_due_date() <= date.today() + timedelta(days=7):
                upcoming_vaccinations.append(vaccination)
        for medication in dog.medications.all():
            if medication.next_due_date() <= date.today() + timedelta(days=7):
                upcoming_medications.append(medication)

    return render(request, 'healthapp/dashboard.html', {
        'dogs': dogs,
        'upcoming_vaccinations': upcoming_vaccinations,
        'upcoming_medications': upcoming_medications,
    })
    
DEFAULT_ACTIVITIES = [
    "Daily walks for 30–60 minutes.",
    "Play fetch or tug-of-war to engage physically.",
    "Let your dog explore new environments during walks.",
    "Off-leash play in a secure, safe area.",
    "Interactive toys or puzzles to keep them engaged."
]

DEFAULT_MENTAL_STIMULATION = [
    "Teach your dog a new trick or command weekly.",
    "Hide treats around the house and let them find them.",
    "Use interactive feeding bowls or mats.",
    "Rotate toys regularly to keep your dog curious.",
    "Play hide-and-seek with your dog using toys or treats."
]

def activity_and_tips(request, dog_id):
    # Fetch the dog's profile
    dog = get_object_or_404(DogProfile, id=dog_id)

    # Provide default activities and tips for all dogs
    breed_info = {
        "activities": DEFAULT_ACTIVITIES,
        "mental_stimulation": DEFAULT_MENTAL_STIMULATION
    }

    return render(request, "healthapp/activity_exercise.html", {
        "dog": dog,
        "activities": breed_info["activities"],
        "mental_stimulation": breed_info["mental_stimulation"]
    })