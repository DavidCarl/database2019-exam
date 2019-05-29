const url = "localhost:5000"
var single_marker

function getBooksByCity() {
    var endpoint = "/api/1"
    var db_type
    if (document.getElementsByName("db-selector")[0].checked) {
        db_type = "mysql"
    } else {
        db_type = "mongo"
    }
    var city = document.getElementById("searchInput").value

    var body = { "db_type": db_type, "city": city }

    apiCall(endpoint, body, (data) => createTable(data))
}

function getCitiesByBook() {
    var endpoint = "/api/2"
    var db_type
    if (document.getElementsByName("db-selector")[0].checked) {
        db_type = "mysql"
    } else {
        db_type = "mongo"
    }
    var title = document.getElementById("searchInput").value

    var body = { "db_type": db_type, "title": title }

    apiCall(endpoint, body, (data) => updateMap(data))
}

function getBooksCitiesByAuthor() {
    var endpoint = "/api/3"
    var db_type
    if (document.getElementsByName("db-selector")[0].checked) {
        db_type = "mysql"
    } else {
        db_type = "mongo"
    }
    var author = document.getElementById("searchInput").value

    var body = { "db_type": db_type, "author": author }

    apiCall(endpoint, body, (data) => tableAndMap(data))
}

function getBooksByGeolocation() {
    var endpoint = "/api/4"
    var db_type
    if (document.getElementsByName("db-selector")[0].checked) {
        db_type = "mysql"
    } else {
        db_type = "mongo"
    }
    geolocation = {
        "lat": document.getElementById("lat").value,
        "lng": document.getElementById("lng").value
    }

    var body = { "db_type": db_type, "geolocation": geolocation }

    apiCall(endpoint, body, (data) => createSmallTable(data))
}

function createSmallTable(data) {
    data = data["data"]

    var resultDiv = document.getElementById('result-col')

    var child = resultDiv.lastElementChild
    while (child) {
        resultDiv.removeChild(child)
        child = resultDiv.lastElementChild
    }

    var table = document.createElement('table')
    table.className = "table table-hover"
    var tr = document.createElement('tr')
    // Creating headers
    for (var i in data[0]) {
        var th = document.createElement('th')
        th.innerHTML = i
        tr.appendChild(th)
    }
    table.appendChild(tr)

    for (var j in data) {
        var tr = document.createElement('tr')
        for (var k in data[j]) {
            var td = document.createElement('td')
            td.innerHTML = data[j][k]
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    resultDiv.appendChild(table)
}

function tableAndMap(data) {
    var books = data["data"]["books"]
    var cities = data["data"]["cities"]

    var resultDiv = document.getElementById('result-col')

    var child = resultDiv.lastElementChild
    while (child) {
        resultDiv.removeChild(child)
        child = resultDiv.lastElementChild
    }

    var table = document.createElement('table')
    table.className = "table table-hover"
    var tr = document.createElement('tr')
    // Creating headers
    for (var i in books[0]) {
        var th = document.createElement('th')
        th.innerHTML = i
        tr.appendChild(th)
    }
    table.appendChild(tr)

    for (var j in books) {
        var tr = document.createElement('tr')
        for (var k in books[j]) {
            var td = document.createElement('td')
            td.innerHTML = books[j][k]
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    resultDiv.appendChild(table)

    var pos = cities[Object.keys(cities)[0]]

    var map = new google.maps.Map(
        document.getElementById("map"),
        { zoom: 6, center: pos }
    )
    for (var k in cities) {
        var marker = new google.maps.Marker({
            position: cities[k],
            title: k,
            map: map
        })
    }

}

function createTable(data) {
    // Dummy data, should be param
    var resultDiv = document.getElementById('result-col')

    var child = resultDiv.lastElementChild
    while (child) {
        resultDiv.removeChild(child)
        child = resultDiv.lastElementChild
    }

    var table = document.createElement('table')
    table.className = "table table-hover"
    var tr = document.createElement('tr')
    // Creating headers
    for (var i in data["data"][0]) {
        var th = document.createElement('th')
        th.innerHTML = i
        tr.appendChild(th)
    }
    table.appendChild(tr)

    for (var j in data["data"]) {
        var tr = document.createElement('tr')
        for (var k in data["data"][j]) {
            var td = document.createElement('td')
            td.innerHTML = data["data"][j][k]
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    resultDiv.appendChild(table)
}

function initMap() {
    var startpos = { lat: 55.770490, lng: 12.512238 }
    var map = new google.maps.Map(
        document.getElementById('map'), { zoom: 6, center: startpos });

    map.addListener('click', function(event) {
        updateLatLng(event, map)
    })
}

function updateLatLng(event, map) {
    var lat = event.latLng.lat();
    var lng = event.latLng.lng();

    if (!single_marker || !single_marker.setPosition) {
        single_marker = new google.maps.Marker({
          position: event.latLng,
          map: map,
        });
      } else {
        single_marker.setPosition(event.latLng);
      }

    document.getElementById('lat').value = lat
    document.getElementById('lng').value = lng
}

function updateMap(data) {
    var pos = data["data"][Object.keys(data["data"])[0]]

    var map = new google.maps.Map(
        document.getElementById("map"),
        { zoom: 6, center: pos }
    )
    for (var i in data["data"]) {
        var marker = new google.maps.Marker({
            position: data["data"][i],
            title: i,
            map: map
        })
    }
}

function apiCall(endpoint, body, callback) {
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    })
        .then((response) => {
            return response.json()
        })
        .then((jsonResponse) => callback(jsonResponse))
        .catch((error) => callback('Error!'))
}