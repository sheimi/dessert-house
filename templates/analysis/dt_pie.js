  $(document).ready(function() {
     var  chart = new Highcharts.Chart({
        chart:  {
                  renderTo: 'chart-container',
                  plotBackgroundColor: null,
                  backgroundColor: null,
                  plotBorderWidth: null,
                  plotShadow: false
                },
        title:  {
                  text: 'Dessert Share Chart',
                },
        tooltip: {
                  formatter: function() {
                      return '<b>'+ this.point.name +'</b>: '
                          + this.percentage + ' %';
                  }
                },
        plotOptions:  {
          pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                                    enabled: true,
                                    color: '#000000',
                                    connectorColor: '#000000',
                                    formatter: function() {
                                      return '<b>'+ this.point.name 
                                        +'</b>: '
                                        + this.percentage +' %';
                                    }
                                }
               }
                      },
      series: [{
                  type: 'pie',
                  name: 'Dessert Share',
                  data: [
                    /*
                            ['Ice Cream', 34.0],
                            ['Cake',        33.0],
                            {  
                                name : 'Fruit',
                                y: 33.0,
                                sliced: true,
                                selected: true
                            }
                            */
{% for key, value  in datas.data.iteritems() %}
  ['{{key}}', {{value * 100 / datas.sum}}]
  {%if not loop.last %}
  ,
  {%endif%}
{% endfor %}
                        ]
              }]
      })
})
