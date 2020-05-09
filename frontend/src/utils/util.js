const zeroLeft = (valueInsert, countZeros=2) => {
        return ("0000".repeat(countZeros) + valueInsert).slice(-countZeros);
}
module.exports.zeroLeft = zeroLeft

function transformToDate(date){
    try {
        let newDate = date.substring(0,10)
        newDate = new Date(newDate)
        return `${zeroLeft(newDate.getDay(), 2)}/${zeroLeft(newDate.getMonth(), 2)}/${newDate.getFullYear()}`
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