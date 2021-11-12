$(document).ready(function(){

    //////////////////////////////////////////////////

        function my_chart(response){
        const chart = Highcharts.chart('chart-areaid', {
            chart: { renderTo: 'chart-areaid',
            defaultSeriesType: 'spline'
            }, 
            title: {
                text: 'Live Reddit Stream'
            },
            xAxis: { type: 'datetime',
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
                animation: false,
                data: response.count
            }]
        });
        }

    $(function fetchdata() {
            $.ajax({
                url: '/reddit_line_data',
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
//////////////////////////////////////////////////

