function initChartAndroid(divId) {
  var dom = document.getElementById(divId);
  var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
  });

  var option;

  option = {
  legend: {
  top: 'bottom'
  },
  toolbox: {
  show: true,
  feature: {
    mark: { show: true },
    dataView: { show: true, readOnly: false },
    restore: { show: true },
    saveAsImage: { show: true }
  }
  },
  series: [
  {
    name: 'Nightingale Chart',
    type: 'pie',
    radius: [50, 250],
    center: ['50%', '50%'],
    roseType: 'area',
    itemStyle: {
      borderRadius: 8
    },
    data: androidDataList
  }
  ]};

if (option && typeof option === 'object') {
  myChart.setOption(option);
  }
  window.addEventListener('resize', myChart.resize);
}

