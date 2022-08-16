
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


def zomatoData(locationI, resturantI, latitudeI, longitudeI):
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }
    location = locationI
    resturant = resturantI.replace(" ", "%20")
    latitude = latitudeI
    longitude = longitudeI
    url = "https://www.zomato.com/webroutes/location/search?q=" + \
        location+"&lat="+latitude+"&lon="+longitude
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    entity_id = str(data["locationSuggestions"][0]["entity_id"])
    entity_type = str(data["locationSuggestions"][0]["entity_type"])
    latitude = str(data["locationSuggestions"][0]["entity_latitude"])
    longitude = str(data["locationSuggestions"][0]["entity_longitude"])
    location = str(data["locationSuggestions"][0]["entity_name"])
    place_id = str(data["locationSuggestions"][0]["place"]["place_id"])
    place_type = str(data["locationSuggestions"][0]["place"]["place_type"])
    place_name = str(data["locationSuggestions"][0]["place"]["place_name"])
    cellId = str(data["locationSuggestions"][0]["place"]["cell_id"])
    isOrderLocation = str(data["locationSuggestions"][0]["is_order_location"])
    o2_serviceablity = str(data["locationSuggestions"]
                           [0]["place"]["o2_serviceablity"])
    delivery_subzone_id = str(
        data["locationSuggestions"][0]["delivery_subzone_id"])
    try:
        userDefinedLatitude = str(
            data["locationSuggestions"][0]["userDefinedLatitude"])
    except:
        userDefinedLatitude = "null"
    try:
        userDefinedLongitude = str(
            data["locationSuggestions"][0]["userDefinedLongitude"])
    except:
        userDefinedLongitude = "null"
    url = "https://www.zomato.com/webroutes/location/get?lat="+latitude+"&lon="+longitude+"&entity_id="+entity_id + \
        "&entity_type="+entity_type+"&userDefinedLatitude="+userDefinedLatitude+"&userDefinedLongitude="+userDefinedLongitude+"&placeId="+place_id+"&placeType="+place_type+"&placeName=" + \
        place_name+"&cellId="+cellId+"&addressId=0&isOrderLocation="+isOrderLocation + \
        "&forceEntityName="+location+"&res_id=111989&o2Serviceable=" + \
        o2_serviceablity+"&pageType=restaurant&persist=true"
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    entity_id = str(data["locationDetails"]["entityId"])
    entity_type = str(data["locationDetails"]["entityType"])
    cityId = str(data["locationDetails"]["cityId"])
    cityName = str(data["locationDetails"]["cityName"])
    placeId = str(data["locationDetails"]["placeId"])
    placeType = str(data["locationDetails"]["placeType"])
    cellId = str(data["locationDetails"]["cellId"])
    deliverySubzoneId = str(data["locationDetails"]["deliverySubzoneId"])
    orderLocationName = str(data["locationDetails"]["orderLocationName"])
    displayTitle = str(data["locationDetails"]["displayTitle"])
    o2Serviceable = str(data["locationDetails"]["o2Serviceable"])
    placeName = str(data["locationDetails"]["placeName"])
    isO2City = str(data["locationDetails"]["isO2City"])
    isO2OnlyCity = str(data["locationDetails"]["isO2OnlyCity"])
    otherRestaurantsUrl = str(data["locationDetails"]["otherRestaurantsUrl"])
    isOrderLocation = str(data["locationDetails"]["isOrderLocation"])
    latitude = str(data["locationDetails"]["latitude"])
    longitude = str(data["locationDetails"]["longitude"])
    entityName = str(data["locationDetails"]["entityName"])
    if userDefinedLatitude == "null":
        userDefinedLatitude = "0"
    if userDefinedLongitude == "null":
        userDefinedLongitude = "0"
    url = "https://www.zomato.com/webroutes/search/autoSuggest?addressId=0&entityId=" + entity_id + "&entityType="+entity_type+"&locationType=&isOrderLocation=" + \
        isOrderLocation+"&cityId="+cityId+"&latitude="+latitude+"&longitude="+longitude+"&userDefinedLatitude="+userDefinedLatitude+"&userDefinedLongitude="+userDefinedLongitude + \
        "&entityName="+entityName+"&orderLocationName="+orderLocationName+"&cityName="+cityName+"&countryId=1&countryName=India&displayTitle="+displayTitle + \
        "&o2Serviceable="+o2Serviceable+"&placeId="+placeId+"&cellId="+cellId+"&deliverySubzoneId="+deliverySubzoneId+"&placeType="+placeType+"&placeName="+placeName + \
        "&isO2City="+isO2City+"&fetchFromGoogle=true&fetchedFromCookie=false&&isO2OnlyCity="+isO2OnlyCity+"&addressBlocker=0&&otherRestaurantsUrl="+otherRestaurantsUrl+"&q=" + \
        resturant+"&context=order&searchMetadata={}"

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    try:
        page_url = data["results"][0]["order"]["actionInfo"]["clickUrl"]
    except:
        page_url = data["results"][0]["actionInfo"]["clickUrl"]
    url = "https://www.zomato.com/webroutes/getPage?page_url="+page_url+"&isMobile=0"
    # print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    # print(len(data["page_data"]["order"]["menuList"]["menus"]))
    foodArr = []
    for food in data["page_data"]["order"]["menuList"]["menus"]:
        for i in range(0, len(food["menu"]["categories"])):
            for j in range(0, len(food["menu"]["categories"][i]["category"]["items"])):
                name = food["menu"]["categories"][i]["category"]["items"][j]["item"]["name"]
                price = food["menu"]["categories"][i]["category"]["items"][j]["item"]["default_price"]
                desc = food["menu"]["categories"][i]["category"]["items"][j]["item"]["desc"]
                try:
                    imageUrl = food["menu"]["categories"][i]["category"]["items"][j]["item"]["item_image_url"]
                except:
                    imageUrl = ""
                if [name, price, desc, imageUrl] not in foodArr:
                    foodArr.append([name, price, desc, imageUrl])
    return foodArr


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
            name = menuD[key]["name"]
            try:
                price = int(menuD[key]["price"]/100)
            except:
                price = "-"
            try:
                description = menuD[key]["description"]
            except:
                description = ""
            try:
                imageId = menuD[key]["cloudinaryImageId"]
            except:
                imageId = "-"
            menuArr.append([name, price, description, imageId])
        zData = zomatoData((location[0]+" "+location[1].split(",")[0]).replace(" ", "%20"), data["name"], str(
            request.session.get("latitude")), str(request.session.get("longitude")))
        finalData = []
        zfinalleftData = []
        sfinalleftData = []
        zdataLeft = []
        sdataLeft = []
        for i in range(0, len(menuArr)):
            for j in range(0, len(zData)):
                if menuArr[i][0].replace(" ", "").replace("\xa0", "").lower() == zData[j][0].replace(" ", "").replace("\xa0", "").lower():
                    finalData.append([[menuArr[i][0], menuArr[i][1], menuArr[i][2], menuArr[i][3]], [
                                     zData[j][0], zData[j][1], zData[j][2], zData[j][3]]])
                    break
                else:
                    if [menuArr[i][0], menuArr[i][1], menuArr[i][2], menuArr[i][3]] not in sdataLeft:
                        sdataLeft.append(
                            [menuArr[i][0], menuArr[i][1], menuArr[i][2], menuArr[i][3]])
                    if [zData[j][0], zData[j][1], zData[j][2], zData[j][3]] not in zdataLeft:
                        zdataLeft.append(
                            [zData[j][0], zData[j][1], zData[j][2], zData[j][3]])
        for i in range(0, len(sdataLeft)):
            flag = 0
            for j in range(0, len(finalData)):
                if sdataLeft[i][0] == finalData[j][0][0]:
                    flag = 1
                    break
            if flag == 0:
                sfinalleftData.append([sdataLeft[i], 0])
        for i in range(0, len(zdataLeft)):
            flag = 0
            for j in range(0, len(finalData)):
                if zdataLeft[i][0] == finalData[j][1][0]:
                    flag = 1
                    break
            if flag == 0:
                zfinalleftData.append([0, zdataLeft[i]])
        return render(request, "comparision.html", {"dataArr": data, "finalData": finalData, "zfinalleftData": zfinalleftData, "sfinalleftData": sfinalleftData, "location": location})
    else:
        return redirect("/")


def search(request):
    url = "https://www.swiggy.com/dapi/restaurants/search/suggest?lat=" + str(request.session.get(
        "latitude"))+"&lng=" + str(request.session.get("longitude"))+"&str=jiv&trackingId=undefined"
    response = requests.request("GET", url)
    data = response.json()["data"]["suggestions"]
    return render(request, 'search.html', {"dataArr": data, "location": request.session.get("location")})
