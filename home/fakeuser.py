import random
from faker import Faker
from django.contrib.auth.models import User
from home.models import Applications, Interests

fake = Faker()

# Create fake interests
interests = ['anime', 'movies', 'books', 'music', 'sports', 'coding', 'travel']
for interest in interests:
    Interests.objects.create(interset=interest, description=fake.text(20))

# Create fake male users
for _ in range(50):  # Adjust the number of users as needed
    username = fake.user_name()
    email = fake.email()
    password = "ajuaju"
    age = random.randint(18, 40)
    gender = 'male'

    user = User.objects.create_user(username=username, email=email, password=password)
    application = Applications.objects.create(user=user, age=age, gender=gender)

    # Add random interests to the application
    random_interests = random.sample(interests, random.randint(1, len(interests)))
    application.interests.add(*Interests.objects.filter(interset__in=random_interests))

# Create fake female users
for _ in range(50):  # Adjust the number of users as needed
    username = fake.user_name()
    email = fake.email()
    password = "ajuaju"
    age = random.randint(18, 40)
    gender = 'female'

    user = User.objects.create_user(username=username, email=email, password=password)
    application = Applications.objects.create(user=user, age=age, gender=gender)

    # Add random interests to the application
    random_interests = random.sample(interests, random.randint(1, len(interests)))
    application.interests.add(*Interests.objects.filter(interset__in=random_interests))
