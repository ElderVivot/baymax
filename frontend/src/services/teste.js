const prepareUrls = require('local-ip-url/prepareUrls');

const teste = prepareUrls({
  protocol: 'http',
  host: '0.0.0.0',
  port: 3001
});

console.log(teste)