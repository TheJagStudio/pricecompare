
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from mainApp.models import userHistory
# Create your views here.


def isalpha(word):
    letters_count = 0
    for i in word:
        if i.isalpha():
            letters_count += 1
    return letters_count


@csrf_exempt
def index(request):
    if request.method == 'POST':
        locationCorr = request.POST['locationCorr']
        if isalpha(locationCorr) > 0:
            url = "https://www.swiggy.com/dapi/misc/address-recommend?place_id="+locationCorr
            response = requests.request("GET", url)
            latitude = response.json(
            )["data"][0]["geometry"]["location"]["lat"]
            longitude = response.json(
            )["data"][0]["geometry"]["location"]["lng"]
            request.session["latitude"] = latitude
            request.session["longitude"] = longitude
            url = "https://www.swiggy.com/dapi/misc/address-recommend?latlng=" + \
                str(request.session.get("latitude"))+"%2C" + \
                str(request.session.get("longitude"))
            response = requests.request("GET", url)
            data = response.json()["data"][0]
            location = ["", ""]
            for i in data["address_components"]:
                if i["types"][0] == "locality":
                    location[0] = i["long_name"]
                else:
                    location[1] += i["long_name"] + ", "
            request.session["location"] = location
            url = "https://www.swiggy.com/dapi/restaurants/list/v5?lat=" + \
                str(latitude)+"&lng="+str(longitude) + \
                "&page_type=DESKTOP_WEB_LISTING"
            response = requests.request("GET", url)
            location = request.session.get("location")
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
            return render(request, "home.html", {"dataArr": response.json()["data"]["cards"], "location": location})
        else:
            latitude = locationCorr.split()[0]
            longitude = locationCorr.split()[1]
            request.session["latitude"] = latitude
            request.session["longitude"] = longitude
            url = "https://www.swiggy.com/dapi/misc/address-recommend?latlng=" + \
                str(request.session.get("latitude"))+"%2C" + \
                str(request.session.get("longitude"))
            response = requests.request("GET", url)
            data = response.json()["data"][0]
            location = ["", ""]
            for i in data["address_components"]:
                if i["types"][0] == "locality":
                    location[0] = i["long_name"]
                else:
                    location[1] += i["long_name"] + ", "
            request.session["location"] = location
            url = "https://www.swiggy.com/dapi/restaurants/list/v5?lat=" + \
                str(latitude)+"&lng="+str(longitude) + \
                "&page_type=DESKTOP_WEB_LISTING"
            response = requests.request("GET", url)
            location = request.session.get("location")
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
            return render(request, "home.html", {"dataArr": response.json()["data"]["cards"], "location": location})
    if("latitude" in request.session and "longitude" in request.session):
        url = "https://www.swiggy.com/dapi/restaurants/list/v5?lat=" + \
            str(request.session.get("latitude"))+"&lng="+str(request.session.get("longitude")) + \
            "&page_type=DESKTOP_WEB_LISTING"
        response = requests.request("GET", url)
        data = response.json()["data"]["cards"]
        location = request.session.get("location")
        return render(request, 'home.html', {"dataArr": data, "location": location})
    else:
        return redirect("/")


def comparision(request):
    if("latitude" in request.session and "longitude" in request.session):
        id = request.GET.get("id")
        url = "https://www.swiggy.com/dapi/menu/v4/full?lat="+str(request.session.get(
            "latitude"))+"&lng="+str(request.session.get("longitude"))+"&menuId="+str(id)
        response = requests.request("GET", url)
        data = response.json()["data"]
        location = request.session.get("location")
        menuD = data["menu"]["items"]
        menuArr = []
        for key in menuD:
            menuArr.append(menuD[key])
        return render(request, "comparision.html", {"dataArr": data, "menuArr": menuArr, "location": location})
    else:
        return redirect("/")


def search(request):
    url = "https://www.swiggy.com/dapi/restaurants/search/suggest?lat=" + \
        str(request.session.get("latitude"))+"&lng=" + \
        str(request.session.get("longitude"))+"&str=jiv&trackingId=undefined"
    response = requests.request("GET", url)
    data = response.json()["data"]["suggestions"]
    return render(request, 'search.html', {"dataArr": data, "location": request.session.get("location")})
