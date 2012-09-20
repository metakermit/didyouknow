var chart; // global
var data; // DATA IS DEFINED AFTER AJAX REQUEST, SO DOES IT MAKE SENSE TO CALL IT WHILE DEFINING CHART? 
var indicator1 = ' ';
var indicator2 = ' ';

var brush;

/**
 * Request data from the server, add it to the graph and set a timeout to request again
 */

function requestData() {
	$.ajax({
		url: "../getdatascatter/", 
		data: {
			countries: $("#selectCountries").val(),
			indicators: $("#selectIndicators").val()
		},
		success: function(focData) {
			data = focData;
			
			drawScatterMatrix(data);
			updateTextBox(data);
			updateDataTable(data);
			
        },
		cache: false,
	});
}

// Update text box with new data
function updateTextBox(data)
{
	// CSV format
	indicatorsString = "";
	for (i in data.indicators)
	{
		indicatorsString = indicatorsString + "\"" + data.indicators[i] + "\" "; 
	}
	$("#data-table").val("\"code\" " + indicatorsString + "\"date\" \"crisis\"\n");
	
	for (i in data.values) 
	{
		$("#data-table").val($("#data-table").val() + data.values[i].country + " ");
		for (j in data.indicators)
		{
			$("#data-table").val($("#data-table").val() + " " + data.values[i][data.indicators[j]]);    
		} 
		$("#data-table").val($("#data-table").val() + " " + data.values[i].date + " " + data.values[i].crisis + "\n");
	}
	
}


// Update data table with new data
function updateDataTable(data)
{
	$("#data-table2").empty();
	
	/*
	// CSV format
	var indicatorsString = "";
	for (i in data.indicators)
	{
		indicatorsString = indicatorsString + "<td>\"" + data.indicators[i] + "\"</td>"; 
	}
	$("#data-table2").append("<tr><td>\"code\"</td>" + indicatorsString + "<td>\"date\"</td><td>\"crisis\"</td></tr>");
	
	var row = "<tr><td>" + data.values[i].country + "</td>";
	for (i in data.values) 
	{
		//$("#data-table2").append("<tr><td>" + data.values[i].country + "</td>");
		for (j in data.indicators)
		{
			//$("#data-table2").append("<td>" + data.values[i][data.indicators[j]] + "</td>"); 
			row = row + "<td>" + data.values[i][data.indicators[j]] + "</td>";
		} 
		//$("#data-table2").append("<td>" + data.values[i].date + "</td><td>" + data.values[i].crisis + "</td></tr>");
		row = row + "<td>" + data.values[i].date + "</td><td>" + data.values[i].crisis + "</td></tr>";
		
		$("#data-table2").append(row);
	}
	*/
	
	//var a = [{"code":0,"value":23},{"code":1,"value":26}];
	//var a = {"code":0,"value":23,"code2":1,"value2":26};
	var rows = d3.select("#data-table2")
	.selectAll("tr")
	.data(data.values)
	.enter().append("tr")
	.selectAll("td")
	.data(function(d){return d3.values(d);})
	.enter().append("td")
	.text(function(d){return d;});

}



function changeMode()
{
	if ($("#selectCountries").val() != null && data != null) 
	{ 

		if ( $("#change-mode :radio:checked").attr("value") == "crisis" )
		{
			d3.selectAll(".cell circle").filter(function(d){return d.crisis;}).classed("crisis-yes",1);
			d3.selectAll(".cell circle").filter(function(d){return !d.crisis;}).classed("crisis-no",1);
		}
		if ( $("#change-mode :radio:checked").attr("value") == "normal" )
		{
			d3.selectAll(".cell circle").filter(function(d){return d.crisis;}).classed("crisis-yes",0);
			d3.selectAll(".cell circle").filter(function(d){return !d.crisis;}).classed("crisis-no",0);
		}
	}
	
}

function drawScatterMatrix(focData) {
	
	d3.selectAll("svg").remove();
	
	// Size parameters.
    var size = 150,
    padding = 19.5,
    n = data.indicators.length;
	m = data.countries.length;
	  
    // Position scales.
    var x = {}, y = {};
    data.indicators.forEach(function(indicator) {
        var value = function(d) { return d[indicator]; },
        domain = [d3.min(data.values, value), d3.max(data.values, value)],
        range = [padding / 2, size - padding / 2];
        x[indicator] = d3.scale.linear().domain(domain).range(range);
        y[indicator] = d3.scale.linear().domain(domain).range(range.reverse());
    });
	
	  // Axes.
	  var axis = d3.svg.axis()
	      .ticks(5)
	      .tickSize(size * n);
	
	  // Brush.
	  var brush = d3.svg.brush()
	      .on("brushstart", brushstart)
	      .on("brush", brush)
	      .on("brushend", brushend);
	
	  // Root panel.
	  var svg = d3.select("#chart").append("svg:svg")
	      .attr("width", size * n + padding + 150)
	      .attr("height", size * n + padding + 60)
	      .append("svg:g")
	      .attr("transform", "translate(130,0)");
	
	  // Legend.
	  var legend = svg.selectAll("g.legend")
	      .data(data.countries)
	    .enter().append("svg:g")
	      .attr("class", "legend")
	      .attr("transform", function(d, i) { return "translate(-120," + (i * 20 + (size * n - (m+1)*20) + padding) + ")"; });


	  legend.append("svg:circle")
	      .attr("class", String)
		  //.attr("class", function(d) { return "country" + data.countries.indexOf(d); } )
	      .attr("r", 3);
	
	  legend.append("svg:text")
	      .attr("x", 12)
	      .attr("dy", ".31em")
	      .text(function(d) { return d; });
	
	  // X-axis.
	  svg.selectAll("g.x.axis")
	      .data(data.indicators)
	    .enter().append("svg:g")
	      .attr("class", "x axis")
	      .attr("transform", function(d, i) { return "translate(" + i * size + ",0)"; })
	      .each(function(d) { d3.select(this).call(axis.scale(x[d]).orient("bottom")); });
	
	  // Y-axis.
	  svg.selectAll("g.y.axis")
	      .data(data.indicators)
	    .enter().append("svg:g")
	      .attr("class", "y axis")
	      .attr("transform", function(d, i) { return "translate(0," + i * size + ")"; })
	      .each(function(d) { d3.select(this).call(axis.scale(y[d]).orient("right")); });

	  // Cell and plot.
	  var cell = svg.selectAll("g.cell")
	      .data(cross(data.indicators, data.indicators))
	    .enter().append("svg:g")
	      .attr("class", "cell")
	      .attr("transform", function(d) { return "translate(" + d.i * size + "," + d.j * size + ")"; })
	      .each(plot);
	
	  // Titles for the diagonal.
	  cell.filter(function(d) { return d.i == d.j; }).append("svg:text")
	      .attr("x", padding)
	      .attr("y", padding)
	      .attr("dy", ".71em")
	      .text(function(d) { return d.x; });
	
	  function plot(p) {
	    var cell = d3.select(this);
	
	    // Plot frame.
	    cell.append("svg:rect")
	        .attr("class", "frame")
	        .attr("x", padding / 2)
	        .attr("y", padding / 2)
	        .attr("width", size - padding)
	        .attr("height", size - padding);
	
	    // Plot only the dots that have values for both indicators.
	    cell.selectAll("circle")
	        .data(data.values.filter(function(d){return (d[p.x]!="" && d[p.y]!="") ? 1 : 0;}))
	      .enter().append("svg:circle")
			.attr("class", function(d) { return d.country; })
	        .attr("cx", function(d) { return x[p.x](d[p.x]); })
	        .attr("cy", function(d) { return y[p.y](d[p.y]); })
	        .attr("r", 3);
	
	    // Plot brush.
	    cell.call(brush.x(x[p.x]).y(y[p.y]));
	  }
	  
	  // Clear the previously-active brush, if any.
	  function brushstart(p) {
	    if (brush.data !== p) {
	      cell.call(brush.clear());
	      brush.x(x[p.x]).y(y[p.y]).data = p;
	    }
	  }
	
	  /*
	  // Highlight the selected circles.
	  function brush(p) {
	    var e = brush.extent();
	    svg.selectAll(".cell circle").attr("class", function(d) {
	      return e[0][0] <= d[p.x] && d[p.x] <= e[1][0]
	          && e[0][1] <= d[p.y] && d[p.y] <= e[1][1]
			  ? d.country : null;
	    });
	  }
	  */
	 
	  // Highlight the selected circles.
	  function brush(p) {
	    var e = brush.extent();
	    svg.selectAll(".cell circle").classed("hidden", function(d) {
	      return e[0][0] <= d[p.x] && d[p.x] <= e[1][0]
	          && e[0][1] <= d[p.y] && d[p.y] <= e[1][1]
			  ? 0 : 1;
	    });
	  }
	 
	  /*
	  // If the brush is empty, select all circles.
	  function brushend() {
	    if (brush.empty()) svg.selectAll(".cell circle").attr("class", function(d) {
		  return d.country;
	    });
	  }
	  */
	 
	 // If the brush is empty, select all circles.
	  function brushend() {
	    if (brush.empty()) svg.selectAll(".cell circle").classed("hidden", 0);
	  }
	 
	
	  function cross(a, b) {
	    var c = [], n = a.length, m = b.length, i, j;
	    for (i = -1; ++i < n;) for (j = -1; ++j < m;) c.push({x: a[i], i: i, y: b[j], j: j});
	    return c;
	  }
	  
  
}





