import frappe
import requests

def get_context(context):
    source_doc = frappe.get_all('source', fields=['name1', 'address', 'lat', 'long'])[0]
    context.source_data = source_doc
    
import frappe
import requests
 
@frappe.whitelist(allow_guest=True)
def fetch_restaurants_with_distances():
    source_doc = frappe.get_all('source', fields=['lat', 'long'])[0]
    source_lat = source_doc['lat']
    source_lng = source_doc['long']

    restaurants = frappe.get_all('restaurants', fields=['restaurant_name', 'lat', 'long', 'location'])
    results = []
    
    for restaurant in restaurants:
        restaurant_lat = restaurant['lat']
        restaurant_lng = restaurant['long']
        _, distance_kilometers = get_route_distance(
            (source_lat, source_lng), 
            (restaurant_lat, restaurant_lng)
        )
        if distance_kilometers is not None:
            results.append({
                'name': restaurant['restaurant_name'],
                'lat': restaurant_lat,
                'long': restaurant_lng,
                'location': restaurant['location'],
                'distance': round(distance_kilometers, 1)
            })
    
    return results

def get_route_distance(coord1, coord2):
    url = f"http://localhost:5001/route/v1/driving/{coord1[1]},{coord1[0]};{coord2[1]},{coord2[0]}?overview=false"
    response = requests.get(url)
    data = response.json()
    if data['code'] == 'Ok':
        distance_meters = data['routes'][0]['distance']
        distance_kilometers = distance_meters / 1000
        return distance_meters, distance_kilometers
    else:
        print("Error: Unable to calculate the distance.")
        return None, None
