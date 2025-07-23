import React from 'react';
import { Layout, Menu, Typography } from 'antd';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import RequestPage from './pages/GetRequestPage';
import ChartsPage from './pages/ChartsPage';
import './App.css';

const { Header, Content, Footer, Sider } = Layout;
const { Title } = Typography;

function App() {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Header className="header" style={{ padding: '0 20px' }}>
          <div className="logo"></div>
          <Title level={3} style={{ color: 'white', margin: '12px 0' }}>前后端交互系统</Title>
        </Header>
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
