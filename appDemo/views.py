import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from mainApp.models import userHistory
# Create your views here.


@csrf_exempt
def searchResults(request):
    input = request.GET['input']
    DataType = request.GET['DataType']
    url = "https://www.swiggy.com/dapi/restaurants/search/v3?lat=" + str(request.session.get("latitude"))+"&lng=" + str(request.session.get(
        "longitude"))+"&str="+input+"&sldEnabled=false&trackingId=undefined&submitAction=ENTER&queryUniqueId=6e7a6ede-adda-2379-3c91-2d7f69426667&selectedPLTab="+DataType
    response = requests.request("GET", url)
    try:
        if DataType == "DISH":
            data = response.json()[
                "data"]["cards"][0]["groupedCard"]["cardGroupMap"][DataType]["cards"]
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            dataArr = response.json(
            )["data"]["cards"][0]["groupedCard"]["cardGroupMap"][DataType]["cards"]
            return HttpResponse(json.dumps(dataArr), content_type="application/json")
    except:
        return HttpResponse("No Results Found")


@csrf_exempt
def locToLoc(request):
    pid = request.GET['pid']
    url = "https://www.swiggy.com/dapi/misc/address-recommend?place_id="+pid
    response = requests.request("GET", url)
    data = response.json()["data"][0]
    location = ["", ""]
    for i in data["address_components"]:
        if i["types"][0] == "locality":
            location[0] = i["long_name"]
        else:
            location[1] += i["long_name"] + ", "
    request.session["location"] = location
    request.session["latitude"] = data["geometry"]["location"]["lat"]
    request.session["longitude"] = data["geometry"]["location"]["lng"]
    if(request.user.is_authenticated):
        userh = userHistory.objects.filter(user=request.user).first()

        if(userh == None):
            uh = userHistory()
            uh.user = request.user
            uh.lh = [request.session.get("latitude"),
                     request.session.get("longitude")]
            uh.save()
        else:
            if [request.session.get("latitude"), request.session.get("longitude")] in userh.lh["data"]:
                pass
            else:
                arr = list(userh.lh["data"])
                tempArr = [request.session.get(
                    "latitude"), request.session.get("longitude")]
                arr.append(tempArr)
                userh.lh = {"data": arr}
                userh.save()

    return HttpResponse(json.dumps(location), content_type="application/json")


def index(request):
    if request.user.is_authenticated:
        print(request.session.get("latitude"))
    if request.session.get("latitude") == None or request.session.get("longitude") == None:
        return render(request, "index.html")
    else:
        return redirect("/main/")


def signin(request):
    if request.method == 'POST':
        userEmail = request.POST['userMail']
        pass1 = request.POST['userPass']

        user = authenticate(username=userEmail, password=pass1)

        if user is not None:
            login(request, user)
            request.session["name"] = request.user.first_name
            fname = user.first_name
            context = {'username': fname}
            return redirect("/main/")
            # messages.success(request, "Logged In Sucessfully!!")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect("/")
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST['userName']
        phone = request.POST['userPhone']
        email = request.POST['userMail']
        pass1 = request.POST['userPass']

        if User.objects.filter(username=username):
            messages.error(
                request, "Username already exist! Please try some other username.")
            return render(request, "register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return render(request, "register.html")

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return render(request, "register.html")

        myuser = User.objects.create_user(username, email, phone, pass1)

        # myuser.is_active = False
        myuser.is_active = True
        myuser.save()
        user = authenticate(username=email, password=pass1)
        login(request, user)
        request.session["name"] = request.user.first_name
        fname = user.first_name
        return redirect("/")
    return render(request, "register.html")


@csrf_exempt
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_signin')


@csrf_exempt
def loactionFinder(request):
    input = request.GET['location']
    url = "https://www.swiggy.com/dapi/misc/place-autocomplete?input="+input
    response = requests.request("GET", url)
    return HttpResponse(response.text, content_type="application/json")
