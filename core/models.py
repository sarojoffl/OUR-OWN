from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('upcoming', 'Upcoming'),
    ]

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='portfolio/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    detail_url = models.URLField(blank=True)

    def __str__(self):
        return self.name
