const moment = require('moment')

const zeroLeft = (valueInsert, countZeros=2) => {
        return ("0000".repeat(countZeros) + valueInsert).slice(-countZeros);
}
module.exports.zeroLeft = zeroLeft

function transformToDate(date){
    try {
        return moment(date.substring(0,10)).format('DD/MM/YYYY')
    } catch (error) {
        return null
    }
}
module.exports.transformToDate = transformToDate

function implementsFilterInURL(baseURL='', filter={}){
    let url = `${baseURL}?`
    for (let [key, value] of Object.entries(filter)) {
        url += `${key}=${value}&`
    }
    return url
}
module.exports.implementsFilterInURL = implementsFilterInURL

function getDataInObjectOrArray(data, vector=[], defaultReturn=undefined){
    try {
        let dataReturn
        if(vector.length === 1){
            dataReturn = data[vector[0]]
        } else if(vector.length === 2){
            dataReturn = data[vector[0]][vector[1]]
        } else if(vector.length === 3){
            dataReturn = data[vector[0]][vector[1]][vector[2]]
        } else if(vector.length === 4){
            dataReturn = data[vector[0]][vector[1]][vector[2]][vector[3]]
        } else if(vector.length === 5){
            dataReturn = data[vector[0]][vector[1]][vector[2]][vector[3]][vector[4]]
        } else if(vector.length === 6){
            dataReturn = data[vector[0]][vector[1]][vector[2]][vector[3]][vector[4]][vector[5]]
        } else if(vector.length === 7){
            dataReturn = data[vector[0]][vector[1]][vector[2]][vector[3]][vector[4]][vector[5]][vector[6]]
        } else {
            dataReturn = defaultReturn
        }

        if( ( dataReturn === undefined || dataReturn === null ) && ( defaultReturn !== undefined && defaultReturn !== null) ){
            return defaultReturn
        } else {
            return dataReturn
        }
    } catch (error) {
        return defaultReturn
    }
}
module.exports.getDataInObjectOrArray = getDataInObjectOrArray

function handleTelefone(ddd=undefined, fone=undefined){
    try {
        let dddManipulate = ""
        if(ddd !== undefined && ddd !== null && ddd !== ""){
            dddManipulate = `${ddd}-`
        }
        
        let foneManipulate = ""
        if(fone !== undefined && fone !== null && fone !== ""){
            foneManipulate = fone
            return `${dddManipulate}${foneManipulate}`
        } else {
            return ""
        }
    } catch (error) {
        return ""
    }
}
module.exports.handleTelefone = handleTelefone

function addOptionInCreatable(vector, value, label=undefined){
    // se o value for em branco já retorna o próprio vector, pois não deve adicionar nada
    if(value === "" || value === undefined || value === 0 || value === null || value === "0"){
        return vector
    }

    let valueFormated = ''
    try {
        valueFormated = value.normalize('NFD').replace(/([\u0300-\u036f]|[^0-9a-zA-Z])/g, '').toLowerCase()
    } catch (error) {
        valueFormated = ''
    }
    // se o valor formato não for válido (não conter letra e nada ele já retorna o próprio vetor)
    if(valueFormated === ""){
        return vector
    }

    // adiciona uma nova opção quando é um valor que ainda não existe
    if(vector.filter(option => option.value.toLowerCase() === valueFormated)[0] === undefined){
        vector.push({
            value: `${valueFormated}`, 
            label: label || `${value}`
        })
    }
    return vector
}
module.exports.addOptionInCreatable = addOptionInCreatable