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
		beforeSend: function() {
			$("#chart > .screen").empty();
			$("#chart > .screen").removeClass("error");
			$("#chart > .screen").addClass("loading");
		},
		error: function(jqXHR) {
			$("#chart > .screen").addClass("error");
			$("#chart > .screen").append("<p>Sorry, there was an error in processing your request.</p>")
		},
		success: function(focData) {
			data = focData;
			
			$("#chart > .screen").removeClass("loading");
			
			drawScatterMatrix(data);
			updateTextarea(data);
			updateTextareaSGD(data);
			updateDataTable(data);
			updateDataList(data);
			
			updateYearsTable(data);
			
        },
		cache: false,
	});
}

function requestSGD() {
	
	// TODO: Replace attribute names!
	var attributes = new Object();
	var text = $("#data-textarea-sgd").val();
	text = text.split('\n');
	var line = text[3];
	line = line.split(' ');
	
	// First and last attributes are index and class.
	line = line.slice(1,-1);
	
	for (att in line) {
		attributes[att] = line[att];
	}
	
	atributtesString = Object.keys(attributes).toString();
	atributtesString = atributtesString.replace(/,/g,' ');
	
	text[3] = "no " + atributtesString + " class";
	text = text.toString();
	text = text.replace(/,/g,'\n')
		
	$.ajax({
		url: "../executesgd/", 
		data: {
			//sgd: $("#data-textarea-sgd").val()
			sgd: text
		},
		beforeSend: function() {
			$("#rules-display > .screen").empty();
			$("#rules-display > .screen").removeClass("error");
			$("#rules-display > .screen").addClass("loading");
			
		},
		error: function(jqXHR) {
			$("#rules-display > .screen").addClass("error");
			$("#rules-display > .screen").append("<p>Sorry, there was an error in processing your request.</p>")
		},
		//dataFilter: function(rules_text) {
		//	// TODO: Rename attributes back!
		//	return rules_text;
		//},
		success: function(rules_text) {
			
			if (rules_text=="") {
				$("#rules-display > .screen").addClass("error");
				$("#rules-display > .screen").append("<p>Sorry, no rules retrieved.</p>")
				return;
			}
			
			// TODO: Rename attributes back!
			
			
			// Fetch only first line from the results (first rule).
			rules = rules_text.split('\n');
			rules = rules[0];
			
			//$('#rules-display > *:not(.screen)').empty();
			//$('#rules-display > .rules-content').empty();
			$("#rules-display > .screen").removeClass("error");
			$("#rules-display > .screen").removeClass("loading");
			$("#rules-textarea").addClass("inactive-rules");
			
			var parsedRules = parseRules(rules);
			
			for (i in parsedRules) {
				parsedRules[i].variable = attributes[parsedRules[i].variable];
			}
			
			applyRules(parsedRules);
			
        },
		cache: false,
	});
}


function parseRules(rulesString) {

	var rules = new Array();
	
	// Extract all rules of the form:
	//	(var1=0.1) (var2<=-0.2) etc. for floating variables
	//	(var1=True) (var2#red) etc. for categorical (and boolean) variables 
	var rulesList = rulesString.match(/\(\s*(\w+[\w\.]*\s*(<|>|=|<=|>=)\s*(-?(0|([1-9]\d*))(\.\d+)?)|\w+\s*(=|#)\s*(\w+))\s*\)/g); // dots in variable name
	
	for (i in rulesList)
	{
		// Extract variable, operator and value from each matched rules.
		var parsedRule = rulesList[i].match(/\(\s*(?:(\w+[\w\.]*)\s*(<|>|=|<=|>=)\s*(-?(?:0|(?:[1-9]\d*))(?:\.\d+)?)|(\w+)\s*(=|#)\s*(\w+))\s*\)/); // dots in variable name
		parsedRule = parsedRule.filter(function(d){return d!=undefined;});
		var rule = new Object();
		rule["variable"] = parsedRule[1];
		rule["operator"] = parsedRule[2];
		rule["value"] = parsedRule[3];
		rules.push(rule);	
	}
	
	return rules;
}

function applyRules(rules) {
	
	$('#rules-display > .rules-content').empty();
	d3.selectAll(".cell circle").classed("hidden",0);
	//d3.selectAll("#data-table > tr:not(:first-child)").classed("hidden-row",0);
	//d3.selectAll("#data-list > p:not(:first-child)").classed("hidden-row",0);
	d3.selectAll("#data-table > tbody > tr").classed("hidden-row",0);
	d3.selectAll("#data-list > p:not(.columnNames)").classed("hidden-row",0);
	
	for (i in rules)
	{
		var rule = rules[i];
		$('#rules-display > .rules-content').append( "(" + 
									"<span class=\"variable\">" + rule.variable + "</span>" +
									"<span class=\"operator\">" + rule.operator + "</span>" +
									"<span class=\"value\">" + rule.value + "</span>" +
									")" );
		var filterData;
		
		switch (rule.operator)
		{
			case "<":
				//filterData = function(d){ return (d[parsedRule[1]] < parsedRule[3]) ? 0 : 1; };
				filterData = function(d){ try {var a = d[rule.variable];} catch(err) {var a = null;} return (a < rule.value) ? 0 : 1; };
				break;
			case ">":
				//filterData = function(d){ return (d[parsedRule[1]] > parsedRule[3]) ? 0 : 1; };
				filterData = function(d){ try {var a = d[rule.variable];} catch(err) {var a = null;} return (a > rule.value) ? 0 : 1; };
				break;
			case "<=":
				//filterData = function(d){ return (d[parsedRule[1]] <= parsedRule[3]) ? 0 : 1; };
				filterData = function(d){ try {var a = d[rule.variable];} catch(err) {var a = null;} return (a <= rule.value) ? 0 : 1; };
				break;
			case ">=":
				//filterData = function(d){ return (d[parsedRule[1]] >= parsedRule[3]) ? 0 : 1; };
				filterData = function(d){ try {var a = d[rule.variable];} catch(err) {var a = null;} return (a >= rule.value) ? 0 : 1; };
				break;
			case "=":
				//filterData = function(d){ return (d[parsedRule[1]].toString() == parsedRule[3]) ? 0 : 1; };
				filterData = function(d){ try {var a = d[rule.variable];} catch(err) {var a = null;} return (a == rule.value) ? 0 : 1; };
				break;
			case "#":
				//filterData = function(d){ return (d[parsedRule[1]].toString() != parsedRule[3]) ? 0 : 1; };
				filterData = function(d){ try {var a = d[rule.variable];} catch(err) {var a = null;} return (a != rule.value) ? 0 : 1; };
				break;
			default:
				filterData = function(d){ return 0; };
				break;
		}					
		d3.selectAll(".cell circle").filter(filterData).classed("hidden",1);
		//d3.selectAll("#data-table > tr:not(:first-child)").filter(filterData).classed("hidden-row",1);
		//d3.selectAll("#data-list > p:not(:first-child)").filter(filterData).classed("hidden-row",1);
		d3.selectAll("#data-table > tbody > tr").filter(filterData).classed("hidden-row",1);
		d3.selectAll("#data-list > p:not(columnNames)").filter(filterData).classed("hidden-row",1);
	}
}

function updateYearsTable(data)
{
	$("#years-table > p").empty();
	
	var dates = $.map(data.values, function(d,i){return d.date;});
	dates = dates.sort();
	var lastDate = dates[0];
	var uniqueDates = [lastDate];
	for (i=1;i<dates.length;i++)
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
			//d3.selectAll("#data-table > tr:not(:first-child)").classed("hidden-row",function(d){return (date==d.date) ? 0 : 1;}); 
			//d3.selectAll("#data-list > p:not(:first-child)").classed("hidden-row",function(d){return (date==d.date) ? 0 : 1;}); 
			d3.selectAll("#data-table > tbody > tr").classed("hidden-row",function(d){return (date==d.date) ? 0 : 1;}); 
			d3.selectAll("#data-list > p:not(.columnNames)").classed("hidden-row",function(d){return (date==d.date) ? 0 : 1;}); 
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

/*
function replaceMe(a,direction)
{
	switch(direction)
	{
	case 1:
		a = a.replace(/\./g,"_");
		a = a.replace(/0/g,"a");
		a = a.replace(/1/g,"b");
		a = a.replace(/2/g,"c");
		a = a.replace(/3/g,"d");
		a = a.replace(/4/g,"e");
		a = a.replace(/5/g,"f");
		a = a.replace(/6/g,"g");
		a = a.replace(/7/g,"i");
		a = a.replace(/8/g,"j");
		a = a.replace(/9/g,"k");
		break;
	case 2:
		a = a.replace(/\_/g,".");
		a = a.replace(/a/g,"0");
		a = a.replace(/b/g,"1");
		a = a.replace(/c/g,"2");
		a = a.replace(/d/g,"3");
		a = a.replace(/e/g,"4");
		a = a.replace(/f/g,"5");
		a = a.replace(/g/g,"6");
		a = a.replace(/i/g,"7");
		a = a.replace(/j/g,"8");
		a = a.replace(/k/g,"9");
		break;
	}
	return a;
}
*/

// Update textarea (sgd) with new data
function updateTextareaSGD(data)
{
	// sgd format
	infoString = "";
	infoString = infoString + "Number of examples " + data.values.length + "\n";
	infoString = infoString + "Number of inputs " + data.indicators.length + "\n";
	
	typeString = "";
	typeString = typeString + "n"; // index variable
	for (i in data.indicators)
	{
		// all indicator values are float !
		typeString = typeString + " f"; 
	}
	typeString = typeString + " o\n"; // class variable
	
	indicatorString = "";
	indicatorString = indicatorString + "no";
	for (i in data.indicators)
	{
		indicatorString = indicatorString + " " + data.indicators[i]; 
		//indicatorString = indicatorString + " " + replaceMe(data.indicators[i],1); 
	}
	indicatorString = indicatorString + " class\n";
	
	$("#data-textarea-sgd").val(infoString + typeString + indicatorString);
	
	for (i in data.values) 
	{
		exampleString = "";
		index = eval(i) + 1;
		exampleString = exampleString + index;
	
		for (j in data.indicators)
		{
			value = data.values[i][data.indicators[j]];
			if (value=="")
			{
				exampleString = exampleString + " ?";
			}
			else
			{
				exampleString = exampleString + " " + value.toFixed(2);
			}
		} 
		
		if (data.values[i].crisis==true)
		{
			exampleString = exampleString + " true";
		}
		else
		{
			exampleString = exampleString + " false";
		}
		exampleString = exampleString + "\n";
		
		$("#data-textarea-sgd").val($("#data-textarea-sgd").val() + exampleString);
	}
	
}

function columnSorting(a,b) { 
	if (a=="date" || a=="country") { return -1;}
	if (b=="date" || b=="country") { return 1;}
	if (a=="crisis") { return 1;}
	if (b=="crisis") { return -1;}
	return (a<b) ? -1 : 1; 
}
				 									
// Update data table with new data
function updateDataTable(data)
{
	/*
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
	*/
	
	$("#data-table").empty();
	
	var columns = d3.keys(data.values[0]).sort( columnSorting );
	
    var thead = d3.select("#data-table").append("thead");
    var tbody = d3.select("#data-table").append("tbody");

    // append the header row
    thead.append("tr")
        .selectAll("th")
        .data(columns)
        .enter()
        .append("th")
            .text(function(column) { return column; });

    // create a row for each object in the data
    var rows = tbody.selectAll("tr")
        .data(data.values)
        .enter()
        .append("tr");

    // create a cell in each row for each column
    var cells = rows.selectAll("td")
        .data(function(row) {
            return columns.map(function(column) {
                return {column: column, value: row[column]};
            });
        })
        .enter()
        .append("td")
            .text(function(d) { return d.value; });

}


// Update data list with new data
function updateDataList(data)
{
	
	$("#data-list").empty();
	var columns = d3.keys(data.values[0]).sort( columnSorting );
	
	var columnNames = d3.select("#data-list")
	.selectAll("p")
	.data([columns])
	.enter().append("p")
	.text(function(d){ return d; });
	
	$("#data-list > p").addClass("columnNames");
	
	var rows = d3.select("#data-list")
	.selectAll("p:not(.columnNames)")
	.data(data.values)
	.enter().append("p");
	
	var rows2 = rows
	.text(function(d,i){ 
			var line = ""; 
			var values = [];
			for (i in columns) {
				values.push(d[columns[i]]);
			} 
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
	
	// Remove all elements from chart except screen used for display while loading.
	$("#chart > *:not(.screen)").remove();
	
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
        //y[indicator] = d3.scale.linear().domain(domain).range(range.reverse());
		y[indicator] = d3.scale.linear().domain(domain).range(range.slice().reverse());
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
	      .attr("transform", "translate(90,0)");
	
	  // Legend.
	  var legend = svg.selectAll("g.legend")
	      .data(data.countries)
	    .enter().append("svg:g")
	      .attr("class", "legend")
	      .attr("transform", function(d, i) { return "translate(-80," + (i * 20 + (size * n - (m+1)*20) + padding) + ")"; });


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
		//d3.selectAll("#data-table > tr:not(:first-child)").classed("hidden-row", function(d) {
		d3.selectAll("#data-table > tbody > tr").classed("hidden-row", function(d) {
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
			//d3.selectAll("#data-table > tr:not(:first-child)").classed("hidden-row", 0);
			d3.selectAll("#data-table > tbody > tr").classed("hidden-row", 0);
			//d3.selectAll("#data-list > p:not(:first-child)").classed("hidden-row", 0);
			d3.selectAll("#data-list > p:not(.columnNames)").classed("hidden-row", 0);
		}
		
	  }
	 
	
	  function cross(a, b) {
	    var c = [], n = a.length, m = b.length, i, j;
	    for (i = -1; ++i < n;) for (j = -1; ++j < m;) c.push({x: a[i], i: i, y: b[j], j: j});
	    return c;
	  }
	  
  
}





