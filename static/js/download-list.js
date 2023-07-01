function initChartDownload(divId) {
    var dom = document.getElementById(divId);
    var myChart = echarts.init(dom, null, {
      renderer: 'canvas',
      useDirtyRect: false
    });
    var app = {};

    var option;

option = {
  // Make gradient line here
  visualMap: [
    {
      show: false,
      type: 'continuous',
      seriesIndex: 0,
      min: 0,
      max: 400
    },
    {
      show: false,
      type: 'continuous',
      seriesIndex: 1,
      dimension: 0,
      min: 0,
      max: iosGameNameByDownload.length - 1
    }
  ],
  title: [
    {
      left: 'center',
      text: 'IOS Download List'
    },
    {
      top: '55%',
      left: 'center',
      text: 'Android Download List'
    }
  ],
  tooltip: {
    trigger: 'axis'
  },
  xAxis: [
    {
      data: iosGameNameByDownload
    },
    {
      data: androidGameNameByDownload,
      gridIndex: 1
    }
  ],
  yAxis: [
    {},
    {
      gridIndex: 1
    }
  ],
  grid: [
    {
      bottom: '60%'
    },
    {
      top: '60%'
    }
  ],
  series: [
    {
      type: 'line',
      showSymbol: true,
      data: iosDownloadCount
    },
    {
      type: 'line',
      showSymbol: true,
      data: androidDownloadCount,
      xAxisIndex: 1,
      yAxisIndex: 1
    }
  ]
};

    if (option && typeof option === 'object') {
      myChart.setOption(option);
    }

    window.addEventListener('resize', myChart.resize);
}