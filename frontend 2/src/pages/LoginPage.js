import React from 'react';
import { Form, Input, Button, Card, message } from 'antd';
import { useNavigate } from 'react-router-dom';

function LoginPage({ setUser }) {
  const navigate = useNavigate();

  const onFinish = (values) => {
    // 模拟后端验证
    if (values.username && values.password) {
      const userData = { username: values.username };
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);
      message.success('登录成功');
      navigate('/');
    } else {
      message.error('请输入用户名和密码');
    }
  };

  return (
    <Card title="登录" style={{ maxWidth: 400, margin: '0 auto', marginTop: '50px' }}>
      <Form name="login" onFinish={onFinish}>
        <Form.Item
          name="username"
          rules={[{ required: true, message: '请输入用户名!' }]}
        >
          <Input placeholder="用户名" />
        </Form.Item>

        <Form.Item
          name="password"
          rules={[{ required: true, message: '请输入密码!' }]}
        >
          <Input.Password placeholder="密码" />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" block>
            登录
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
}

export default LoginPage;
