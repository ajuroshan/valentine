from django.shortcuts import render, redirect
from django.http import HttpResponse
from home.models import *

GOLDEN_RATIO = 1.61803398875

# Create your views here.

def home_view(request):
    return HttpResponse(f"You are logged in as {request.user.username}")


def calculate_interest_score(interest_set1, interest_set2):
    common_interests = set(interest_set1) & set(interest_set2)
    return len(common_interests)

def calculate_age_score(age1, age2):
    age_difference = abs(age1 - age2)
    return GOLDEN_RATIO / (1 + age_difference)

def calculate_total_score(interest_score, age_score):
    return GOLDEN_RATIO * interest_score + age_score

def calculate_match_percentage(total_score, max_possible_score):
    return (total_score / max_possible_score) * 100

def match_users(request):
    male_applications = Applications.objects.filter(gender='male').exclude(male_match__isnull=False)
    female_applications = Applications.objects.filter(gender='female').exclude(female_match__isnull=False)

    max_possible_score = GOLDEN_RATIO * len(Interests.objects.all())

    for male in male_applications:
        best_female = None
        best_score = 0

        for female in female_applications:
            interest_score = calculate_interest_score(male.interests.all(), female.interests.all())
            age_score = calculate_age_score(male.age, female.age)
            total_score = calculate_total_score(interest_score, age_score)

            if total_score > best_score:
                best_score = total_score
                best_female = female

        if best_female:
            match_percentage = calculate_match_percentage(best_score, max_possible_score)
            match = Match.objects.create(
                male_application=male,
                female_application=best_female,
                age_score=age_score,
                interest_score=interest_score,
                total_score=best_score,
                match_percentage=match_percentage
            )
            return HttpResponse(f"Match created: {match}")

    return HttpResponse("No matches found.")



def match_view(request):
    user_match = Match.objects.filter(
        male_application__user=request.user
    ).select_related('female_application__user').first()

    if user_match:
        response_text = f"Your Match: {user_match.female_application.user.username} - Match Percentage: {user_match.match_percentage}%"
    else:
        response_text = "No match found."

    return HttpResponse(response_text)