function statEmp(status){
    if(status === 'A'){
        return 'Ativa'
    } else if(status === 'I'){
        return 'Inativa'
    } else if(status === 'M'){
        return 'Sem Movimento'
    } else if(status === 'C'){
        return 'Em Constituição'
    } else if(status === 'B'){
        return 'Em Processo Baixa'
    } else {
        return status
    }
}
module.exports.statEmp = statEmp

function isCompanyBranch(tins_emp, cgce_emp){
    try {
        if(tins_emp !== 1){
            return 'Não'
        } else {
            if(cgce_emp.substring(8, 12) === '0001'){
                return 'Não'
            } else {
                return 'Sim'
            }
        }
    } catch (error) {
        return 'Não'
    }
}
module.exports.isCompanyBranch = isCompanyBranch

function formatCgceEmp(tins_emp, cgce_emp){
    try {
        if(tins_emp === 1){
            return `${cgce_emp.substring(0, 2)}.${cgce_emp.substring(2, 5)}.${cgce_emp.substring(5, 8)}/${cgce_emp.substring(8, 12)}-${cgce_emp.substring(12)}`
        } else if(tins_emp === 2){
            return `${cgce_emp.substring(0, 3)}.${cgce_emp.substring(3, 6)}.${cgce_emp.substring(6, 9)}-${cgce_emp.substring(9)}`
        } else {
            return cgce_emp
        }
    } catch (error) {
        return 'Não'
    }
}
module.exports.formatCgceEmp = formatCgceEmp