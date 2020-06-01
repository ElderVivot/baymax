const fs = require('fs')
const path = require('path')

const createFolderToSaveData = (settings) => {
    // estrutura de pastas será:
    // 1 - caminho base ('C:/notas_fiscais/goiania')
    // 2 - tipo (error, warning, sucess)
    // 3 - loguin
    // 4 - empresa (opcional)
    // 5 - dateHourProcessing
    // Exemplo final: C:/notas_fiscais/goiania/sucess/CPF/DIVIART/data_hora
    
    let wayToSave = 'C:/notas_fiscais/goiania'
    fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)

    const type = settings.type
    wayToSave = path.join(wayToSave, type)
    fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)
    
    const loguin = settings.loguin
    wayToSave = path.join(wayToSave, loguin)
    fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)    
  
    let labelEmpresa = settings.labelEmpresa
    if(labelEmpresa !== undefined){
        labelEmpresa = labelEmpresa.substring(0, 70)
        wayToSave = path.join(wayToSave, labelEmpresa)
        fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)

        // const cpfCnpj = settings.cpfCnpj
        // if(cpfCnpj !== undefined){
        //     wayToSave = path.join(wayToSave, cpfCnpj)
        //     fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)
        // }
    }

    const dateHourProcessing = settings.dateHourProcessing
    wayToSave = path.join(wayToSave, dateHourProcessing)
    fs.existsSync(wayToSave) || fs.mkdirSync(wayToSave)
  
    return wayToSave
  }

  module.exports = createFolderToSaveData