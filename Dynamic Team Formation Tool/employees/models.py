from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    skills = models.TextField() 
    roll = models.PositiveIntegerField()# Skills will be stored as a comma-separated string

    def __str__(self):
        return self.name

    
