from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User



#  Custom User Model 
class UsersData(AbstractUser):

    # User roles 
    ROLE_CHOICES = (
        (1, 'Admin'),
        (2, 'HR'),
        (3, 'Employee'),
    )

    # Stores the role of the user
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)

    # Stores bonus points 
    bonus_points = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Stores reward amount
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.username or 'User'} ({self.get_role_display()})"


# Model to store peer voting data
class PeerVoting(models.Model):
    
    # User who gives the vote
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='votes_given',
        on_delete=models.CASCADE
    )

    # User who receives the vote
    vote_for = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='votes_received',
        on_delete=models.CASCADE
    )

    # Vote 
    vote = models.PositiveIntegerField(default=0)

    # Month 
    month = models.CharField(max_length=30)

    
    def __str__(self):
        return f"{self.user} → {self.vote_for} | Score: {self.vote} ({self.month})"


#  Model to store performance data 
class Performance(models.Model):
    

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Total performance score 
    performance_score = models.PositiveIntegerField(default=0)

    # Month 
    month = models.CharField(max_length=30)

    # Stores employee ID 
    employee_id = models.CharField(max_length=30)


    def __str__(self):
        return f"{self.user} | {self.month} | Score: {self.performance_score}"


# Model to track user activities 
class ActivityLog(models.Model):

   
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Description of the action performed
    action = models.CharField(max_length=255)

    # Requested path/URL
    path = models.CharField(max_length=255)

    # HTTP method used (GET, POST, etc.)
    method = models.CharField(max_length=10)

    # IP 
    ip_address = models.GenericIPAddressField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{username} - {self.action} - {self.created_at}"


# Model to define reward score ranges
class Rewards(models.Model):

    # First score range and reward
    from_score_1 = models.PositiveIntegerField(default=0)
    to_score_1 = models.PositiveIntegerField(default=0)
    reward_amount_1 = models.PositiveIntegerField(default=0)

    # Second score range and reward
    from_score_2 = models.PositiveIntegerField(default=0)
    to_score_2 = models.PositiveIntegerField(default=0)
    reward_amount_2 = models.PositiveIntegerField(default=0)

    # Third score range and reward
    from_score_3 = models.PositiveIntegerField(default=0)
    to_score_3 = models.PositiveIntegerField(default=0)
    reward_amount_3 = models.PositiveIntegerField(default=0)

    # Fourth score range and reward
    from_score_4 = models.PositiveIntegerField(default=0)
    to_score_4 = models.PositiveIntegerField(default=0)
    reward_amount_4 = models.PositiveIntegerField(default=0)
