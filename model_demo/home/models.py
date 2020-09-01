from django.db import models
from django.contrib.auth.models import User

from datetime import date

class Restaurant(models.Model):
    name = models.TextField()
    address = models.TextField(blank=True, default='')
    url = models.URLField(blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{name} {user}".format(name=self.name, user=self.user.username)

    class Meta:
        # default ordering rule
        """ [var] -> ascending
            [-var]-> descending
        """
        ordering = ['name', 'user']

        """database table name
        """
        db_table = "restaurant"

class Dish(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True, default='')
    price = models.DecimalField('USD amount', max_digits=8, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __string__(self):
        return self.name

class Review(models.Model):
    RATING_CHOICE = ((1, 'one'), (2, 'two'), (3, 'three'))
    rating = models.PositiveSmallIntegerField('Rating', blank=False, default=3, choices=RATING_CHOICE)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    class Meta:
        """abstract class
        This model will then not be used to create any database table if abstract is True
        """
        abstract = True

class RestaurantReview(Review):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    def __str__(self):
        return "{} review".format(self.restaurant.name)