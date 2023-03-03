let map;

if (!latitude || !longitude) {
    latitude = 37.7749;
    longitude = -122.4194;
}

function initMap() {
  // Convert latitude and longitude strings to numbers
  var lat = parseFloat(latitude);
  var lng = parseFloat(longitude);

  // Create a new map centered on the latitude and longitude coordinates
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: lat, lng: lng },
    zoom: 13,
  });

  // Add a marker to the map at the latitude and longitude coordinates
  var marker = new google.maps.Marker({
    position: { lat: lat, lng: lng },
    map: map,
  });
}
window.initMap = initMap;