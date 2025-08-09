import React, { useState, useEffect } from 'react';
import { Radio, Card, Spin, Alert } from 'antd';
import ReactEcharts from 'echarts-for-react';
import axios from 'axios';

const ChartsPage = () => {
  const [chartType, setChartType] = useState('bar');
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchChartData(chartType);
  }, [chartType]);

  const fetchChartData = async (type) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`http://localhost:5000/api/chart-data?chart_type=${type}`);
      setChartData(response.data.data);
    } catch (err) {
      console.error('获取图表数据失败:', err);
      setError('获取图表数据失败，请检查后端服务是否启动');
    } finally {
      setLoading(false);
    }
  };

  const handleChartTypeChange = (e) => {
    setChartType(e.target.value);
  };

  const getOption = () => {
    if (!chartData) return {};

    const { xAxis, series, chartType } = chartData;

    if (chartType === 'pie') {
      // 饼图配置
      return {
        title: {
          text: '饼图数据展示',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          data: xAxis
        },
        series: [
          {
            name: '数据',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: xAxis.map((name, index) => ({
              name,
              value: series[index]
            })),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
    } else {
      // 柱状图或折线图配置
      return {
        title: {
          text: chartType === 'bar' ? '柱状图数据展示' : '折线图数据展示',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: xAxis
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: series,
          type: chartType
        }]
      };
    }
  };

  return (
    <div className="charts-page">
      <h2 style={{ marginBottom: '20px', borderBottom: '1px solid #eee', paddingBottom: '10px' }}>数据可视化图表</h2>
      
      <div style={{ marginBottom: 24, textAlign: 'center' }}>
        <Radio.Group 
          value={chartType} 
          onChange={handleChartTypeChange} 
          buttonStyle="solid"
          size="large"
        >
          <Radio.Button value="bar">柱状图</Radio.Button>
          <Radio.Button value="line">折线图</Radio.Button>
          <Radio.Button value="pie">饼图</Radio.Button>
        </Radio.Group>
      </div>
      
      <Card 
        style={{ 
          marginTop: 16, 
          minHeight: 450, 
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          background: '#f9f9f9',
          borderRadius: '5px'
        }}
        bordered={false}
      >
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 350 }}>
            <Spin size="large" />
          </div>
        ) : error ? (
          <Alert message={error} type="error" showIcon />
        ) : chartData ? (
          <ReactEcharts 
            option={getOption()} 
            style={{ height: 400, marginTop: 20 }} 
          />
        ) : (
          <div style={{ textAlign: 'center', padding: 24 }}>没有图表数据</div>
        )}
      </Card>
    </div>
  );
};

export default ChartsPage; 