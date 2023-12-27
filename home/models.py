from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    campus = models.CharField(max_length=15 , choices = (('maincampus','maincampus'),('soe','soe')), blank = True)
    year = models.PositiveIntegerField(choices = ((1,1),(2,2),(3,3),(4,4),(5,5)),default = 0)
    match_with_same_year = models.BooleanField(default=False)
    match_with_same_campus = models.BooleanField(default=False)

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