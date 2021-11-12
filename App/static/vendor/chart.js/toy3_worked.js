var chart = null;
// var mycharts;

$(document).ready(function(){
// function my_chart(response) {
    // $('#data-container').highcharts({
        chart = Highcharts.chart('data-container', {
        chart: { renderTo: 'data-container',
           defaultSeriesType: 'spline',
        //    animation: false
           events: {
               load: fetchdata
           }
        },
        title: {
            text: 'Live Reddit Stream'
        },
        xAxis: {//{ type: 'datetime',
                 //categories: response['halfhour']

        },
        yAxis: {
        minPadding: 0.2,
        maxPadding: 0.2,
        title: {text: 'Value',
                margin: 80}
         },
        series: [{
            name: 'reddit_stream',
            data: []//response['count']
        }]
    });
});


// $(
    function fetchdata() {
        $.ajax({
            url: '/fetch_data',
            type:'POST',
            dataType: '',
            success: function(output_string){
            //call my_chart function

            var series = chart.series[0]

                // shift = series.data.length > 20;

            chart.series[0]= output_string.count


            // var parsed_response = jQuery.parseJSON(output_string);

            // chart.series[0].data[0].update(output_string)

            // var series = chart.series[0],

            // shift = series.data.length > 20;

            // chart.series[0].addPoint(output_string);

            // chart.series.addPoint(output_string, true, shift);

            // console.log(output_string);

            // my_chart(output_string);
            
            },
            
            complete:function(output_string){
                setTimeout(fetchdata,5000);
            },

            error: function (xhr, ajaxOptions, thrownError){
                console.log(xhr.statusText);
                console.log(thrownError);
            }
    });
}
// });
