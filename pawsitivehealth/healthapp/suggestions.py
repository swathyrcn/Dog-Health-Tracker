# In views.py or a separate file like suggestions.py

BREED_BASE_SUGGESTIONS = {
    'golden retriever': {
        'food': ["High-quality kibble", "Lean meats"],
        'treats': ["Carrot sticks", "Peanut butter Kong"],
        'supplements': ["Fish oil for coat & joints"],
    },
    'pug': {
        'food': ["Lower-calorie kibble", "Veggie mix-ins (carrots, peas)"],
        'treats': ["Low-fat treats", "Apple slices (no seeds)"],
        'supplements': ["Joint supplements (common for brachycephalic breeds)"],
    },
}

# Additional suggestions for different age ranges
AGE_SUGGESTIONS = {
    'puppy': {
        'food': ["Puppy formula kibble", "More frequent meals (3-4/day)"],
        'treats': ["Small, soft treats for training"],
        'supplements': ["Consider puppy multivitamin if vet-approved"],
    },
    'adult': {
        'food': ["Standard adult kibble (2 meals/day)"],
        'treats': ["Moderate treats", "Dental chews"],
        'supplements': [],
    },
    'senior': {
        'food': ["Senior kibble (joint support)"],
        'treats': ["Low-calorie treats", "Easier-to-chew items"],
        'supplements': ["Glucosamine/chondroitin", "Omega-3 for joints"],
    },
}

# Additional suggestions for weight categories
WEIGHT_SUGGESTIONS = {
    'underweight': {
        'food': ["High-calorie, nutrient-dense kibble", "Possibly more frequent meals"],
        'treats': ["Higher-calorie treats (peanut butter, cheese)"],
        'supplements': ["Vet consultation if significantly underweight"],
    },
    'normal': {
        'food': [],
        'treats': [],
        'supplements': [],
    },
    'overweight': {
        'food': ["Weight management kibble", "Controlled portions"],
        'treats': ["Low-fat treats, veggies"],
        'supplements': ["Joint supplements (excess weight can stress joints)"],
    },
}

def get_diet_suggestions(breed: str, age: int, weight: float):
    """
    Returns a dict with lists of recommended 'food', 'treats', and 'supplements'
    based on the dog's breed, age, and weight.
    """

    # 1) Start with an empty base
    recommendations = {
        'food': [],
        'treats': [],
        'supplements': [],
    }

    breed_lower = breed.lower() if breed else ""
    breed_suggestions = BREED_BASE_SUGGESTIONS.get(breed_lower, None)
    if breed_suggestions:
        # Merge breed's base suggestions
        recommendations['food'].extend(breed_suggestions['food'])
        recommendations['treats'].extend(breed_suggestions['treats'])
        recommendations['supplements'].extend(breed_suggestions['supplements'])

    # 2) Determine age category (puppy, adult, senior) as you see fit
    if age < 1:
        age_cat = 'puppy'
    elif age < 7:
        age_cat = 'adult'
    else:
        age_cat = 'senior'

    age_sugg = AGE_SUGGESTIONS.get(age_cat, None)
    if age_sugg:
        recommendations['food'].extend(age_sugg['food'])
        recommendations['treats'].extend(age_sugg['treats'])
        recommendations['supplements'].extend(age_sugg['supplements'])

    # 3) Determine weight category
    # For example, you might call a dog overweight if > 30kg, underweight if < 10kg, etc.
    # This is just a placeholder logic:
    if weight < 10:
        weight_cat = 'underweight'
    elif weight > 25:
        weight_cat = 'overweight'
    else:
        weight_cat = 'normal'

    weight_sugg = WEIGHT_SUGGESTIONS.get(weight_cat, None)
    if weight_sugg:
        recommendations['food'].extend(weight_sugg['food'])
        recommendations['treats'].extend(weight_sugg['treats'])
        recommendations['supplements'].extend(weight_sugg['supplements'])

    # 4) Optionally remove duplicates or refine:
    # Convert lists to sets & back if you want to avoid duplicates:
    recommendations['food'] = list(set(recommendations['food']))
    recommendations['treats'] = list(set(recommendations['treats']))
    recommendations['supplements'] = list(set(recommendations['supplements']))

    return recommendations
