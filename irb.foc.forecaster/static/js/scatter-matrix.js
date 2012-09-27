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
			wbIndicators: $("#selectWBIndicators").val(),
			rcaIndicators: $("#selectRCAIndicators").val()
		},
		success: function(focData) {
			data = focData;
			
			drawScatterMatrix(data);
			updateTextarea(data);
			updateDataTable(data);
			updateDataList(data);
			
			updateYearsTable(data);
			
        },
		cache: false,
	});
}

/*
function updateYearsTable(data)
{
	
	var dates = $.map(data.values, function(d,i){return d.date;});
	dates = dates.sort();
	var lastDate = dates[0];
	var uniqueDates = [lastDate];
	for (i=1;i<=dates.length;i++)
	{
		if (dates[i] == dates[i-1]) { continue; }
		else { lastDate = dates[i]; uniqueDates.push(lastDate); }
	}
	
	console.log(uniqueDates);
	
	d3.select("#years-table > tbody > tr ")
	.selectAll("td")
	.data(uniqueDates)
	.enter().append("td").on("click",
		function(date){
			d3.selectAll(".cell circle").classed("hidden",function(d){return (date==d.date) ? 0 : 1;}); 
			d3.selectAll("#data-table > tr:not(:first-child)").classed("hidden-row",function(d){return (date==d.date) ? 0 : 1;}); 
			d3.selectAll("#data-list > p:not(:first-child)").classed("hidden-row",function(d){return (date==d.date) ? 0 : 1;}); 
			$( "#slider" ).slider( "option", "value", date );
			$( "#year" ).val( $( "#slider" ).slider( "value" ));
 			})
	.text(function(d){return d;});
}
*/



function updateYearsTable(data)
{
	$("#years-table > p").empty();
	
	var dates = $.map(data.values, function(d,i){return d.date;});
	dates = dates.sort();
	var lastDate = dates[0];
	var uniqueDates = [lastDate];
	for (i=1;i<=dates.length;i++)
	{
		if (dates[i] == dates[i-1]) { continue; }
		else { lastDate = dates[i]; uniqueDates.push(lastDate); }
	}
	
	d3.select("#years-table > p ")
	.selectAll("span")
	.data(uniqueDates)
	.enter().append("span").on("click",
		function(date){
			d3.selectAll(".cell circle").classed("hidden",function(d){return (date==d.date) ? 0 : 1;}); 
			d3.selectAll("#data-table > tr:not(:first-child)").classed("hidden-row",function(d){return (date==d.date) ? 0 : 1;}); 
			d3.selectAll("#data-list > p:not(:first-child)").classed("hidden-row",function(d){return (date==d.date) ? 0 : 1;}); 
			$( "#slider" ).slider( "option", "value", date );
			$( "#year" ).val( $( "#slider" ).slider( "value" ));
			d3.selectAll("#years-table > p > span").classed("highlighted-year",function(d){ return (date==d) ? 1 : 0; });
 			})
	.text(function(d){return d + " ";});
}



// Update textarea with new data
function updateTextarea(data)
{
	// CSV format
	indicatorsString = "";
	for (i in data.indicators)
	{
		indicatorsString = indicatorsString + "\"" + data.indicators[i] + "\" ; "; 
	}
	$("#data-textarea").val("\"code\" ; " + indicatorsString + "\"date\" ; \"crisis\"\n");
	
	for (i in data.values) 
	{
		$("#data-textarea").val($("#data-textarea").val() + data.values[i].country);
		for (j in data.indicators)
		{
			$("#data-textarea").val($("#data-textarea").val() + " ; " + data.values[i][data.indicators[j]]);    
		} 
		$("#data-textarea").val($("#data-textarea").val() + " ; " + data.values[i].date + " ; " + data.values[i].crisis + "\n");
	}
	
}


// Update data table with new data
function updateDataTable(data)
{
	$("#data-table").empty();
	
	d3.select("#data-table")
	.selectAll("tr")
	.data([d3.keys(data.values[0])])
	.enter().append("tr")
	.selectAll("td")
	.data(function(d){return d;})
	.enter().append("td")
	.text(function(d){return d;});
	
	var rows = d3.select("#data-table")
	.selectAll("tr:not(:first-child)")
	.data(data.values)
	.enter().append("tr")
	.selectAll("td")
	.data(function(d){return d3.values(d);})
	.enter().append("td")
	.text(function(d){
             return ($.isNumeric(d)) ? (Math.floor(d)-d!=0) ? d.toFixed(2) : d : d; 
			 });

}


// Update data list with new data
function updateDataList(data)
{
	$("#data-list").empty();
	
	var rows = d3.select("#data-list")
	.selectAll("p")
	.data([d3.keys(data.values[0])])
	.enter().append("p")
	.text(function(d){ return d; });
	
	var rows = d3.select("#data-list")
	.selectAll("p:not(:first-child)")
	.data(data.values)
	.enter().append("p")
	//.on("click", function(dp){
	//					d3.selectAll(".cell circle").classed("hidden",function(dc){return (dp.date==dc.date) ? 0 : 1;}); 
 	//					})
	.text(function(d,i){ 
			var line = ""; 
			var values = d3.values(d); 
			for (i in values) { 
				var temp1 = values[i];
				// If temp1 is numeric but NOT integer round it to 2 decimal places.
				var temp2 = $.isNumeric(temp1) ? (Math.floor(temp1)-temp1!=0) ? temp1.toFixed(2) : temp1 : temp1 ;
				if (i == 0) { line = line + temp2; }
				else { line = line + "," + temp2; }
			} 
			return line;
			});

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
		d3.selectAll("#data-table > tr:not(:first-child)").classed("hidden-row", function(d) {
	      return e[0][0] <= d[p.x] && d[p.x] <= e[1][0]
	          && e[0][1] <= d[p.y] && d[p.y] <= e[1][1]
			  ? 0 : 1;
	    });
		d3.selectAll("#data-list > p:not(:first-child)").classed("hidden-row", function(d) {
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
	    if (brush.empty()) {
			svg.selectAll(".cell circle").classed("hidden", 0);
			d3.selectAll("#data-table > tr:not(:first-child)").classed("hidden-row", 0);
			d3.selectAll("#data-list > p:not(:first-child)").classed("hidden-row", 0);
		}
		
	  }
	 
	
	  function cross(a, b) {
	    var c = [], n = a.length, m = b.length, i, j;
	    for (i = -1; ++i < n;) for (j = -1; ++j < m;) c.push({x: a[i], i: i, y: b[j], j: j});
	    return c;
	  }
	  
  
}





