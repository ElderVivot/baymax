class IsIntegrattionLayoutCompanieOld {
    constructor(companie={}){
        this.companie = companie
        this.integrattionLayoutCompanie = {}
    }

    process(){
        if(this.companie.dateAccountPaidOld !== undefined){
            return true
        }
    }
}
module.exports = IsIntegrattionLayoutCompanieOld