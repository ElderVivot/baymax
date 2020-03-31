import React from 'react'

import IntegrattionLayoutsFieldsNewOrEdit from './FieldsNewOrEdit'

const fieldsOptions = [
    { value: 'paymentDate', label: 'Data de Pagamento'},
    { value: 'document', label: 'NF ou Documento'},
    { value: 'cgceProvider', label: 'CNPJ Fornedor'},
    { value: 'nameProvider', label: 'Nome Fornecedor'},
    { value: 'bank', label: 'Banco/Caixa'},
    { value: 'account', label: 'Conta Corrente'},
    { value: 'amountPaid', label: 'Valor Pago'},
    { value: 'amountOriginal', label: 'Valor Original'},
    { value: 'amountInterest', label: 'Valor Juros'},
    { value: 'amountFine', label: 'Valor Multa'},
    { value: 'amountDiscount', label: 'Valor Desconto'},
    { value: 'amountDevolution', label: 'Valor Devolução'},
    { value: 'dueDate', label: 'Data de Vencimento'},
    { value: 'issueDate', label: 'Data de Emissão'},
    { value: 'historic', label: 'Histórico'},
    { value: 'category', label: 'Categoria'},
    { value: 'accountPlan', label: 'Plano de Contas'},
    { value: 'parcelNumber', label: 'Número da Parcela'},
    { value: 'companyBranch', label: 'Filial/Empresa'},
    { value: 'typeMoviment', label: 'Tipo Movimento'},
]

function IntegrattionLayoutsFieldsList( { idx, fieldsFile, setFieldValue, initialValues } ){

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

    function ButtonDelete(isDisabled=false){
        return( 
            <button className="btn btn-danger ml-2 btn-sm btn10px" type="button" 
                onClick={deleteField} disabled={isDisabled}>
                <i className="fa fa-trash"></i>
            </button>
        )
    }

    function Buttons(){
        return (
            <div>
                {EditField()}
                {ButtonDelete()}
            </div>
        )
    }

    const nameFieldVector = fieldsOptions.filter(option => option.value === fieldsFile[idx].nameField)
    let nameField = ""
    if(nameFieldVector.length > 0){
        nameField = nameFieldVector[0].label
    }
    
    return (
        <>
            <tr className="d-flex justify-content-center text-center">
                <td className="col-4 align-center">{nameField}</td>
                <td className="col-1 align-center">{fieldsFile[idx].positionInFile}</td>
                <td className="col-1 align-center">{fieldsFile[idx].positionInFileEnd}</td>
                <td className="col-3 align-center">{fieldsFile[idx].nameColumn}</td>
                <td className="col-1 align-center">{fieldsFile[idx].formatDate}</td>
                <td className="col-2 align-center">
                    <Buttons />
                </td>
            </tr>
        </>
    )
}

export default IntegrattionLayoutsFieldsList