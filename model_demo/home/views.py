from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import RestaurantReview, Restaurant

from random import randint

def create_comment():
    comment = ''

    for _ in range(randint(20, 100)):
        comment += chr(randint(0, ord('z')-ord('A')) + ord('A'))

    return comment

# Create your views here.
def create_review(request):
    # retrieve queryset object only by the id column
    user = User.objects.only('id').get(id=2)
    restaurant = Restaurant.objects.only('id').get(id=1)
    obj = RestaurantReview(comment=create_comment(), user=user, restaurant=restaurant)
    obj.save()

    return HttpResponse("")
