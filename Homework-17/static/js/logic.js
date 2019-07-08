var myMap = L.map("map", {
    center: [
        37.09, -95.71
    ],
    zoom: 5
});

var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
}).addTo(myMap);

var satellite = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
}).addTo(myMap);

var terrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
}).addTo(myMap);



var earthquakeData = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson";
earthquakeArray = [];

// Perform a GET request to the query URL
d3.json(earthquakeData, function(data) {
    function chooseColor(mag) {
        switch(true) {
            case mag > 5:
                return "#FF9633";
            case mag > 4:
                return "#FFBB33";
            case mag > 3:
                return "#FFE333";
            case mag > 2:
                return "#DAFF33";
            case mag > 1:
                return "#99FF33";
            default:
                return "#FF5233";
        }
    }
    function circleRadius(mag) {
        return mag * 4
    };
    function geojsonMarkerOptions(feature) {
        return {
            radius: circleRadius(feature.properties.mag),
            fillColor: chooseColor(feature.properties.mag),
            color: "black",
            weight: 0.5,
            opacity: 1,
            fillOpacity: 1
        }
    };

    L.geoJSON(data, {
        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng);
        },
        style: geojsonMarkerOptions,
        onEachFeature: function(feature, layer) {
          layer.bindPopup("<h3>" + feature.properties.place +
              "</h3><hr><h1>Magnitude: " + feature.properties.mag +  "</h1><hr><p>" + new Date(feature.properties.time) + "</p>");
        }
    }).addTo(myMap);
});
