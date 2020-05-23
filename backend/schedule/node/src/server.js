const express = require('express')
const companiesSettings = require('./jobs/CompaniesSettings')

const app = express()

companiesSettings.start()

const port = 3005
app.listen(port, () => console.log(`Server Schedule-Node | Executing in port ${port} ...`))