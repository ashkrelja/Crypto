<script>

function my_chart(response) {
    $('#data-container').highcharts({
        chart: { renderTo: 'data-container',
           defaultSeriesType: 'spline'
        },
        title: {
            text: 'Live Reddit Stream'
        },
        xAxis: {accessibility: {
                rangeDescription: 'Range: 1 to 94'
            }
        },
        yAxis: {
        minPadding: 0.2,
        maxPadding: 0.2,
        title: {text: 'Value',
                margin: 80}
         },
        series: [{
            name: 'reddit_stream',
            data: response
        }]
    });
}


$(function fetchdata() {
        $.ajax({
            url: '/fetch_data',
            type:'POST',
            dataType: '',
            success: function(output_string){
            //call my_chart function
            // var parsed_response = jQuery.parseJSON(output_string);

            var series = chart.series[0],

            shift = series.data.length > 20;

            chart.series[0].addPoint(output_string, true, shift);

            console.log(output_string);
            my_chart(output_string);
            
            },
            
            complete:function(output_string){
                setTimeout(fetchdata,5000);
            },

            error: function (xhr, ajaxOptions, thrownError){
                console.log(xhr.statusText);
                console.log(thrownError);
            }
    });
});

</script>