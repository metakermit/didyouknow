
var chart; // global
var data; // DATA IS DEFINED AFTER AJAX REQUEST, SO DOES IT MAKE SENSE TO CALL IT WHILE DEFINING CHART? 

var c = ['BRA','ISL']

/**
 * Request data from the server, add it to the graph and set a timeout to request again
 */

// $.ajax("../getdata/", {data: {countries:["HRV","USA"]}})

function requestData2() {
	$.ajax({
		url: "../getdata/", 
		data: {
			countries: $("select").val()
		},
		success: function(focData) {
			data = focData;
			
			// Remove all series from chart
			while (chart.series.length > 0)
			{
				chart.series[0].remove();
			}
			
			for (j in data) {
				var seriesOptions = {
					name: data[j].code,
					data: []
				};
				chart.addSeries(seriesOptions, true);
				var series = chart.series[j], shift = series.data.length > 20; // shift if the series is longer than 20
				var country = focData[j];
				var x_ind = country.x_ind;
				var y_ind = country.y_ind;
				for (i in x_ind.data) {
					chart.series[j].addPoint([x_ind.data[i], y_ind.data[i]], true, false); // [x,y],redraw,shift
				}
			}
			updatePlot();
        },
		cache: false,
	});
}

function requestData() {
    $.ajax({
        url: '/getdata/',
		data: {
			countries: ["BRA", "ITA"]
		},
        success: function(focData) {
			data = focData;
			for (j in data) {
				var seriesOptions = {
					name: data[j].code,
					data: []
				};
				chart.addSeries(seriesOptions, true);
				var series = chart.series[j], shift = series.data.length > 20; // shift if the series is longer than 20
				var country = focData[j];
				var x_ind = country.x_ind;
				var y_ind = country.y_ind;
				for (i in x_ind.data) {
					chart.series[j].addPoint([x_ind.data[i], y_ind.data[i]], true, false); // [x,y],redraw,shift
				}
			}
			updatePlot();
        },
        cache: false
    });
}


// Update labels according to fetched indicators.
function updatePlot()
{
	chart.xAxis[0].axisTitle.attr({ text: data[0].x_ind.code.bold() }) ;
	chart.yAxis[0].axisTitle.attr({ text: data[0].y_ind.code.bold() }) ;
	// Alternative:  $(chart.yAxis[0].axisTitle.element).text('New Label');
	
	chart.setTitle({ text: 'Complete multigroup for two indicators' });
	
}



$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            defaultSeriesType: 'line',
            events: {
                load: requestData
            }
        },
        title: {
            text: ' '
        },
        xAxis: {
            tickPixelInterval: 150,
            maxZoom: 50,
            title: {
			    //margin: 80,
				text: 'x'
			},
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                //margin: 80,
				text: 'y'
            }
        },
		tooltip: {
			formatter: function() {
					// This callback function is called after the chart is loaded and data defined!
					//return 'x'.bold() + ':' + this.x.toFixed(2) + ', ' + 'y'.bold() + ': ' + this.y.toFixed(2);
					return data[0].x_ind.code.bold() + ':' + this.x.toFixed(2) + '  ' + data[0].y_ind.code.bold() + ': ' + this.y.toFixed(2);
			}
		},
		//series: [],
        //series: [{
        //    name: '',
        //    data: []
        //}]
    });        
});

