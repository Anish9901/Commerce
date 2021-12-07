from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.db.models.base import Model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    return render(request,"auctions/index.html",{
            "listings": listings.objects.all(),
            "bids":bids.objects.all()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request):
    if request.method =="POST":
        item_name = request.POST["item_name"]
        description = request.POST["Description"]
        img_url = request.POST["img_url"]
        start_bid = request.POST["Price"]
        category = request.POST["category"]
        b = bids(current_price = start_bid)
        b.save()
        l = listings(lister = request.user ,item_name = item_name, description = description,url = img_url,category = category,price = b)
        l.save()
        return HttpResponseRedirect(reverse("index"))


    return render(request, "auctions/listing.html", {
        "check": 1
    })


def show(request,item_id):
    item_to_show = listings.objects.get(id = item_id)
    if(request.user.is_authenticated):
        if watchlist.objects.filter(users = request.user, item = item_id).exists():
            return render(request,"auctions/item.html",{
                "item": item_to_show,
                "watching":1
            })
    return render(request,"auctions/item.html",{
    "item": item_to_show,
    })
    
    
    
def watchlist_add(request,item_id): 
    x = listings.objects.get(id = item_id)   
    if request.method =="GET":
        if watchlist.objects.filter(users = request.user, item = x).exists() == False:
            w = watchlist.objects.get_or_create(users = request.user,item = x)
            #obj = watchlist.objects.get(users = request.user)
           
            #w.item.add(x)
            
            return render(request,"auctions/item.html",{
                "item":listings.objects.get(id = item_id),
                "watching":2
            })
        else:
            return render(request,"auctions/item.html",{
            "item":listings.objects.get(id = item_id),
            "watching": 1,
        })
    return render(request,"auctions/item.html",{
            "item":listings.objects.get(id = item_id),
            "watching": 0,
        })
    
def watchlist_remove(request,item_id):
    if request.method =="POST":
        a = watchlist.objects.filter(users = request.user)
        b = a.get(item = item_id)
        b.delete()
    return HttpResponseRedirect(reverse(show,kwargs={'item_id':item_id}))

def watchlist_viewing(request,user):
    return render(request,"auctions/watchlist.html",{
        "watch": watchlist.objects.filter(users = request.user),
        "name": request.user
    })


@login_required

def biding(request,item_id):
    l = []
    if request.method == "POST":
        amount = request.POST["bids_from_form"]
        x = float(amount)
        item = listings.objects.get(id = item_id)
        if len(l) == 0 and x >= item.price.current_price:
            item.price = x
            l.append(x)
        elif x > item.price.current_price:
            item.price = x
            l.append(x)
        else:
            if watchlist.objects.filter(users = request.user, item = item_id).exists():
                return render(request,"auctions/item.html",{
                "item": item,
                "errmsg": 1,
                "watching": 1
                })
            else:
                return render(request,"auctions/item.html",{
                "item": item,
                "errmsg": 1,
                "watching": 0
                })
            #return HttpResponseRedirect(reverse(show, kwargs={}))

