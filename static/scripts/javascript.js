const url = "localhost:5000"


function getBooksByCity() {
    var endpoint = url + "/api/1"
    var db_type 
    if (document.getElementsByName("db-selector")[0].checked) {
        db_type = "mysql"
    } else {
        db_type = "mongo"
    }
    var city = document.getElementById("searchInput").value

    var body = {"db_type": db_type, "city": city}
    apiCall(endpoint, body, (data) => createTable(data))

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
    for(var i in data["data"][0]) {
        var th = document.createElement('th')
        th.innerHTML = i
        tr.appendChild(th)
    }
    table.appendChild(tr)

    for (var j in data["data"]) {
        var tr = document.createElement('tr')
        for(var k in data["data"][j]) {
            var td = document.createElement('td')
            td.innerHTML = data["data"][j][k]
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    resultDiv.appendChild(table)
}



function apiCall(endpoint, body, callback) {
    fetch(endpoint, {
        method: 'GET',
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