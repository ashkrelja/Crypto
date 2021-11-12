$(document).ready(function(){

    const options = {
        chart: { renderTo: 'chart-areaid',
        defaultSeriesType: 'spline'
        }, 
        title: {
            text: 'Live Reddit Stream'
        },
        xAxis: { type: 'datetime',
                categories: []

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
            data: []
        }]
    }
    const chart = Highcharts.chart('chart-areaid', options)
    

        // Data
    // const getData = () => {
        setInterval(() => {
            fetch('/reddit_line_data')
                .then( resp => resp.json())
                .then(data => {
                    chart.update({
                        xAxis: { categories: data.halfhour
                        },
                        series: [{
                            data: data.count
                        }]
                    }, true, false, false)
                    })
        }, 1000)
        // }
        // getData()
})