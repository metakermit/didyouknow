
var chart; // global
var data; // DATA IS DEFINED AFTER AJAX REQUEST, SO DOES IT MAKE SENSE TO CALL IT WHILE DEFINING CHART? 

var indicator = 'asdasdasd'

/**
 * Request data from the server, add it to the graph and set a timeout to request again
 */


function requestData() {
    $.ajax({
        url: '/getdata/',
        success: function(focData) {
			data = focData;
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is longer than 20
			var country = focData[0];
			var x_ind = country.x_ind;
			var y_ind = country.y_ind;
			for (i in x_ind.data) {
				chart.series[0].addPoint([x_ind.data[i], y_ind.data[i]], true, false);
			}
            // add the point
            //chart.series[0].addPoint(point, true, shift);
			
			updatePlot();
            
            // call it again after one second
            //setTimeout(requestData, 1000);    
        },
        cache: false
    });
}


function updatePlot()
{
	chart.xAxis[0].axisTitle.attr({ text: data[0].x_ind.code.bold() }) ;
	chart.yAxis[0].axisTitle.attr({ text: data[0].y_ind.code.bold() }) ;
	// Alternative:  $(chart.yAxis[0].axisTitle.element).text('New Label');
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'container',
            defaultSeriesType: 'scatter',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Live random data'
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
        series: [{
            name: 'Random data',
            data: []
        }]
    });        
});

