$(document).ready(function() {
    var chart = new Highcharts.Chart({
      chart: {
        renderTo: 'chart-container',
        defaultSeriersType: 'line',
        backgroundColor: null,
        marginRight: 130,
        marginBottom: 25
      }
      , title: {
        text: '{{title}}',
        x: -20
      }
      , xAxis: {
        categories: [
          {% for item in items %}
            '{{item[1].key}}'
            {% if not loop.last %}
              ,
            {% endif %}
          {% endfor %}
        ]
      }
      , yAxis: {
        title: { text: 'income'},
        plotLines: [{
          value: 0,
          width: 1,
          color: '#808080'
        }]
      }
      , legend: {
          layout: 'vertical',
          align: 'right',
          verticalAlign: 'top',
          x: -10,
          y: 100,
          borderWidth: 0
      }
      , tooltip: {
          formatter: function() {
              return '<b>'+ this.series.name +'</b><br/>'+
                          this.x +':  $'+ this.y;
            }
      }
      , series: [{
              name: 'General',
              data: [
                {% for item in items %}
                  {{item[1].num}}
                  {% if not loop.last %}
                    ,
                  {% endif %}
                {% endfor %}
              ],
              marker: {symbol: 'square'}
            }
        {% if linear %}
        , {
          type: 'line'
          , name: 'Line'
          , data: 
            {{linear}}
          , marker: {
          }
          , states: {
            hover: {
              lineWidth: 0
            }
          }
          , enableMouseTracking: false
        }
        {% else %}
        yyy
        {% endif %}
      ]
  })
})
