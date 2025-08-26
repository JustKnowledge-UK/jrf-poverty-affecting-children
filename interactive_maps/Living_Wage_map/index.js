var map = L.map('map', {
    zoomControl: true,
    zoomDelta: 0.5,  // smaller = finer zoom steps (e.g., 0.5 = half-step zooms)
    zoomSnap: 0.5    // aligns zoom levels to increments of 0.5
}).setView([51.61, -0.11], 12);


L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    detectRetina: true,
}).addTo(map);

L.geoJson(blw_con).addTo(map);


// Select colour according to the percentage of jobs paid below living wage.
function getColor(d) {
    return d >= 45 ? '#d53e4f' :
           d >= 40  ? '#f46d43' :
           d >= 35  ? '#fdae61' :
           d >= 30  ? '#fee08b' :
           d >= 25   ? '#e6f598' :
           d >= 20   ? '#abdda4' :
           d >= 15   ? '#66c2a5' :
                      '#3288bd';
}

// Style the geoJSON layer.
function style(feature) {
    return {
        fillColor: getColor(feature.properties.percent_blw),
        weight: 0,
        opacity: 0,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.3
    };
}

L.geoJson(blw_con, {style: style}).addTo(map);


var geojson;


// Make the geometries highlighted visually in some way when they are hovered with a mouse.
function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    layer.bringToFront();
    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    geojson.resetStyle(e.target);
    info.update();
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



geojson = L.geoJson(blw_con, {
    style: style,
    onEachFeature: onEachFeature
}).addTo(map);


var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>Percentage of Jobs paid below Living Wage:</h4>' +  (props ?
        '<b>' + props.PCON24NM + '</b><br />' + props.percent_blw + '%'
        : 'Hover over a constituency');
};

info.addTo(map);


var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 15, 20, 25, 30, 35, 40, 45],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i]) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '% <br>' : '+%');
    }

    return div;
};

legend.addTo(map);
