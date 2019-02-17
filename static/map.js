
function updateMap(cur_usr_loc_lat, cur_usr_loc_lng, jsonArr) {

    // var testJsonArr = jsonArr;
    var testJsonArr = [{
        "locationName": "Aroma Joe’s",
        "address": "72 Main St, Durham, NH 03824",
        "lat": 43.135446,
        "long": -70.92806
    }, {
        "locationName": "Durham House of Pizza",
        "address": "40 Main St, Durham, NH 03824,",
        "lat": 43.13421,
        "long": -70.92554
    }, {
        "locationName": "University of New Hampshire InterOperability Laboratory",
        "address": "21 Madbury Rd #100, Durham, NH 03824",
        "lat": 43.13613,
        "long": -70.92556
    }];

    var markers = [];

    // create map
    var mapProp = {
        center: new google.maps.LatLng(cur_usr_loc_lat, cur_usr_loc_lng),
        zoom: 10,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

    // create infowindow (which will be used by markers)
    var infoWindow = new google.maps.InfoWindow();


    // marker creater function (acts as a closure for html parameter)
    function createMarker(options, html) {
        var marker = new google.maps.Marker(options);
        if (html) {
            google.maps.event.addListener(marker, "click", function () {
                infoWindow.setContent(html);
                infoWindow.open(options.map, this);
            });
        }

        return marker;
    }

    var labe1 = 1;





    function createMarkerHelper(lat, lon, jsonObj) {
        var marker1;
        if (jsonObj != null) {
            marker1 = createMarker({
                position: new google.maps.LatLng(lat, lon),
                map: map,
                animation: google.maps.Animation.DROP,
                label: {
                    text: "" + labe1++,
                    color: "#FFFFFF",
                    fontSize: "16px",
                    fontWeight: ""
                },

            }, "<h6>" + jsonObj.locationName + "</h6>");
        } else {
            // google's home icon for google+
            var icon = {
                path: "M20 40V28h8v12h10V24h6L24 6 4 24h6v16z",
                fillColor: '#4688F4',
                fillOpacity: 1,
                strokeWeight: 0,
                scale: 0.6,
                size: new google.maps.Size(24, 22), // scaled size
                scaledSize: new google.maps.Size(24, 22),
                origin: new google.maps.Point(0, 0), // origin
                anchor: new google.maps.Point(24, 44) // anchor
            }

            marker1 = createMarker({
                position: new google.maps.LatLng(lat, lon),
                map: map,
                //icon: icon,
            }, "<h1>Your Location</h1>");
        }

        markers.push(marker1);
    }

    createMarkerHelper(cur_usr_loc_lat, cur_usr_loc_lng, null);

    for (var i = 0; i < testJsonArr.length; i++) {
        var object = testJsonArr[i];
        createMarkerHelper(object.lat, object.long, object);

    }

    if (markers.length > 1) {
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < markers.length; i++) {
            bounds.extend(markers[i].getPosition());
        }

        map.fitBounds(bounds);
    }

    var request = {
        location: pyrmont,
        types: ['restaurant']
    };
}



function getUserLocation() {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;
            alert('Your current location is: ' + lat + ' ' + lng);
            var client = new HttpClient();

            $(function () {
                sayHi();
                function sayHi() {
                    $.ajax({
                        type: "GET",
                        url: "getMap",
                        success: function (data) {
                            console.log(data);
                            updateMap(lat, lng, data);
                        },
                    });
                }
            });

        }, function () {

        });
    } else {
        // Browser doesn't support Geolocation
    }
}
