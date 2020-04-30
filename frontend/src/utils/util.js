const zeroLeft = (valueInsert, countZeros=2) => {
        return ("0000".repeat(countZeros) + valueInsert).slice(-countZeros);
}
module.exports.zeroLeft = zeroLeft

function transformToDate(date){
    if(date === null){
        return null
    }
    let newDate = date.substring(0,10)
    newDate = new Date(newDate)
    return `${zeroLeft(newDate.getDay(), 2)}/${zeroLeft(newDate.getMonth(), 2)}/${newDate.getFullYear()}`
}
module.exports.transformToDate = transformToDate