const { CronJob } = require('cron')
const { api } = require('../../../../../frontend/src/services/api')
const SettingsCompaniesSettings = require('../../../../../frontend/src/services/SettingsCompaniesSettings')

async function loadCompaniesSettings() {
    console.log('- [CompaniesSettingsView] - Iniciando busca das empresas às ', new Date())
    let dataSettingsCompaniesSettings = []
    try {
        const settingsCompaniesSettings = new SettingsCompaniesSettings()
        dataSettingsCompaniesSettings = await settingsCompaniesSettings.process()
        console.log(`- [CompaniesSettingsView] - Encontrado ${dataSettingsCompaniesSettings.length} empresas`)
        
        await api.delete('/companies_settings_view')
        await api.post('/companies_settings_view', dataSettingsCompaniesSettings )
        console.log(`- [CompaniesSettingsView] - Salvo empresas no banco de dados`)
    } catch (error) {
        console.log('- [CompaniesSettingsView]', error)
    }
    return dataSettingsCompaniesSettings
}

const job = new CronJob(
	'*/5 * * * *',
	async function (){
        await loadCompaniesSettings()
    },
	null,
	true,
	'America/Sao_Paulo'
)

module.exports = job