const express = require('express')

const IntegrattionLayoutController = require('./controllers/IntegrattionLayoutController')

// routes cria as rotas
const routes = express.Router()

routes.get('/integrattion_layouts', IntegrattionLayoutController.index)
routes.get('/integrattion_layouts/:id', IntegrattionLayoutController.show)
routes.post('/integrattion_layouts', IntegrattionLayoutController.store)
routes.post('/integrattion_layouts/:id', IntegrattionLayoutController.update)

// exportando as rotas
module.exports = routes