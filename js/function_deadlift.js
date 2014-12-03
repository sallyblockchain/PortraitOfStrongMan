$( document ).ready( function() {
    var options = {
        chart: {
            renderTo: 'container',
            type: 'line',
            zoomType: 'x'
        }, 
        title: {
            text: 'Data Visualization for Training and Competition Data of Powerlifting \
                        and Strongman from 2012 to 2014 - Deadlift'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' :
                    'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime',
            title: {
                text: 'Date'
            },
            minRange: 5 * 24 * 3600000 // 5 days
        }, 
        yAxis: {
            title: {
                text: 'Weight (pounds)'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [0.5, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                marker: {
                    radius: 0.5
                },
                lineWidth: 0.5,
                states: {
                    hover: {
                        lineWidth: 0.5
                    }
                }, 
                threshold: null
            },
            series: {
                cursor: 'pointer',
                point: {
                    events: {
                        click: function () {
                            if(this.options.url != undefined) {
                                location.href = this.options.url;
                            }  
                        }
                    }
                }
            }
        },
        tooltip: {
            pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.y}</b><br/>',
            crosshairs: true,
            shared: true
        }, 
        series: []
    };

    $.get('data/deadlift.csv', function(data) {
        // split the lines
        var lines = data.split('\n');
        //console.log(lines);
        var names = [];
        var jordan = {
            data: [],

        }
        var steve = {
            data: []
        }
        var isaak = {
            data: []
        }
        $.each(lines, function(lineNo, line) {
            var items = line.split(',');

            // header line contains categories
            var currDate = null;
            if(lineNo == 0) {
                $.each(items, function(itemNo, item) {
                    item = item.replace(/"/g, ""); 
                    if(itemNo > 0) names.push(item);
                });
                //console.log(actions);

            } else {
                $.each(items, function(itemNo, item) {
                    if(itemNo == 0) {
                        item = item.replace(/"/g, "");
                      
                        var dateString = item.split('-');
                        var year = parseInt(dateString[2]); // 2012-2014
                        var month = parseInt(dateString[0]) - 1; // months: 0-based index
                        var day = parseInt(dateString[1]);
                        currDate = Date.UTC(year, month, day);
                        
                    } else {
                        if(itemNo == 1) {
                            if(jordan.name == null) {
                                jordan.name = names[0];
                            } 
                            if(item != "x") {
                                jordan.data.push( [currDate, parseFloat(item)] );
                            }       
                        } else if (itemNo == 2) {
                            if(steve.name == null) {
                                steve.name = names[1];
                            }
                            if(item != "x") {
                                steve.data.push( [currDate, parseFloat(item)] );
                            }

                        } else {
                            if(isaak.name == null) {
                                isaak.name = names[2];
                            }
                            if(item != "x") {
                                isaak.data.push( [currDate, parseFloat(item)] );
                            }
                        } 
                    }
                }); // end of .each
            }
        }); 

        options.series.push(jordan);
        options.series.push(steve);
        options.series.push(isaak);
        var chart = new Highcharts.Chart(options);
    });   
});