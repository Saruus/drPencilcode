from django.db import models

# Models of drScratch

class File(models.Model):
    filename = models.CharField(max_length=100)
    method = models.CharField(max_length=100)
    time = models.TextField()
    move = models.CharField(max_length=100)
    art = models.CharField(max_length=100)
    text = models.CharField(max_length=100)
    sound = models.CharField(max_length=100)
    control = models.CharField(max_length=100)
    operators = models.CharField(max_length=100)

class Dashboard(models.Model):
	user = models.TextField()
	frelease = models.DateField()

class Project(models.Model):
	name = models.TextField()
	version = models.IntegerField()
	score = models.IntegerField()
	level = models.TextField()
	path = models.TextField()
	fupdate = models.TextField()
	dashboard = models.ForeignKey(Dashboard)
	
class Attribute(models.Model):
	myproject = models.ForeignKey(Project)
	character = models.TextField()
	orientation = models.IntegerField()
	position = models.IntegerField()
	costume = models.IntegerField()
	visibility = models.IntegerField()
	size = models.IntegerField()

class Dead(models.Model):
	myproject = models.ForeignKey(Project)
	character = models.TextField()
	blocks = models.IntegerField()

class Duplicate(models.Model):
	myproject = models.ForeignKey(Project)
	numduplicates = models.IntegerField()

class Sprite(models.Model):
	myproject = models.ForeignKey(Project)
	character = models.TextField()

class Mastery(models.Model):
	myproject = models.ForeignKey(Project)
	move = models.CharField(max_length=100)
	art = models.CharField(max_length=100)
	text = models.CharField(max_length=100)
	sound = models.CharField(max_length=100)
	control = models.CharField(max_length=100)
	operators = models.CharField(max_length=100)

class Comment(models.Model):
	user = models.TextField()
	text = models.TextField()
	date = models.DateField()

class Activity(models.Model):
	text = models.TextField()
	date = models.DateField()

class Survey(models.Model):
	question1 = models.CharField(max_length=50)
	#question2 = models.CharField(max_length=10)
	#question3 = models.CharField(max_length=10)



	
