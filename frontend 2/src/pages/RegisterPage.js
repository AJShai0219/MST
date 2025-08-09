import React from 'react';
import { Form, Input, Button, Typography, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';

const { Title } = Typography;

const RegisterPage = () => {
  const navigate = useNavigate();

  const onFinish = async (values) => {
    if (values.password !== values.confirm) {
      return message.error('两次密码不一致');
    }

    try {
      await api.post('/register', {
        username: values.username,    // 改为 username
        password: values.password,
        confirm: values.confirm       // 记得传confirm给后端
      });
      message.success('注册成功，请登录');
      navigate('/login');
    } catch (err) {
      message.error('注册失败: ' + (err.response?.data?.message || err.message));
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '50px auto', padding: 24, border: '1px solid #eee', borderRadius: 8 }}>
      <Title level={3} style={{ textAlign: 'center' }}>注册</Title>
      <Form layout="vertical" onFinish={onFinish}>
        <Form.Item
          label="用户名"
          name="username"
          rules={[{ required: true, message: '请输入用户名' }]}
        >
          <Input placeholder="请输入用户名" />
        </Form.Item>
        <Form.Item
          label="密码"
          name="password"
          rules={[{ required: true, message: '请输入密码' }]}
        >
          <Input.Password placeholder="请输入密码" />
        </Form.Item>
        <Form.Item
          label="确认密码"
          name="confirm"
          rules={[{ required: true, message: '请再次输入密码' }]}
        >
          <Input.Password placeholder="请再次输入密码" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" block>
            注册
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default RegisterPage;
