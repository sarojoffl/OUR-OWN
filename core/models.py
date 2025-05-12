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

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.title

class Feature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='features/')

    def __str__(self):
        return self.title

class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.CharField(max_length=50)  # e.g. 'fa-home', 'fa-star'
    is_featured = models.BooleanField(default=False)
    features = models.TextField(help_text="One feature per line")

    def feature_list(self):
        return self.features.strip().split('\n')

    def __str__(self):
        return self.name

class About(models.Model):
    experience_years = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255)
    description = models.TextField()
    more_info = models.TextField()
    image = models.ImageField(upload_to='about/')
    why_choose_us = models.TextField(blank=True, null=True)

class Story(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField()

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question