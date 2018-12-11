from django.db import models
import re
import bcrypt
from datetime import datetime

class UserManager(models.Manager):

    def regValidator(self, form):

        errors = []

        name = form['name']
        username = form['username'].lower()
        password = form['password']
        confirm_pw = form['confirm_pw']

        if not name:
            errors.append("Name is required.")
        elif len(name) < 3:
            errors.append("Name must be at least 3 characters.")
        elif not name.isalpha():
            errors.append("Name cannot contain numbers.")
        if not username:
            errors.append("Username is required.")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters.")
        else:
            users = User.objects.filter(username = username)
            if users:
                errors.append("Username already exists. Please login.")
        if not password:
            errors.append("Password is required.")
        elif len(password) < 8:
            errors.append("Password must have at least 8 characters.")
        if not confirm_pw:
            errors.append("Confirm password is required.")
        if password != confirm_pw:
            errors.append("Passwords must match.")

        if not errors:
            # save user in database
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(name=name, username=username, password=hash_pw)
            return (True, user)
        else:
            return (False, errors)


    def loginValidator(self, form):
        errors = []

        username = form['username'].lower()
        password = form['password']

        if not username:
            errors.append("Username is required.")
        else:
            users = User.objects.filter(username = username)
            if not users:
                errors.append("Username not in database. Please register.")
            else:
                user = users[0]
                if not bcrypt.checkpw(password.encode(), user.password.encode()):
                    errors.append("Password does not match password in database.")
        if not password:
            errors.append("Password is required.")

        if not errors:
            user = User.objects.get(username = username)
            return (True, user)
        else:
            return (False, errors)

class TripManager(models.Manager):
    def tripValidator(self, form, id):
        errors = []
        now = str(datetime.now())
        destination = form['destination']
        description = form['description']
        travel_start = form['travel_start']
        travel_end = form['travel_end']

        if not destination:
            errors.append("Destination is required.")
        if not description:
            errors.append("Description is required.")
        if not travel_start:
            errors.append("Travel start date is required.")
        elif travel_start < now:
            errors.append("Time travel has not been invented yet.")
        if not travel_end:
            errors.append("Travel end date is required.")
        elif travel_end < travel_start:
            errors.append("Why?")
        print(travel_start)
        if not errors:
            trip = Trip.objects.create(destination = destination, description = description, travel_start = travel_start, travel_end = travel_end, planner_id = id)
            return (True, trip)
        else:
            return (False, errors)

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # planned_trips (-> Trip)

    def __repr__(self):
        return "<User: {}>".format(self.name)

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    travel_start = models.DateField()
    travel_end = models.DateField()
    description = models.CharField(max_length=255)
    planner = models.ForeignKey(User, related_name="planned_trips")
    joiners = models.ManyToManyField(User, related_name="joined_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __repr__(self):
        return "<Trip: {}>".format(self.destination)
