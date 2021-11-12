$(document).ready(function(){

    function my_chart(response) {
        // $('#data-container').highcharts({
            chart = Highcharts.chart('data-container', {
            chart: { renderTo: 'data-container',
            defaultSeriesType: 'spline'
            //    animation: false
            //    events: {
            //        load: fetchdata
            //    }
            },
            title: {
                text: 'Live Reddit Stream'
            },
            xAxis: {//{ type: 'datetime',
                    categories: response.halfhour

            },
            yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {text: 'Value',
                    margin: 80}
            },
            series: [{
                name: 'reddit_stream',
                data: response.count
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

                my_chart(output_string);
                
                },
                
                complete:function(output_string){
                    setTimeout(fetchdata,10000);
                },

                error: function (xhr, ajaxOptions, thrownError){
                    console.log(xhr.statusText);
                    console.log(thrownError);
                }
            });
        });
});

