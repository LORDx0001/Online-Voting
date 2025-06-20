from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


class Voter(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )
    phone_number = PhoneNumberField(region="UZ")
    password = models.CharField(max_length=128)
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"
    
class Election(models.Model):
    ELECTION_TYPES = [
        ('human', 'Human'),
        ('place', 'Place'),
        ('project', 'Project'),
        ('idea', 'Idea'),
    ]

    title = models.CharField(max_length=200)
    election_type = models.CharField(max_length=20, choices=ELECTION_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def candidate_types(self):
        valid_types = ['human', 'place', 'project', 'idea', 'other']
        if self.election.election_type not in valid_types:
            raise ValidationError("Invalid election type for candidate.")
        
    def vote_count(self):
        return self.vote_set.count()
    
    def __str__(self):
        return f"{self.name} ({self.election.title})"

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election')

    def __str__(self):
        return f"{self.voter} voted for {self.candidate} in {self.election}"
