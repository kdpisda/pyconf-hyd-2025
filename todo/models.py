from django.contrib.auth.models import User
from django.db import models


class List(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lists")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Priority(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"


class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=6, choices=Priority.choices, default=Priority.MEDIUM
    )
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["due_date", "-priority", "-created_at"]
