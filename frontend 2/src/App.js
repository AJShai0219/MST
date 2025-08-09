import React, { useState, useEffect } from 'react';
import { Layout, Menu, Typography, Button, Dropdown } from 'antd';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { UserOutlined, LogoutOutlined } from '@ant-design/icons';
import RequestPage from './pages/GetRequestPage';
import ChartsPage from './pages/ChartsPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DigitUploadPage from './pages/DigitUploadPage';
import './App.css';

const { Header, Content, Footer, Sider } = Layout;
const { Title } = Typography;

function App() {
  const [user, setUser] = useState(null);

  // 从 localStorage 读取登录信息
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  // 退出登录
  const handleLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        {/* 顶部导航 */}
        <Header className="header" style={{ padding: '0 20px', display: 'flex', justifyContent: 'space-between' }}>
          <Title level={3} style={{ color: 'white', margin: '12px 0' }}>前后端交互系统</Title>

          {user ? (
            <Dropdown
              menu={{
                items: [
                  {
                    key: 'logout',
                    label: '退出登录',
                    icon: <LogoutOutlined />,
                    onClick: handleLogout,
                  },
                ],
              }}
            >
              <Button type="text" style={{ color: 'white' }} icon={<UserOutlined />}>
                {user.username}
              </Button>
            </Dropdown>
          ) : (
            <div>
              <Link to="/login"><Button type="link" style={{ color: 'white' }}>登录</Button></Link>
              <Link to="/register"><Button type="link" style={{ color: 'white' }}>注册</Button></Link>
            </div>
          )}
        </Header>

        {/* 左侧菜单 + 内容 */}
        <Layout>
          <Sider width={200} className="site-layout-background" style={{ boxShadow: '2px 0 6px rgba(0,0,0,0.1)' }}>
            <Menu
              mode="inline"
              defaultSelectedKeys={['1']}
              style={{
                height: '100%',
                borderRight: 0,
                fontWeight: '500'
              }}
            >
              <Menu.Item key="1" style={{ marginTop: '20px' }}>
                <Link to="/">参数传递</Link>
              </Menu.Item>
              <Menu.Item key="2">
                <Link to="/charts">数据可视化图表</Link>
              </Menu.Item>
              <Menu.Item key="5">
                <Link to="/digit-upload">手写数字识别</Link>
              </Menu.Item>
            </Menu>
          </Sider>

          <Layout style={{ padding: '24px' }}>
            <Content
              className="site-layout-background"
              style={{
                padding: 24,
                margin: 0,
                minHeight: 280,
                background: '#fff',
                borderRadius: '5px',
                boxShadow: '0 1px 4px rgba(0,0,0,0.08)'
              }}
            >
              <Routes>
                <Route path="/" element={<RequestPage />} />
                <Route path="/charts" element={<ChartsPage />} />
                <Route path="/login" element={<LoginPage setUser={setUser} />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/digit-upload" element={<DigitUploadPage />} />
              </Routes>
            </Content>
            <Footer style={{ textAlign: 'center', color: '#888' }}>
              前后端交互系统 ©2025
            </Footer>
          </Layout>
        </Layout>
      </Layout>
    </Router>
  );
}

export default App;
