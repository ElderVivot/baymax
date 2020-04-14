import React from 'react'
import Select from 'react-select'
import { Col, Form } from "react-bootstrap"

// const fieldsOptions = [
//     { value: 'paymentDate', label: 'Data de Pagamento'},
//     { value: 'document', label: 'NF ou Documento'},
//     { value: 'cgceProvider', label: 'CNPJ Fornedor'},
//     { value: 'nameProvider', label: 'Nome Fornecedor'},
//     { value: 'bank', label: 'Banco/Caixa'},
//     { value: 'account', label: 'Conta Corrente'},
//     { value: 'amountPaid', label: 'Valor Pago'},
//     { value: 'amountOriginal', label: 'Valor Original'},
//     { value: 'amountInterest', label: 'Valor Juros'},
//     { value: 'amountFine', label: 'Valor Multa'},
//     { value: 'amountDiscount', label: 'Valor Desconto'},
//     { value: 'amountDevolution', label: 'Valor Devolução'},
//     { value: 'dueDate', label: 'Data de Vencimento'},
//     { value: 'issueDate', label: 'Data de Emissão'},
//     { value: 'historic', label: 'Histórico'},
//     { value: 'category', label: 'Categoria'},
//     { value: 'accountPlan', label: 'Plano de Contas'},
//     { value: 'parcelNumber', label: 'Número da Parcela'},
//     { value: 'companyBranch', label: 'Filial/Empresa'},
//     { value: 'typeMoviment', label: 'Tipo Movimento'},
// ]

const typeValidationOptions = [
    { value: 'isEqual', label: 'É igual à'},
    { value: 'isDifferent', label: 'É diferente de'},
    { value: 'isDate', label: 'É uma data'},
    { value: 'isLessThan', label: 'É menor que'},
    { value: 'isLessThanOrEqual', label: 'É menor ou igual à'},
    { value: 'isBiggerThan', label: 'É maior que'},
    { value: 'isBiggerThanOrEqual', label: 'É maior ou igual à'},
    { value: 'contains', label: 'Contém'},
    { value: 'notContains', label: 'Não Contém'}
]

const nextValidationOrAndOptions = [
    { value: 'and', label: 'E'},
    { value: 'or', label: 'OU'}
]

function IntegrattionLayoutsFieldsListValidation( { values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched } ){

    let fieldsOptions = []
    fieldsOptions.push(...values.fields.map( value => value["nameField"] ))

    function validateField(name, idx){
        try {
            return touched.validationLineToPrint[idx][name] && errors.validationLineToPrint[idx][name] ? "has-error" : null
        } catch (error) {
            return null
        }
    }

    function fieldValueValidation(idx){
        let disabled = false
        if(values.validationLineToPrint[idx].typeValidation === "isDate") {
            disabled = true
        }

        return(
            <Col >
                <Form.Control
                    id={`validationLineToPrint[${idx}].valueValidation`}
                    name={`validationLineToPrint[${idx}].valueValidation`}
                    type="text"
                    className={`selected ${validateField('valueValidation', idx)} text-center`}
                    placeholder="Informe a validação"
                    value={values.validationLineToPrint[idx].valueValidation}
                    disabled={disabled}
                    onChange={handleChange(`validationLineToPrint[${idx}].valueValidation`)}
                    onBlur={() => setFieldTouched(`validationLineToPrint[${idx}].valueValidation`, true)}
                />
            </Col>
        )
    }
    
    return (
        <>
            <div className="form row mt-2">
                <label className="col-form-label font-weight-600">Os dados deste layout deverão ser gerados apenas se:</label>                
            </div>

            <div className="form row">
                <table className="table ml-3 table-striped table-bordered table-hover">
                    <thead>
                        <tr className="d-flex justify-content-center text-center">
                            <th className="col-3 fields-of-table align-center">Campo</th>
                            <th className="col-2 fields-of-table align-center">Tipo Validação</th>
                            <th className="col-4 fields-of-table align-center">Valor</th>
                            <th className="col-2 fields-of-table align-center">E/OU</th>
                            <th className="col-1 fields-of-table align-center">
                                <div className="font-weight-600">Ações</div>
                                <button className="btn btn-success btn-sm btn10px ml-3" type="button" style={{height:25}}
                                    onClick={() => {
                                        setFieldValue("validationLineToPrint", [...values.validationLineToPrint, { 
                                            nameField: "",
                                            typeValidation: "",
                                            valueValidation: "",
                                            nextValidationOrAnd: ""
                                        }])
                                    } } >
                                    <i className="fa fa-plus"></i>
                                </button>        
                            </th>
                        </tr>
                    </thead>
                    <tbody>{
                        values.validationLineToPrint.map( (field, idx) => (
                            <tr key={`validationLineToPrint[${idx}]`} className="d-flex justify-content-center text-center">
                                <td key={`validationLineToPrint[${idx}].nameField`} className="col-3 align-center">
                                    <Col>
                                        <Select 
                                            id={`validationLineToPrint[${idx}].nameField`}
                                            name={`validationLineToPrint[${idx}].nameField`}
                                            options={fieldsOptions}
                                            className={`selected ${validateField('nameField', idx)} select-center`}
                                            isSearchable={true}
                                            placeholder="Selecione"
                                            value={fieldsOptions.filter(option => option.value === values.validationLineToPrint[idx].nameField)[0]}
                                            onChange={selectedOption => handleChange(`validationLineToPrint[${idx}].nameField`)(selectedOption.value)}
                                            onBlur={() => setFieldTouched(`validationLineToPrint[${idx}].nameField`, true)}
                                        />
                                    </Col>
                                </td>
                                <td key={`validationLineToPrint[${idx}].typeValidation`} className="col-2 align-center">
                                    <Col>
                                        <Select 
                                            id={`validationLineToPrint[${idx}].typeValidation`}
                                            name={`validationLineToPrint[${idx}].typeValidation`}
                                            options={typeValidationOptions}
                                            className={`selected ${validateField('typeValidation', idx)} select-center`}
                                            isSearchable={true}
                                            placeholder="Selecione"
                                            value={typeValidationOptions.filter(option => option.value === values.validationLineToPrint[idx].typeValidation)[0]}
                                            onChange={selectedOption => handleChange(`validationLineToPrint[${idx}].typeValidation`)(selectedOption.value)}
                                            onBlur={() => setFieldTouched(`validationLineToPrint[${idx}].typeValidation`, true)}
                                        />
                                    </Col>
                                </td>
                                <td key={`validationLineToPrint[${idx}].valueValidation`} className="col-4 align-center">
                                    {fieldValueValidation(idx)}
                                </td>
                                <td key={`validationLineToPrint[${idx}].nextValidationOrAnd`} className="col-2 align-center">
                                    <Col>
                                        <Select 
                                            id={`validationLineToPrint[${idx}].nextValidationOrAnd`}
                                            name={`validationLineToPrint[${idx}].nextValidationOrAnd`}
                                            options={nextValidationOrAndOptions}
                                            className={`selected ${validateField('nextValidationOrAnd', idx)} select-center`}
                                            isSearchable={true}
                                            placeholder="Selecione"
                                            value={nextValidationOrAndOptions.filter(option => option.value === values.validationLineToPrint[idx].nextValidationOrAnd)[0]}
                                            onChange={selectedOption => handleChange(`validationLineToPrint[${idx}].nextValidationOrAnd`)(selectedOption.value)}
                                            onBlur={() => setFieldTouched(`validationLineToPrint[${idx}].nextValidationOrAnd`, true)}
                                        />
                                    </Col>
                                </td>
                                <td key={`validationLineToPrint[${idx}].button`} className="col-1 align-center">
                                    <button className="btn btn-danger ml-2 btn-sm btn10px" type="button" 
                                        onClick={() => {
                                            const updatedFields = [...values.validationLineToPrint]
                                            updatedFields.splice(idx, 1)
                                            setFieldValue("validationLineToPrint", updatedFields)
                                        } }
                                    >
                                        <i className="fa fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        ))
                    }
                    </tbody>
                </table>
            </div>           
        </>

    )
    
}

export default IntegrattionLayoutsFieldsListValidation