var chart;
var mycharts;

function requestData()
{
    var requests = $.get('/fetch_data');

    // console.log(requests)

    var tm = requests.done(function (result)
    {
        var series = chart.series[0],

        shift = series.data.length > 20;

        console.log(chart.data.length)

        chart.series[0].addPoint(result, true, shift);

        setTimeout(requestData, 2000);                

    }); 
}

$(document).ready(function() {

    chart = new Highcharts.Chart({
        chart: {renderTo: 'data-container',
                defaultSeriesType: 'spline',
                events: {
                    load: requestData
                }
            },
        title: {
            text: 'Live random data'
        },
        xAxis: {type: 'datetime',
                tickPixelInterval: 150,
                maxZoom: 20 * 1000},
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {text: 'Value',
                    margin: 80}
        },
        series: [{name: 'reddit_stream',
                  data: []
                }]
    });

})
