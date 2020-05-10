const express = require('express')

const IntegrattionLayoutController = require('./controllers/IntegrattionLayoutController')
const IntegrattionCompaniesController = require('./controllers/IntegrattionCompaniesController')
const ExtractCompaniesController = require('./controllers/ExtractCompaniesController')
const ExtractCompaniesMovementsController = require('./controllers/ExtractCompaniesMovementsController')
const CompaniesSettingsController = require('./controllers/CompaniesSettingsController')

// routes cria as rotas
const routes = express.Router()

// rotas do integrattion_layouts
routes.get('/integrattion_layouts', IntegrattionLayoutController.index)
routes.get('/integrattion_layouts/:id', IntegrattionLayoutController.show)
routes.post('/integrattion_layouts', IntegrattionLayoutController.store)
routes.put('/integrattion_layouts/:id', IntegrattionLayoutController.update)
routes.delete('/integrattion_layouts/:id', IntegrattionLayoutController.delete)

// rotas do integrattion_companies
routes.get('/integrattion_companies', IntegrattionCompaniesController.index)
routes.get('/integrattion_companies/:id', IntegrattionCompaniesController.show)
routes.post('/integrattion_companies', IntegrattionCompaniesController.store)
routes.put('/integrattion_companies/:id', IntegrattionCompaniesController.update)
routes.delete('/integrattion_companies/:id', IntegrattionCompaniesController.delete)

// rotas do extract_companies
routes.get('/extract_companies', ExtractCompaniesController.index)

// rotas do extract_companies_movements
routes.get('/extract_companies_movements', ExtractCompaniesMovementsController.index)

// rotas do companies_settings
routes.get('/companies_settings', CompaniesSettingsController.index)
routes.get('/companies_settings/:codi_emp', CompaniesSettingsController.show)
routes.post('/companies_settings', CompaniesSettingsController.store)
routes.put('/companies_settings/:codi_emp', CompaniesSettingsController.update)

// exportando as rotas
module.exports = routes