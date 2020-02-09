const express = require('express')

const IntegrattionLayoutController = require('./controllers/IntegrattionLayoutController')

// routes cria as rotas
const routes = express.Router()

routes.post('/integrattion_layouts', IntegrattionLayoutController.store)

// exportando as rotas
module.exports = routes