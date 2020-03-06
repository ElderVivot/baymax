import React from 'react'

import IntegrattionLayoutsFieldsNewOrEdit from './FieldsNewOrEdit'

const fieldsOptions = [
    { value: 'paymentDate', label: 'Data de Pagamento'},
    { value: 'document', label: 'NF ou Documento'},
    { value: 'cgceProvider', label: 'CNPJ Fornedor'},
    { value: 'nameProvider', label: 'Nome Fornecedor'},
    { value: 'bank', label: 'Banco/Caixa'},
    { value: 'amountPaid', label: 'Valor Pago'},
    { value: 'amountOriginal', label: 'Valor Original'},
    { value: 'amountInterest', label: 'Valor Juros'},
    { value: 'amountFine', label: 'Valor Multa'},
    { value: 'amountDiscount', label: 'Valor Desconto'},
    { value: 'dueDate', label: 'Data de Vencimento'},
    { value: 'issueDate', label: 'Data de Emissão'},
    { value: 'historic', label: 'Histórico'},
    { value: 'category', label: 'Categoria'},
    { value: 'accountPlan', label: 'Plano de Conta'},
]

function IntegrattionLayoutsFieldsList( { idx, fieldsFile, setFieldValue, initialValues } ){

    const addField = () => {
        setFieldValue("fields", [...fieldsFile, { 
            nameField: "",
            positionInFile: "",
            positionInFileEnd: "",
            nameColumn: "",
            formatDate: ""
         }])
    }
    
    const deleteField = () => {
        const updatedfieldsFile = [...fieldsFile]
        updatedfieldsFile.splice(idx, 1)
        setFieldValue("fields", updatedfieldsFile)
    }

    const EditField = () => {
        return (
            < IntegrattionLayoutsFieldsNewOrEdit
                key={`fieldFile-${idx}`}
                idx={idx}
                setFieldValueParent={setFieldValue}
                fieldsOptions={fieldsOptions}
                initialValues={initialValues[idx]}
            />
        )
    }

    function ButtonAdd(){
        return (
            <button className="btn btn-success" type="button" 
                onClick={addField}>
                <i className="fa fa-plus"></i>
            </button>
        )
    }

    function ButtonDelete(isDisabled=false){
        if(isDisabled === true){
            return( 
                <button className="btn btn-danger ml-2" type="button" 
                    onClick={deleteField} disabled>
                    <i className="fa fa-trash"></i>
                </button>
            )
        } else {
            return( 
                <button className="btn btn-danger ml-2" type="button" 
                    onClick={deleteField}>
                    <i className="fa fa-trash"></i>
                </button>
            )
        }
    }

    function Buttons(){
        if (fieldsFile.length === idx+1) {
            if(fieldsFile.length === 1 && idx === 0){
                return (
                    <div>
                        {ButtonAdd()}
                        {EditField()}
                        {ButtonDelete(true)}
                    </div>
                )
            } else {
                return (
                    <div>
                        {ButtonAdd()}
                        {EditField()}
                        {ButtonDelete()}
                    </div>
                )
            }
        } else {
            return (
                <div>
                    {EditField()}
                    {ButtonDelete()}
                </div>
                
            )
        }
    }

    const nameFieldVector = fieldsOptions.filter(option => option.value === fieldsFile[idx].nameField)
    let nameField = ""
    if(nameFieldVector.length > 0){
        nameField = nameFieldVector[0].label
    }
    
    return (
        <>
            <tr className="d-flex">
                <td className="col-4">{nameField}</td>
                <td className="col-1">{fieldsFile[idx].positionInFile}</td>
                <td className="col-1">{fieldsFile[idx].positionInFileEnd}</td>
                <td className="col-3">{fieldsFile[idx].nameColumn}</td>
                <td className="col-1">{fieldsFile[idx].formatDate}</td>
                <td className="col-2 text-align-center">
                    <Buttons />
                </td>
            </tr>
        </>
    )
}

export default IntegrattionLayoutsFieldsList