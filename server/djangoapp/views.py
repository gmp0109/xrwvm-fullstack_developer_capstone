# Uncomment the required imports before adding the code

from .restapis import get_request, analyze_review_sentiments
# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})

    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email
    )

    login(request, user)

    return JsonResponse({"userName": username, "status": "Authenticated"})

#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})


def get_dealer_details(request, dealer_id):
    endpoint = "/fetchDealer/" + str(dealer_id)
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})


def get_dealer_reviews(request, dealer_id):
    endpoint = "/fetchReviews/dealer/" + str(dealer_id)
    reviews = get_request(endpoint)

    for review_detail in reviews:
        sentiment = analyze_review_sentiments(review_detail["review"])
        review_detail["sentiment"] = sentiment

    return JsonResponse({"status": 200, "reviews": reviews})

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
