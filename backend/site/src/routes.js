const express = require('express')

const IntegrattionLayoutController = require('./controllers/IntegrattionLayoutController')
const IntegrattionCompaniesController = require('./controllers/IntegrattionCompaniesController')
const ExtractCompaniesController = require('./controllers/ExtractCompaniesController')

// routes cria as rotas
const routes = express.Router()

// rotas do integrattion_layouts
routes.get('/integrattion_layouts', IntegrattionLayoutController.index)
routes.get('/integrattion_layouts/:id', IntegrattionLayoutController.show)
routes.post('/integrattion_layouts', IntegrattionLayoutController.store)
routes.put('/integrattion_layouts/:id', IntegrattionLayoutController.update)
routes.delete('/integrattion_layouts/:id', IntegrattionLayoutController.delete)

// rotas do integrattion_companies
routes.post('/integrattion_companies', IntegrattionCompaniesController.store)

// rotas do extract_companies
routes.get('/extract_companies', ExtractCompaniesController.index)

// exportando as rotas
module.exports = routes