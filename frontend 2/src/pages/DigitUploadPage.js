import React, { useState, useEffect } from 'react';
import { Upload, Button, Typography, message, Image, Spin, Alert } from 'antd';
import { UploadOutlined, LoginOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';

const { Title } = Typography;

const DigitUploadPage = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(true); // 默认已登录

  const navigate = useNavigate();

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (!user) {
      setIsLoggedIn(false); // 未登录状态
    }
  }, []);

  const beforeUpload = (file) => {
    const isImage = file.type.startsWith('image/');
    if (!isImage) {
      message.error('只能上传图片文件!');
      return Upload.LIST_IGNORE;
    }
    setFile(file);
    setPreview(URL.createObjectURL(file));
    return false;
  };

  const handleSubmit = async () => {
    if (!file) {
      message.error('请先选择图片');
      return;
    }
    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await api.post('/predict-digit', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setResult(res.data.result);
      message.success('预测完成');
    } catch (err) {
      message.error('上传失败: ' + (err.response?.data?.message || err.message));
    } finally {
      setLoading(false);
    }
  };

  if (!isLoggedIn) {
    return (
      <div style={{ maxWidth: 500, margin: '40px auto', padding: 24 }}>
        <Alert
          message="未登录"
          description="您需要先登录才能使用手写数字识别功能。"
          type="warning"
          showIcon
        />
        <Button
          type="primary"
          icon={<LoginOutlined />}
          style={{ marginTop: 20 }}
          block
          onClick={() => navigate('/login')}
        >
          去登录
        </Button>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 500, margin: '40px auto', padding: 24, border: '1px solid #eee', borderRadius: 8 }}>
      <Title level={3} style={{ textAlign: 'center' }}>手写数字识别</Title>

      <Upload beforeUpload={beforeUpload} showUploadList={false}>
        <Button icon={<UploadOutlined />}>选择图片</Button>
      </Upload>

      {preview && (
        <div style={{ marginTop: 20, textAlign: 'center' }}>
          <Image src={preview} alt="预览" style={{ maxHeight: 200 }} />
        </div>
      )}

      <Button
        type="primary"
        onClick={handleSubmit}
        disabled={!file || loading}
        block
        style={{ marginTop: 20 }}
      >
        {loading ? <Spin size="small" /> : '提交识别'}
      </Button>

      {result !== null && (
        <div style={{ marginTop: 20, textAlign: 'center' }}>
          <Title level={4}>预测结果: {result}</Title>
        </div>
      )}
    </div>
  );
};

export default DigitUploadPage;
