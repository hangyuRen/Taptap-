function initChartRate(divId){
     var dom = document.getElementById(divId);
    var myChart = echarts.init(dom, null, {
      renderer: 'canvas',
      useDirtyRect: false
    });
    var app = {};

    var option;

    option = {
  title: {
    text: 'IOS/Android热门榜各评分区间游戏数'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {},
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'value',
    boundaryGap: [0, 0.01]
  },
  yAxis: {
    type: 'category',
    data: xLabel
  },
  series: [
    {
      name: 'IOS',
      type: 'bar',
      data: iosRate
    },
    {
      name: 'Android',
      type: 'bar',
      data: androidRate
    }
  ]
};

    if (option && typeof option === 'object') {
      myChart.setOption(option);
    }

    window.addEventListener('resize', myChart.resize);
}