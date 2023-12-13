let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            // Set the default country code, e.g., 'lt' for Lithuania
            componentRestrictions: { 'country': ['lt'] },
        }
    );

    // Specify the function to be called when a prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // Reset the input field or show an alert if the user did not select a prediction
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    } else {
        // console.log('place name =>', place.name);
    }

    // Get the address components and assign them to the fields
    var geocoder = new google.maps.Geocoder();
    var address = document.getElementById('id_address').value;

    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // Update values using jQuery
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address);

            // Loop through address components and assign other address data
            for (var i = 0; i < place.address_components.length; i++) {
                for (var j = 0; j < place.address_components[i].types.length; j++) {
                    // Get a country
                    if (place.address_components[i].types[j] == 'country') {
                        $('#id_country').val(place.address_components[i].long_name);
                    }
                    // Get a city
                    if (place.address_components[i].types[j] == 'locality') {
                        $('#id_city').val(place.address_components[i].long_name);
                    }
                }
            }
        }
    });
}
