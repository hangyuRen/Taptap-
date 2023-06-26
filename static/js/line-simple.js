function initChart(divId) {
     var dom = document.getElementById('container');
    var myChart = echarts.init(dom, null, {
      renderer: 'canvas',
      useDirtyRect: false
    });
    var app = {};

    var option;

    option = {
  xAxis: {
    type: 'category',
    data: x_data
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: y_data,
      type: 'line'
    }
  ]
};

    if (option && typeof option === 'object') {
      myChart.setOption(option);
    }

    window.addEventListener('resize', myChart.resize);
}