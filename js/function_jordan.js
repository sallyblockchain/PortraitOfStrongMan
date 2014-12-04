$(document).ready(function() {
    var options = {
        chart: {
            renderTo: 'container',
            type: 'line',
            zoomType: 'x'
        }, 
        title: {
            text: 'Data Visualization for Training and Competition Data of Powerlifting \
                        and Strongman from 2012 to 2014 - Jordan'
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

    $.get('data/new_data.csv', function(data) {
        // split the lines
        var lines = data.split('\n');
        //console.log(lines);
        var actions = [];
        var bench = {
            data: [],

        }
        var squat = {
            data: []
        }
        var deadlift = {
            data: []
        }
        var bodyweight = {
            data: []
        }
        $.each(lines, function(lineNo, line) {
            var items = line.split(',');

            // header line contains categories
            var currDate = null;
            if(lineNo == 0) {
                $.each(items, function(itemNo, item) {
                    item = item.replace(/"/g, ""); 
                    if(itemNo > 0) actions.push(item);
                });

            } else {
                $.each(items, function(itemNo, item) {
                    if(itemNo == 0) {
                        var found = false;
                        item = item.replace(/"/g, "");
                        if(item == "07-13-13") {
                            found = true;
                        }
                        var dateString = item.split('-');
                        var year = parseInt("20" + dateString[2]); // 2012-2014
                        var month = parseInt(dateString[0]) - 1; // months: 0-based index
                        var day = parseInt(dateString[1]);
                        currDate = Date.UTC(year, month, day);
                        //if(found)
                        //    console.log(currDate);
                        
                    } else {
                        if(itemNo == 1) {
                            if(bench.name == null) {
                                bench.name = actions[0];
                            } 

                            bench.data.push( [currDate, parseFloat(item)] );
                            
                        } else if (itemNo == 2) {
                            if(squat.name == null) {
                                squat.name = actions[1];
                            }
                            if(currDate == 1373673600000) {
                                squat.data.push({
                                    x: currDate,
                                    y: parseFloat(item),
                                    marker: {
                                        symbol: 'url(images/strongman.png)'
                                    },
                                    url: 'https://www.youtube.com/watch?v=geEBvmYTA44'
                                });
                            } else {
                                squat.data.push( [currDate, parseFloat(item)] );
                            }
                         
                        } else if (itemNo == 3) {
                            if(deadlift.name == null) {
                                deadlift.name = actions[2];
                            }
                            if(currDate == 1402617600000) { // 06-13-14
                                deadlift.data.push( {
                                    x: currDate,
                                    y: parseFloat(item),
                                    marker: {
                                        symbol: 'url(images/strongman.png)'
                                    },
                                    url: 'https://www.youtube.com/watch?v=yLpOipCyGKs'
                                });
                            } else if (currDate == 1377820800000) { // 08-30-13
                                deadlift.data.push( {
                                    x: currDate,
                                    y: parseFloat(item),
                                    marker: {
                                        symbol: 'url(images/strongman.png)'
                                    },
                                    url: 'https://www.youtube.com/watch?v=TnXRXnGgu7c'
                                });
                            } else {
                                deadlift.data.push( [currDate, parseFloat(item)] );
                            }
                        } else {
                            if(bodyweight.name == null) {
                                bodyweight.name = actions[3];
                            }
                            bodyweight.data.push( [currDate, parseFloat(item)] );
                        }
                    }
                });
            }
        }); 

        options.series.push(bench);
        options.series.push(squat);
        options.series.push(deadlift);
        options.series.push(bodyweight);
        var chart = new Highcharts.Chart(options);
    });

    
});