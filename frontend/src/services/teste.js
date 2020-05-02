const axios = require('axios')

const api = axios.create({
    baseURL: 'http://localhost:3001'
})

async function testeAsyn(){
    try {
        const responseLayouts = await api.get(`/integrattion_layouts`)
        if(responseLayouts.statusText === "OK"){
            console.log('consegui pegar os layous primeiro')
        }

        const responseIntegrattionCompanies = await api.get(`/integrattion_companies`)
        if(responseIntegrattionCompanies.statusText === "OK"){
            console.log('consegui pegar as empresas primeiro')
        }

        console.log('eu depois')
    } catch (error) {
        console.log(error)
    }
}

testeAsyn()