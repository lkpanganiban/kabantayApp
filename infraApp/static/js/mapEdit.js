var map = L.map('map').setView([14.302988,121.081985], 7);

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',maxZoom: 15,
    }).addTo(map);

var bingGeocoder = new L.Control.BingGeocoder('API_KEY')
map.addControl(bingGeocoder);


var drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);
var drawControl = new L.Control.Draw({
	draw:{
		polygon:false,
		polyline:false,
		rectangle:false,
		circle:false
	},
    edit: {
        featureGroup: drawnItems,
    },

});
map.addControl(drawControl);
map.on('draw:created', function (e) {
    var type = e.layerType,
        layer = e.layer;

    if (type === 'marker') {
        // Do marker specific actions
    }

    // Do whatever else you need to. (save to db, add to map etc)
    map.addLayer(layer);

    var latitude = layer.getLatLng().lat;
    $("#latitude").val(latitude)
    var longitude = layer.getLatLng().lng;
    $("#longitude").val(longitude)
	 

});

