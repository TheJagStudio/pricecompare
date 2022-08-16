
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Cookie': 'PHPSESSID=bc1ffc3f210214de73d55aa404d1c101; csrf=b06efb174ea5180ef8ab5bf1a8fd2e89; fbcity=11736; fbtrack=fce8797023ed82c4514f216fad6830a5; fre=0; rd=1380000; zl=en; AWSALBTG=ujrNOFIbXZx1x1B8NaWKYlfh7DyUczbP69iTzCrXQUpqQ7vHEflWOhkkbNpPXMLcYlgPE1zy9QPNpkKrTl/5o9ajvtoCxq5zoyGUCOuDQ871ISA54T5xUJZHKkNlzoBANCPyCaRfXeVPmciIk+/UdgmMxfVZ6UYmqQgo2/LAWxOs; AWSALBTGCORS=ujrNOFIbXZx1x1B8NaWKYlfh7DyUczbP69iTzCrXQUpqQ7vHEflWOhkkbNpPXMLcYlgPE1zy9QPNpkKrTl/5o9ajvtoCxq5zoyGUCOuDQ871ISA54T5xUJZHKkNlzoBANCPyCaRfXeVPmciIk+/UdgmMxfVZ6UYmqQgo2/LAWxOs'
    }
    location = locationI
    resturant = resturantI.replace(" ", "%20")
    latitude = latitudeI
    longitude = longitudeI
    url = "https://www.zomato.com/webroutes/location/search?q=" + \
        location+"&lat="+latitude+"&lon="+longitude
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        data = response.json()["locationSuggestions"]
    except ValueError:
        print(response.text)
        print('Bad Data from Server. Response content is not valid JSON')
        return [["none", 0, "none", ""]]
    entity_id = str(data[0]["entity_id"])
    entity_type = str(data[0]["entity_type"])
    latitude = str(data[0]["entity_latitude"])
    longitude = str(data[0]["entity_longitude"])
    location = str(data[0]["entity_name"])
    place_id = str(data[0]["place"]["place_id"])
    place_type = str(data[0]["place"]["place_type"])
    place_name = str(data[0]["place"]["place_name"])
    cellId = str(data[0]["place"]["cell_id"])
    isOrderLocation = str(data[0]["is_order_location"])
    o2_serviceablity = str(data
                           [0]["place"]["o2_serviceablity"])
    try:
        userDefinedLatitude = str(
            data[0]["userDefinedLatitude"])
    except:
        userDefinedLatitude = "null"
    try:
        userDefinedLongitude = str(
            data[0]["userDefinedLongitude"])
    except:
        userDefinedLongitude = "null"
    url = "https://www.zomato.com/webroutes/location/get?lat="+latitude+"&lon="+longitude+"&entity_id="+entity_id + \
        "&entity_type="+entity_type+"&userDefinedLatitude="+userDefinedLatitude+"&userDefinedLongitude="+userDefinedLongitude+"&placeId="+place_id+"&placeType="+place_type+"&placeName=" + \
        place_name+"&cellId="+cellId+"&addressId=0&isOrderLocation="+isOrderLocation + \
        "&forceEntityName="+location+"&res_id=111989&o2Serviceable=" + \
        o2_serviceablity+"&pageType=restaurant&persist=true"
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        data = response.json()["locationDetails"]
    except ValueError:
        print('Bad Data from Server. Response content is not valid JSON')
        return [["none", 0, "none", ""]]
    entity_id = str(data["entityId"])
    entity_type = str(data["entityType"])
    cityId = str(data["cityId"])
    cityName = str(data["cityName"])
    placeId = str(data["placeId"])
    placeType = str(data["placeType"])
    cellId = str(data["cellId"])
    deliverySubzoneId = str(data["deliverySubzoneId"])
    orderLocationName = str(data["orderLocationName"])
    displayTitle = str(data["displayTitle"])
    o2Serviceable = str(data["o2Serviceable"])
    placeName = str(data["placeName"])
    isO2City = str(data["isO2City"])
    isO2OnlyCity = str(data["isO2OnlyCity"])
    otherRestaurantsUrl = str(data["otherRestaurantsUrl"])
    isOrderLocation = str(data["isOrderLocation"])
    latitude = str(data["latitude"])
    longitude = str(data["longitude"])
    entityName = str(data["entityName"])
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
    try:
        data = response.json()["results"]
    except ValueError:
        print('Bad Data from Server. Response content is not valid JSON')
    try:
        page_url = data[0]["order"]["actionInfo"]["clickUrl"]
    except:
        page_url = data[0]["actionInfo"]["clickUrl"]
    url = "https://www.zomato.com/webroutes/getPage?page_url="+page_url+"&isMobile=0"
    # print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        data = response.json()["page_data"]
    except ValueError:
        print('Bad Data from Server. Response content is not valid JSON')
        return [["none", 0, "none", ""]]
    # print(len(data["page_data"]["order"]["menuList"]["menus"]))
    foodArr = []
    for food in data["order"]["menuList"]["menus"]:
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
