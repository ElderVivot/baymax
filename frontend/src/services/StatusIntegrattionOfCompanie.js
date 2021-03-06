class StatusIntegrattionOfCompanie {
    constructor(dataCompanie={}){
        this.dataCompanie = dataCompanie
        this.status = 'Pendente'
    }

    isCompanyBranch(){
        try {
            if(this.dataCompanie.isCompanyBranch === "Sim"){
                this.status = 'É Filial'
            }
        } catch (error) {
            return
        }
    }

    hasMoviment(){
        try {
            const totalNotes = this.dataCompanie.qtdEntryNotes + this.dataCompanie.qtdOutputNotes + this.dataCompanie.qtdServiceNotes
            if(totalNotes === 0){
                this.status = 'Sem Movimento'
            }
        } catch (error) {
            return
        }
    }

    statusCompanie(){
        if(this.dataCompanie.stat_emp !== "Ativa" || this.dataCompanie.dina_emp ){
            this.status = 'Empresa Inativa'
        }
    }

    isCompletedOldModel(){
        try {
            if( !this.dataCompanie.layoutsAccountPaidNewModel && this.dataCompanie.dateAccountPaidOld){
                this.status = 'Concluída - Modelo Antigo'
            }
        } catch (error) {
            
        }
    }

    isCompleted(){
        try {
            if(this.dataCompanie.layoutsAccountPaidNewModel && !this.dataCompanie.statusAccountPaid){
                this.status = 'Concluída - ERP'
            }
        } catch (error) {
            return
        }
    }

    identifiesTheStatus(){
        if(this.dataCompanie.statusAccountPaid && this.dataCompanie.statusAccountPaid !== "Pendente"){
            this.status = this.dataCompanie.statusAccountPaid
            return this.status
        }

        this.hasMoviment()
        this.isCompanyBranch()
        this.statusCompanie()
        this.isCompletedOldModel()
        this.isCompleted()

        return this.status
    }
}
module.exports = StatusIntegrattionOfCompanie