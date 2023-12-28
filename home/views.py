from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from home.models import *
from home.forms import ApplicationsForm
from django.contrib import messages

GOLDEN_RATIO = 1.61803398875

# Create your views here.
def home_view(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        existing_application = Applications.objects.filter(user=user).first()
    else:
        existing_application = None

    if request.method == 'POST':
        # If the user has an existing application, retrieve it; otherwise, create a new one
        form = ApplicationsForm(request.POST, instance=existing_application)
        if form.is_valid():
            # Save the updated form data
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request,"Application Updated")
            return redirect('home_view')  # Redirect to the same view after saving
    else:
        # If the user has an existing application, use it as the initial data; otherwise, create a new form
        form = ApplicationsForm(instance=existing_application) if existing_application else ApplicationsForm()
        
    context = {'form': form}
    return render(request, 'home/homepage.html', context)


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
        pass

    return HttpResponse(response_text)


def test_function_for_test_branch():
    pass
    pass
    pass