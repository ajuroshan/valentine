from django.db import models
from django.contrib.auth.models import User

# Create your models here.

INTEREST_CHOICES = [
    ('anime', 'Anime'),
    ('movies', 'Movies'),
    ('books', 'Books'),
    # Add more interests as needed
]

class Interests(models.Model):
    interset = models.CharField(max_length=20,default='')
    description = models.CharField(max_length=20,default='')
    
    def __str__(self) -> str:
        return str(self.interset)

class Applications(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=1)
    gender = models.CharField(max_length=10, choices = (('male','male'),('female','female')),blank = True)
    interests = models.ManyToManyField(Interests)

    def __str__(self):
        return self.user.username
    
    
class Match(models.Model):
    male_application = models.OneToOneField('Applications', related_name='male_match', on_delete=models.CASCADE)
    female_application = models.OneToOneField('Applications', related_name='female_match', on_delete=models.CASCADE)
    match_date = models.DateTimeField(auto_now_add=True)
    age_score = models.FloatField(null=True, blank=True)
    interest_score = models.FloatField(null=True, blank=True)
    total_score = models.FloatField(null=True, blank=True)
    match_percentage = models.FloatField(null=True, blank=True)

    
    def __str__(self):
        return f"{self.male_application.user.username} matched with {self.female_application.user.username} with {self.match_percentage} % Match."