
var chart; // global

/**
 * Request data from the server, add it to the graph and set a timeout to request again
 */


function requestData() {
    $.ajax({
        url: '/getdata/',
        success: function(focData) {
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
			
			
            
            // call it again after one second
            //setTimeout(requestData, 1000);    
        },
        cache: false
    });
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
            maxZoom: 50
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: 'Value',
                margin: 80
            }
        },
        series: [{
            name: 'Random data',
            data: []
        }]
    });        
});

