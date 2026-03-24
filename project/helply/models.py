from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLE_CHOICES = [
        ('requester', 'Requester'),
        ('helper', 'Helper'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs_posted')
    helper = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs_accepted')
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    time_window = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    budget_negotiable = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} #{self.id}"


class Message(models.Model):
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Message #{self.id}"


class Review(models.Model):
    job = models.ForeignKey("Job", on_delete=models.CASCADE, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviews_given")
    reviewee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reviews_received")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review #{self.id}"


class Report(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reports_made")
    reported_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reports_received")
    reported_job = models.ForeignKey("Job", on_delete=models.SET_NULL, null=True, blank=True, related_name="reports")
    reason = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report #{self.id}"