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