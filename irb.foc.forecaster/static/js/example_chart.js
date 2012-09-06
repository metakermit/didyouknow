
var chart; // global
var data; // DATA IS DEFINED AFTER AJAX REQUEST, SO DOES IT MAKE SENSE TO CALL IT WHILE DEFINING CHART? 
var indicator1 = ' ';
var indicator2 = ' ';

/**
 * Request data from the server, add it to the graph and set a timeout to request again
 */

function requestData() {
	$.ajax({
		url: "../getdata/", 
		data: {
			countries: $("select").val()
		},
		success: function(focData) {
			data = focData;
			
			//if (!$.isEmptyObject(data.RoleOwners)) // data is not a json object so it doesn't work?
			if (data.length!=0)
			{
				indicator1 = data[0].x_ind.code;
				indicator2 = data[0].y_ind.code;
			}
			
			// Remove all series from chart
			while (chart.series.length > 0)
			{
				chart.series[0].remove();
			}
			
			// For all retrieved countries
			for (j in data) {
				var seriesOptions = {
					name: data[j].code,
					data: []
				};
				chart.addSeries(seriesOptions, true);
				var series = chart.series[j]; //, shift = series.data.length > 20; // shift if the series is longer than 20
				var country = data[j];
				//var country = focData[j];
				var x_ind = country.x_ind;
				var y_ind = country.y_ind;
				var dates = country.dates;
				
				// Draw all points for given country 
				for (i in x_ind.data) {
					var point = {x: x_ind.data[i], y: y_ind.data[i], date: dates[i]};
					chart.series[j].addPoint(point, true, false); // point,redraw,shift
				}
				
			}
			updatePlot();
			
			updateTextBox(data);
        },
		cache: false,
	});
}

// Update labels according to fetched indicators.
function updatePlot()
{
	// Alternative:  $(chart.yAxis[0].axisTitle.element).text('New Label');
	chart.xAxis[0].axisTitle.attr({ text: indicator1.bold() }) ;
	chart.yAxis[0].axisTitle.attr({ text: indicator2.bold() }) ;
	chart.setTitle({ text: 'Complete multigroup for two indicators' });
	chart.redraw();
}

// Update text box with new data
function updateTextBox(data)
{
	/*
	$("#data-table2").val("");
	for (j in data) {
		$("#data-table2").val( $("#data-table2").val() + "dates: " + data[j].dates + "\n");
		$("#data-table2").val( $("#data-table2").val() + "x_ind: " + data[j].x_ind.data + "\n");
		$("#data-table2").val( $("#data-table2").val() + "y_ind: " + data[j].y_ind.data + "\n");
	}
	*/
	
	// CSV format
	$("#data-table1").val("code x y date\n");
	for (j in data) {
	
		var code = data[j].code;
		var x = data[j].x_ind;
		var y = data[j].y_ind;
		var dates = data[j].dates;
		
		for (i in x.data) {
			$("#data-table1").val( $("#data-table1").val() + code + " " + x.data[i] + " " + y.data[i] + " " + dates[i] + "\n");
			//$("#data-table1").val( $("#data-table1").val() + code + "\t\t" + x.data[i] + "\t\t" + y.data[i] + "\t\t" + dates[i] + "\n");
		}
	}
	
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            defaultSeriesType: 'scatter',
            events: {
                load: requestData
            },
			showAxes: true,
        },
        title: {
            text: ' '
        },
        xAxis: {
            tickPixelInterval: 150,
            maxZoom: 50,
            title: {
			    //margin: 80,
				text: ' '
			},
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                //margin: 80,
				text: ' '
            }
        },
		
		//Tooltips showing indicator values.
		/*tooltip: {
			formatter: function() {
					// This callback function is called after the chart is loaded and data defined!
					return data[0].x_ind.code.bold() + ':' + this.x.toFixed(2) + '  ' + data[0].y_ind.code.bold() + ': ' + this.y.toFixed(2);
			}
		},
		*/
		
		// Tooltip showing date.
		tooltip: {
			formatter: function() {
					return this.point.date;
			}
		},
		
    });        
});

