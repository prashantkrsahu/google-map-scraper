$(document).ready(function () {

    var map;
    var lat_lng = [];
    var mapMarker = [];
    var locRadius = [];

    var search_input = document.getElementById('placeSearch');

    function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
            center: {
                lat: 28.658879,
                lng: 77.170129
            },
            zoom: 15
        });

        // Add marker on click with redius on google maps
        map.addListener('click', function (e) {
            console.log(e.latLng.lat(), e.latLng.lng());
            lat_lng.push([e.latLng.lat(), e.latLng.lng()]);
            placeMarkerAndPanTo(e.latLng, map);
            var cityCircle = new google.maps.Circle({
                strokeColor: '#FF0000',
                strokeOpacity: 0.8,
                strokeWeight: 1,
                fillColor: '#FF0000',
                fillOpacity: 0.25,
                map: map,
                center: e.latLng,
                radius: 200
            });
            locRadius.push(cityCircle);

        });

        // Place Search Autocomplete
        var autocomplete = new google.maps.places.Autocomplete(search_input);
        // var autocomplete = new google.maps.places.Autocomplete(search_input);
        autocomplete.bindTo('bounds', map);
        autocomplete.setFields(
            ['address_components', 'geometry', 'icon', 'name']);
        autocomplete.addListener('place_changed', function () {
            var place = autocomplete.getPlace();
            if (!place.geometry) {
                window.alert("No details available for input:" + place.name + "");
                return;
            }
            // If the place has a geometry, then present it on a map.
            if (place.geometry.viewport) {
                map.fitBounds(place.geometry.viewport);
                map.setZoom(15);
            } else {
                map.setCenter(place.geometry.location);
                map.setZoom(15);  // Why 17? Because it looks good.
            }
        });

        $("#clearMarker").click(function () {
            lat_lng = [];
            for (var i in mapMarker) {
                mapMarker[i].setMap(null);
                locRadius[i].setMap(null);
            }
        });
    }

    // Place marker to the map
    function placeMarkerAndPanTo(latLng, map) {
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            icon: "static/images/marker.png"
        });
        mapMarker.push(marker);
        map.panTo(latLng);
    }

    initMap();

    $("#scrapDataBtn").click(function () {
        var radius = $("#radius").val();
        var business_type = $("#businessType").val();
        var data = {"data": lat_lng, "radius": radius, "business_type": business_type};
        if (lat_lng.length == 0) {
            alert("Select place on the map.");
        } else {
            $.ajax({
                method: "POST",
                url: "api/latlng",
                data: JSON.stringify(data),
                dataType: 'json',
                beforeSend: function (data) {
                    $("#loader").css('display', 'block');
                },
                success: function (data) {
                    window.location = 'download';
                    $("#loader").css('display', 'none');
                },
                error: function (data) {
                    console.log("error data", data);
                    $("#loader").css('display', 'none');
                }

            });
        }
    });
});