import requests
from .log import logerr, loginfo

# Update location every 1 minute
def ping_location(Start_ip):
    ip_request = requests.get("https://get.geojs.io/v1/ip.json")
    my_ip = ip_request.json()["ip"]
    if my_ip != Start_ip:  # If IP changed, then show in console and change value
        loginfo(f"New IP Address: {my_ip}")
    else:
        my_ip = Start_ip
    geo_request_url = "https://get.geojs.io/v1/ip/geo/" + my_ip + ".json"
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()
    Lat_loc = geo_data["latitude"]
    Long_loc = geo_data["longitude"]
    loginfo(
        f"Current Location:\n\tLatitude - {Lat_loc}\n\tLongitude - {Long_loc}\n"
    )  # Print Location - Latitude and Longitude
    return my_ip, Lat_loc, Long_loc