from django.db import models

# Models of drScratch

class File(models.Model):
    filename = models.CharField(max_length=100)
    method = models.CharField(max_length=100)
    time = models.TextField()
    score = models.CharField(max_length=10)
    move = models.CharField(max_length=100)
    art = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    sound = models.CharField(max_length=100)
    control = models.CharField(max_length=100)
    operators = models.CharField(max_length=100)
    bonus = models.CharField(max_length=1000)

class Dashboard(models.Model):
	user = models.TextField()
	frelease = models.DateField()
	
class Activity(models.Model):
	text = models.TextField()
	date = models.DateField()

class Survey(models.Model):

    name = models.CharField(max_length=200)
    user = models.CharField(max_length=100)
    date = models.TextField()
    question1a = models.CharField(max_length=10)
    question1b = models.CharField(max_length=10)
    question2a = models.CharField(max_length=10)
    question2b = models.CharField(max_length=10)
    question2c = models.CharField(max_length=10)
    question2d = models.CharField(max_length=200)
    question3a = models.CharField(max_length=100)
    question3b = models.CharField(max_length=10)
    question3c = models.CharField(max_length=10)
    question4 = models.CharField(max_length=10)
    question5 = models.CharField(max_length=10)
    question6 = models.CharField(max_length=500)



	
