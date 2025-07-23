import React, { useState } from 'react';
import { Input, Button, Card, message, Space, Divider, Row, Col } from 'antd';
import axios from 'axios';

const RequestPage = () => {
  const [inputValue, setInputValue] = useState('');
  const [bodyValue, setBodyValue] = useState('');
  const [paramValue, setParamValue] = useState('');
  const [getResponse, setGetResponse] = useState(null);
  const [postResponse, setPostResponse] = useState(null);
  const [getLoading, setGetLoading] = useState(false);
  const [postLoading, setPostLoading] = useState(false);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleBodyValueChange = (e) => {
    setBodyValue(e.target.value);
  };

  const handleParamValueChange = (e) => {
    setParamValue(e.target.value);
  };

  const handleGetSubmit = async () => {
    if (!inputValue.trim()) {
      message.warning('请输入参数');
      return;
    }

    setGetLoading(true);
    try {
      const result = await axios.get(`http://localhost:5000/api/get-data?input_value=${inputValue}`);
      setGetResponse(result.data);
      message.success('GET请求成功');
    } catch (error) {
      console.error('GET请求失败:', error);
      message.error('GET请求失败，请查看控制台');
    } finally {
      setGetLoading(false);
    }
  };

  const handlePostSubmit = async () => {
    if (!bodyValue.trim() || !paramValue.trim()) {
      message.warning('请输入Body参数和Param参数');
      return;
    }

    setPostLoading(true);
    try {
      const result = await axios.post(
        `http://localhost:5000/api/post-data?param_value=${paramValue}`,
        { body_value: bodyValue }
      );
      setPostResponse(result.data);
      message.success('POST请求成功');
    } catch (error) {
      console.error('POST请求失败:', error);
      message.error('POST请求失败，请查看控制台');
    } finally {
      setPostLoading(false);
    }
  };

  return (
    <div className="request-page">
      <h2 style={{ marginBottom: '20px', borderBottom: '1px solid #eee', paddingBottom: '10px' }}>参数传递</h2>
      
      {/* GET请求部分 */}
      <div style={{ marginBottom: 30, background: '#f9f9f9', padding: '20px', borderRadius: '5px' }}>
        <h3 style={{ marginBottom: '15px' }}>GET请求</h3>
        <Row gutter={16}>
          <Col xs={24} sm={16}>
            <Input
              placeholder="请输入GET参数"
              value={inputValue}
              onChange={handleInputChange}
              style={{ width: '100%', marginBottom: '10px' }}
            />
          </Col>
          <Col xs={24} sm={8}>
            <Button 
              type="primary" 
              onClick={handleGetSubmit} 
              loading={getLoading}
              style={{ width: '100%' }}
            >
              发送GET请求
            </Button>
          </Col>
        </Row>
        
        {getResponse && (
          <Card 
            title="GET响应结果" 
            style={{ marginTop: 16, boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}
          >
            <p><strong>状态码:</strong> {getResponse.status}</p>
            <p><strong>消息:</strong> {getResponse.message}</p>
            <p><strong>数据:</strong> {getResponse.data}</p>
          </Card>
        )}
      </div>
      
      <Divider />
      
      {/* POST请求部分 */}
      <div style={{ marginBottom: 30, background: '#f9f9f9', padding: '20px', borderRadius: '5px' }}>
        <h3 style={{ marginBottom: '15px' }}>POST请求</h3>
        <Row gutter={[16, 16]}>
          <Col span={24}>
            <Input
              placeholder="请输入Body参数"
              value={bodyValue}
              onChange={handleBodyValueChange}
              style={{ width: '100%' }}
            />
          </Col>
          <Col span={24}>
            <Input
              placeholder="请输入Param参数"
              value={paramValue}
              onChange={handleParamValueChange}
              style={{ width: '100%' }}
            />
          </Col>
          <Col span={24}>
            <Button 
              type="primary" 
              onClick={handlePostSubmit} 
              loading={postLoading}
              style={{ width: '100%' }}
            >
              发送POST请求
            </Button>
          </Col>
        </Row>
        
        {postResponse && (
          <Card 
            title="POST响应结果" 
            style={{ marginTop: 16, boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}
          >
            <p><strong>状态码:</strong> {postResponse.status}</p>
            <p><strong>消息:</strong> {postResponse.message}</p>
            <p><strong>Body参数:</strong> {postResponse.data.body}</p>
            <p><strong>Param参数:</strong> {postResponse.data.param}</p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default RequestPage; 