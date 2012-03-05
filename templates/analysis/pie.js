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
                  text: '{{title}}',
                },
        tooltip: {
                  formatter: function() {
                      return '<b>'+ this.point.name +'</b>: '
                          + Math.round(this.percentage) + ' %';
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
                                        + Math.round(this.percentage) +' %';
                                    }
                                }
               }
                      },
      series: [{
                  type: 'pie',
                  name: 'Dessert Share',
                  data: [
{% for key, value  in datas.data.iteritems() %}
  {% if loop.first %}
  {
    name : '{{key}}', 
    y : {{value}},
    sliced: true,
    selected: true
  }
  {% else %}
  ['{{key}}', {{value}}]
  {% endif %}
  {%if not loop.last %}
  ,
  {%endif%}
{% endfor %}
                        ]
              }]
      })
})
