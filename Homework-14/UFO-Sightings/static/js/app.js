// from data.js
var tableData = data;

var submit = d3.select("#filter-btn");

submit.on("click", function() {

    d3.event.preventDefault();

    var inputElement = d3.select(".form-control");

    var inputValue = inputElement.property("value").toString();

    console.log(inputValue);

    var table = d3.select("tbody");

    table.html("");

    var filteredData = tableData.filter(date => date.datetime === inputValue);

    filteredData.forEach((data) => {
        var row = table.append("tr");
        Object.entries(data).forEach(([key, value]) => {
            var cell = row.append("td");
            cell.text(value);
        });
    });




    console.log(filteredData);


});
