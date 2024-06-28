import streamlit as st
from streamlit.components.v1 import html

# Function to generate HTML with Google Maps and geofencing logic
def generate_map_html(api_key, lat, lng, radius, user_lat=None, user_lng=None, simulate_movement=False):
    user_location_script = ""
    if user_lat is not None and user_lng is not None:
        user_location_script = f"""
            let userLocation = {{ lat: {user_lat}, lng: {user_lng} }};
            const userMarker = new google.maps.Marker({{
                position: userLocation,
                map: map,
                title: 'User Location'
            }});

            function checkGeofence() {{
                const isInsideGeofence = google.maps.geometry.spherical.computeDistanceBetween(
                    new google.maps.LatLng(userLocation),
                    geofence.getCenter()
                ) <= geofence.getRadius();

                if (isInsideGeofence) {{
                    alert("User has reached inside the geofence!");
                    return true;
                }}
                return false;
            }}

            function moveUser() {{
                const geofenceCenter = geofence.getCenter();
                const latStep = (geofenceCenter.lat() - userLocation.lat) / 50;
                const lngStep = (geofenceCenter.lng() - userLocation.lng) / 50;

                const moveInterval = setInterval(() => {{
                    userLocation = {{
                        lat: userLocation.lat + latStep,
                        lng: userLocation.lng + lngStep
                    }};
                    userMarker.setPosition(userLocation);

                    if (checkGeofence()) {{
                        clearInterval(moveInterval);
                    }}
                }}, 1000);
            }}

            { 'moveUser();' if simulate_movement else 'checkGeofence();' }
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Geofencing with Google Maps</title>
        <script src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=geometry"></script>
        <style>
            #map {{
                height: 400px;
                width: 100%;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            function initMap() {{
                const mapCenter = {{ lat: {lat}, lng: {lng} }};
                const geofenceCenter = {{ lat: {lat}, lng: {lng} }};
                const geofenceRadius = {radius};

                const map = new google.maps.Map(document.getElementById('map'), {{
                    zoom: 13,
                    center: mapCenter
                }});

                const geofence = new google.maps.Circle({{
                    strokeColor: '#FF0000',
                    strokeOpacity: 0.8,
                    strokeWeight: 2,
                    fillColor: '#FF0000',
                    fillOpacity: 0.35,
                    map: map,
                    center: geofenceCenter,
                    radius: geofenceRadius
                }});

                {user_location_script}
            }}
            window.onload = initMap;
        </script>
    </body>
    </html>
    """

# Streamlit app
st.title('Geofencing with Google Maps')

api_key = 'AIzaSyAfczM6HrvFXvDgRc7Sk9MYC2yXqYxEF78'
lat = st.number_input('Enter Geofence Center Latitude', value=52.4751549)
lng = st.number_input('Enter Geofence Center Longitude', value=-1.8870842)
radius = st.number_input('Enter Geofence Radius (meters)', value=1000.0)

user_lat = st.number_input('Enter User Latitude', value=52.4435823)
user_lng = st.number_input('Enter User Longitude', value=-1.897724)

simulate_movement = st.checkbox('Simulate User Movement')

if st.button('Show Map with Geofence'):
    map_html = generate_map_html(api_key, lat, lng, radius, user_lat, user_lng)
    html(map_html, height=450)

if st.button('Check User Position'):
    map_html = generate_map_html(api_key, lat, lng, radius, user_lat, user_lng)
    html(map_html, height=450)

if st.button('Simulate User Movement'):
    map_html = generate_map_html(api_key, lat, lng, radius, user_lat, user_lng, simulate_movement=True)
    html(map_html, height=450)
