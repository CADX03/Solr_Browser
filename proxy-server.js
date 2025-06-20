const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

app.use('/solr', createProxyMiddleware({
    target: 'http://localhost:8983',
    changeOrigin: true,
    pathRewrite: { '^/solr': '/solr' },
}));

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Proxy server running on http://localhost:${PORT}`);
});