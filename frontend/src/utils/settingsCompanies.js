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

function regimeEmp(code_regime){
    try {
        if(code_regime === 1){
            return 'Lucro Real'
        } else if(code_regime === 2){
            return 'Simples - ME'
        } else if(code_regime === 3){
            return 'Estimativa'
        } else if(code_regime === 4){
            return 'Simples - EPP'
        } else if(code_regime === 5){
            return 'Lucro Presumido'
        } else if(code_regime === 6){
            return 'Reg. Exp. Trib.'
        } else if(code_regime === 7){
            return 'Lucro Arbitrado'
        } else if(code_regime === 8){
            return 'Imune do IRPJ'
        } else if(code_regime === 9){
            return 'Isenta do IRPJ'
        } else {
            return ''
        }
    } catch (error) {
        return ''
    }
}
module.exports.regimeEmp = regimeEmp

function regimeCaixaEmp(code_regime){
    try {
        if(code_regime === 'C'){
            return 'Competência'
        } else if(code_regime === 'X'){
            return 'Caixa'
        } else {
            return ''
        }
    } catch (error) {
        return ''
    }
}
module.exports.regimeCaixaEmp = regimeCaixaEmp