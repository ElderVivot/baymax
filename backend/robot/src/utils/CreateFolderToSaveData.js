const fs = require('fs')
const path = require('path')

const createFolderToSaveData = (settings) => {
    // estrutura de pastas será:
    // 1 - caminho base ('C:/notas_fiscais/goiania')
    // 2 - dateHourProcessing
    // 3 - tipo (error, warning, sucess)
    // 4 - loguin
    // 5 - empresa (opcional)
    // Exemplo final: C:/notas_fiscais/goiania/data_hora/sucess/CPF/Empresa

    let wayToSave = 'C:/notas_fiscais/goiania'
    fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)

    const dateHourProcessing = settings.dateHourProcessing
    wayToSave = path.join(wayToSave, dateHourProcessing)
    fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)    
    
    const type = settings.type
    wayToSave = path.join(wayToSave, type)
    fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)
    
    const loguin = settings.loguin
    wayToSave = path.join(wayToSave, loguin)
    fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)    
  
    const labelEmpresa = settings.labelEmpresa
    if(labelEmpresa !== undefined){
        wayToSave = path.join(wayToSave, labelEmpresa)
        fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)

        // const cpfCnpj = settings.cpfCnpj
        // if(cpfCnpj !== undefined){
        //     wayToSave = path.join(wayToSave, cpfCnpj)
        //     fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)
        // }
    }
  
    return wayToSave
  }

  module.exports = createFolderToSaveData