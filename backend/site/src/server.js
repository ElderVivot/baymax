const express = require('express')
const bodyParser = require('body-parser')
const mongoose = require('mongoose')
const cors = require('cors')

const routes = require('./routes')

const app = express()

mongoose.connect('mongodb://localhost/baymax', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: false,
    useCreateIndex: true
})

app.use(cors('*'))
// app.use(cors('http://localhost:3001'))
app.use(bodyParser.json({limit: '100mb'}))
app.use(bodyParser.urlencoded({ extended: false }))
app.use(routes)

const port = 3001
app.listen(port, () => console.log(`Executando na porta ${port} ...`))