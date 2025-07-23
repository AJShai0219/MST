const path = require('path');
const { merge } = require('webpack-merge');

module.exports = {
  devServer: {
    allowedHosts: ['localhost', '127.0.0.1'],
    host: 'localhost',
    port: 3000,
    open: true
  }
}; 