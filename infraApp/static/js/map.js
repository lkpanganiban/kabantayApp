var streets = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',maxZoom: 15,
    });

var satellite = L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpeg', {
            attribution: 'Tiles by <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            subdomains: '1234'
        }); 

var map = L.map('map',{
    center:[12.9966338,122.2119],
    zoom:6,
    layers:[streets]
    });


//Extending Popup class

var CustomPop = L.Popup.extend({

    options: {
        closeButton:true,
        className:'pop',
        zoomAnimation:false
    },

    _initLayout: function () {
        var prefix = 'leaflet-popup',
            container = this._container = L.DomUtil.create('div',
            prefix + ' ' + (this.options.className || '') +
            ' leaflet-zoom-' + (this._zoomAnimated ? 'animated' : 'hide'));

        if (this.options.closeButton) {
            var closeButton = this._closeButton = L.DomUtil.create('a', prefix + '-close-button', container);
            closeButton.href = '#close';
            closeButton.innerHTML = '&#215;';

            L.DomEvent.on(closeButton, 'click', this._onCloseButtonClick, this);
        }

        var wrapper = this._wrapper = L.DomUtil.create('div', 'pop', container);
        this._contentNode = L.DomUtil.create('div', 'content', wrapper);

        L.DomEvent
            .disableClickPropagation(wrapper)
            .disableScrollPropagation(this._contentNode)
            .on(wrapper, 'contextmenu', L.DomEvent.stopPropagation);

    }

}); 

var data = new L.geoJson(newTwo);

    var civil = L.icon({
        iconUrl: "../../static/js/images/civilworks.png",
        iconSize:     [25, 25], // size of the icon
        iconAnchor:   [0, 0], // point of the icon which will correspond to marker's location
        opacity: 0.5,
    });

var markers = L.markerClusterGroup({ chunkedLoading: true });
        
   for (var i = 0; i < newTwo.features.length; i++) {
            var layerInfo ="<h5><b><big>"+newTwo.features[i].properties.field_1+"</big></b></h5>"+
                                "<b>"+newTwo.features[i].properties.field_3+"</b><br>"+
                                "Status:"+newTwo.features[i].properties.field_7+"%";
            var regTwo = new CustomPop().setContent(layerInfo);

            var a = [parseFloat(newTwo.features[i].properties.field_12),parseFloat(newTwo.features[i].properties.field_11)];
            var title = newTwo.features[i].properties.field_2;
            var marker = L.marker(L.latLng(a[0], a[1]), { title: title,icon:civil});
            marker.bindPopup(regTwo);
            markers.addLayer(marker);
        }

        map.addLayer(markers);

//layer initializations
    var regions;
    var provinces;
    var airports;
    var IndustrialZones;
    var roads;



//initialize Airport Points
    var planeIcon = L.icon({
        iconUrl: "../../static/js/images/airports.png",
        iconSize:     [25, 25], // size of the icon
        iconAnchor:   [0, 0], // point of the icon which will correspond to marker's location
        opacity: 0.5,
    });

   airports = new L.geoJson(airports, {
        pointToLayer: function (feature, latlng) {
            var layerInfo ="<h5><b><big>"+feature.properties.AIRPORTNAM+" Port</big></b></h5>"+
                                "<b>"+feature.properties.ADDRESS+"</b><br>"+
                                ""+feature.properties.NEWCLASS+"";
            var pop = new CustomPop().setContent(layerInfo);

            return L.marker(latlng, {icon:planeIcon}).bindPopup(pop);
        }
    });

//initialize Seaports Points
    var seaportIcon = L.icon({
        iconUrl: "../../static/js/images/seaports.png",
        iconSize:     [25, 25], // size of the icon
        iconAnchor:   [0, 0], // point of the icon which will correspond to marker's location
        opacity: 0.5,
    });

   seaports = new L.geoJson(seaports, {
        pointToLayer: function (feature, latlng) {
            var layerInfo ="<h5><b><big>"+feature.properties.PORTNAME+" Port</big></b></h5>"+
                                "<b>"+feature.properties.CLASSIFICA+"</b><br>"+
                                ""+feature.properties.SUPER_REGI+"";
            var pop = new CustomPop().setContent(layerInfo);

            return L.marker(latlng, {icon:seaportIcon}).bindPopup(pop);
        }
    });

//initialize Roads
    roads = new L.geoJson(roads,{
        style:styleRoads,
        onEachFeature:onEachFeatureRoads
    });

        //Style Industrial Zones
        function styleRoads(feature) {
            if(feature.properties.type === 'primary'){
                return {
                    weight: 3,
                    opacity: 1,
                    color: '#E52769',
                    dashArray: '',
                    fillOpacity: 0.5,
                    fillColor: '#3AE0A2'
                };
            }
            else if (feature.properties.type === 'secondary'){
                return {
                    weight: 2,
                    opacity: 1,
                    color: '#347385',
                    dashArray: '3',
                    fillOpacity: 0.5,
                    fillColor: '#3AE0A2'
                };
            }
        }

        //style behavior Roads
        function highlightRoads(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 2,
                color: '#DAFE24',
                dashArray: '',
                fillOpacity: 0.7,
                fillColor: '#F58723'
            });

            if (!L.Browser.ie && !L.Browser.opera) {
                layer.bringToFront();
        }
    }

        function resetHighlightRoads(e) {
            roads.resetStyle(e.target);
        }

        function onEachFeatureRoads(feature, layer) {
            layer.on({
                mouseover: highlightRoads,
                mouseout: resetHighlightRoads,
                click: zoomToFeature
            });
        }

//initialize Industrial Zones
    IndustrialZones= new L.geoJson(IndusZones,{
        style:styleIndusZones,
        onEachFeature: onEachFeatureIndusZones
    });

    //Style Industrial Zones
        function styleIndusZones(feature) {
            return {
                weight: 1,
                opacity: 1,
                color: '#E52769',
                dashArray: '',
                fillOpacity: 0.5,
                fillColor: '#3AE0A2'
            };
        }


    //style behavior Industrial Zones  
        function highlightIndusZones(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 2,
                color: 'yellow',
                dashArray: '3',
                fillOpacity: 0.7,
                fillColor: '#F58723'
            });

            if (!L.Browser.ie && !L.Browser.opera) {
                layer.bringToFront();
            }

            var popupIndus = $("<div></div>",{
                id:"industrial",
                css:{}
            });
            var contentIndus = $("<h4>Industrial Zones</h4><p>"+layer.feature.properties.CODE+"</p><p style='font-size:11px'><i><b>"+layer.feature.properties.LOCATION+"</b></i></p>").appendTo(popupIndus);

            popupIndus.appendTo("#map");
        }

        function resetHighlightIndusZones(e) {
            IndustrialZones.resetStyle(e.target);
            $("#industrial").remove();
        }

        function onEachFeatureIndusZones(feature, layer) {
            layer.on({
                mouseover: highlightIndusZones,
                mouseout: resetHighlightIndusZones,
                click: zoomToFeature
            });
        }

//initialize Provinces Map
    provinces = new L.geoJson(ProvData,{
            style:styleProv,
            onEachFeature: onEachFeatureProv
            });

    //Style Provinces
        function styleProv(feature) {
            var fill ="rgb("+feature.properties.color+")";
            return {
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.5,
                fillColor: fill
            };
        }

    //style behavior Provinces 
        function highlightProvinces(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 2,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7,
                fillColor: '#D0D102'
            });

            if (!L.Browser.ie && !L.Browser.opera) {
                layer.bringToFront();
            }

            var popupProv = $("<div></div>",{
                id:"provinces",
                css:{}
            });
            var contentProv = $("<h4>Province</h4><p>"+layer.feature.properties.NAME_1+"</p><p style='font-size:11px'><i><b>"+layer.feature.properties.REGION+"</b></i></p>").appendTo(popupProv);

            popupProv.appendTo("#map");
        }

        function resetHighlightProv(e) {
            provinces.resetStyle(e.target);
            $("#provinces").remove();
        }

        function onEachFeatureProv(feature, layer) {
            layer.on({
                mouseover: highlightProvinces,
                mouseout: resetHighlightProv,
                click: zoomToFeature
            });
        }

//initialize Regions map

    regions = new L.geoJson(RegionData, {
                style: style,
                onEachFeature: onEachFeature
            });

    //style Regions
     function style(feature) {
            return {
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7,
                fillColor: feature.properties.color
            };
        }

    //style behavior Regions    
        function highlightFeature(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 3,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.5,
                fillColor:'#F21311'
            });

            if (!L.Browser.ie && !L.Browser.opera) {
                layer.bringToBack();
            }

            var popup = $("<div></div>",{
                id:"region",
                css:{}
            });
            var content = $("<h4>Region</h4><div>"+layer.feature.properties.REGION+"</div>").appendTo(popup);
            popup.appendTo("#map");
        }

        function resetHighlight(e) {
            regions.resetStyle(e.target);
            $("#region").remove();
        }

        function zoomToFeature(e) {
            map.fitBounds(e.target.getBounds());
        }

        function onEachFeature(feature, layer) {
            layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight,
                click: zoomToFeature
            });
        }

var baseLayers = {
  "Base Maps": {
    "OSM Satellite": satellite,
    "OpenStreet Map": streets,
  }
};

var overLayers = {
  "Boundaries": {
    "Regions": regions,
    "Provinces": provinces
  },
    "Road Network": {
    "<span style='color:black;'><b>Primary Roads</b></span><img src='../../static/js/images/primary.png'></br><span style='padding-left:10px;'>Secondary Roads</span><img src='../../static/js/images/secondary.png'>": roads
  },
  "Industrial Zones": {
    "Industrial Zones": IndustrialZones
  },
    "Transport POIs": {
    "<span>Airports</span><img src='../../static/js/images/airports.png' width='30px' style='margin-left:5px;'/>": airports,
    "<span>Seaports</span><img src='../../static/js/images/seaports.png' width='30px' style='margin-left:5px;'/>": seaports
  }
};

var baseMaps={
    "OSM Satellite": satellite,
    "OpenStreet Map": streets,
};

var overlayMaps={
    "Regions": regions,
    "Roads": roads,
    "Industrial Zones": IndustrialZones,
    "Airports": airports
};

regions.addTo(map);

//L.control.layers(baseMaps, overlayMaps).addTo(map);
map.addControl( new L.Control.CategorizedLayers(baseLayers, overLayers, {collapsed: false}) );














