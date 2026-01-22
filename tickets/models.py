from django.db import models

class Ticket(models.Model):
    description = models.TextField()
    category = models.CharField(max_length=50)
    priority = models.CharField(max_length=10)
    assigned_team = models.CharField(max_length=100)
    auto_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category

