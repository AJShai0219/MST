const { devServer } = require('customize-cra');

module.exports = {
  devServer: function(configFunction) {
    return function(proxy, allowedHost) {
      const config = configFunction(proxy, allowedHost);
      config.allowedHosts = ['localhost', '127.0.0.1', '.localhost'];
      return config;
    };
  }
}; 