import React from 'react'
import Select from 'react-select'
import { Col, Form } from "react-bootstrap"

const typeValidationOptions = [
    { value: 'banksInTheCorrelation', label: 'Bancos no De-Para'},
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

function FieldsValidation( { values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched, defaultValues, idxAccountPaid, integrattionLayouts } ){

    let fieldsOptions = []
    for(let integrattionLayout of integrattionLayouts){
        if(integrattionLayout._id === values.accountPaid.layouts[idxAccountPaid].idLayout){
            fieldsOptions.push(...integrattionLayout.fields.map( value => value["nameField"] ))
            break
        }
    }

    function validateField(vector){
        try {
            if(vector.length === 2){
                return errors.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[vector[0]][vector[1]] ? "has-error" : null
            }
            if(vector.length === 3){
                return errors.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[vector[0]][vector[1]][vector[2]] ? "has-error" : null
            }
        } catch (error) {
            return null
        }
    }

    function messageError(vector){
        try {
            let message = null
            if(vector.length === 2){
                message = errors.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[vector[0]][vector[1]]
            }
            if(vector.length === 3){
                message = errors.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[vector[0]][vector[1]][vector[2]]
            }

            if(message.indexOf('must be a') >= 0) {
                message = 'Campo obrigatório'
            }
            return message
        } catch (error) {
            return null
        }
    }

    function fieldValueValidation(idx){
        let disabled = false
        if(values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].typeValidation === "isDate" || values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].typeValidation === "banksInTheCorrelation") {
            disabled = true
            values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].valueValidation = ' '
        } else {
            if(values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].valueValidation === ' '){
                values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].valueValidation = ''
            }
        }

        return(
            <Col >
                <Form.Group className="mb-0">
                    <Form.Control
                        name={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].valueValidation`}
                        type="text"
                        className={`selected ${validateField([idx, 'valueValidation'])} text-center`}
                        placeholder="Informe a validação"
                        value={values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].valueValidation}
                        disabled={disabled}
                        onChange={handleChange(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].valueValidation`)}
                        onBlur={() => setFieldTouched(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].valueValidation`, true)}
                    />
                    <Form.Control.Feedback type="invalid">{messageError([idx, 'valueValidation'])}</Form.Control.Feedback>
                </Form.Group>
            </Col>
        )
    }

    function fieldNameField(idx){
        let disabled = false
        if(values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].typeValidation === "banksInTheCorrelation") {
            disabled = true
            values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].nameField = ' '
        } else {
            if(values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].nameField === ' '){
                values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].nameField = ''
            }
        }

        return (
            <Col>
                <Form.Group className="mb-0">
                    <Select 
                        id={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nameField`}
                        name={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nameField`}
                        options={fieldsOptions}
                        className={`selected ${validateField([idx, 'nameField'])} select-center`}
                        isSearchable={true}
                        placeholder="Selecione"
                        isDisabled={disabled}
                        value={fieldsOptions.filter(option => option.value === values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].nameField)[0]}
                        onChange={selectedOption => handleChange(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nameField`)(selectedOption.value)}
                        onBlur={() => setFieldTouched(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nameField`, true)}
                    />
                    <Form.Control.Feedback type="invalid">{messageError([idx, 'nameField'])}</Form.Control.Feedback>
                </Form.Group>
            </Col>
        )
    }

    function validateIfDataIsThisCompanie(){
        try {
            if(values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie === undefined){
                values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie = []
            }

            return (
                values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie.map( (field, idx) => (
                    <tr key={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}]`} className="d-flex justify-content-center text-center">
                        <td key={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nameField`} className="col-3 align-center">
                            { fieldNameField(idx) }
                        </td>
                        <td key={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].typeValidation`} className="col-2 align-center">
                            <Col>
                                <Form.Group className="mb-0">
                                    <Select 
                                        id={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].typeValidation`}
                                        name={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].typeValidation`}
                                        options={typeValidationOptions}
                                        className={`selected ${validateField([idx, 'typeValidation'])} select-center`}
                                        isSearchable={true}
                                        placeholder="Selecione"
                                        value={typeValidationOptions.filter(option => option.value === values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].typeValidation)[0]}
                                        onChange={selectedOption => handleChange(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].typeValidation`)(selectedOption.value)}
                                        onBlur={() => setFieldTouched(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].typeValidation`, true)}
                                    />
                                    <Form.Control.Feedback type="invalid">{messageError([idx, 'typeValidation'])}</Form.Control.Feedback>
                                </Form.Group>
                            </Col>
                        </td>
                        <td key={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].valueValidation`} className="col-4 align-center">
                            {fieldValueValidation(idx)}
                        </td>
                        <td key={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nextValidationOrAnd`} className="col-2 align-center">
                            <Col>
                                <Select 
                                    id={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nextValidationOrAnd`}
                                    name={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nextValidationOrAnd`}
                                    options={nextValidationOrAndOptions}
                                    className={`selected ${validateField('nextValidationOrAnd', idx)} select-center`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={nextValidationOrAndOptions.filter(option => option.value === values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie[idx].nextValidationOrAnd)[0]}
                                    onChange={selectedOption => handleChange(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nextValidationOrAnd`)(selectedOption.value)}
                                    onBlur={() => setFieldTouched(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].nextValidationOrAnd`, true)}
                                />
                            </Col>
                        </td>
                        <td key={`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie[${idx}].button`} className="col-1 align-center">
                            <button className="btn btn-danger ml-2 btn-sm btn10px" type="button" 
                                onClick={() => {
                                    const updatedFields = [...values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie]
                                    updatedFields.splice(idx, 1)
                                    setFieldValue(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie`, updatedFields)
                                } }
                            >
                                <i className="fa fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                ))
            )
        } catch (error) {
            
        }
    }
    
    return (
        <>
            <div className="form row ml-2 mt-0">
                <label className="col-form-label font-weight-600">Os dados desta empresa deverão ser gerados apenas se:</label>                
            </div>

            <div className="form row">
                <table className="table ml-3 table-bordered table-hover mb-0">
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
                                        setFieldValue(`accountPaid.layouts[${idxAccountPaid}].validateIfDataIsThisCompanie`, [...values.accountPaid.layouts[idxAccountPaid].validateIfDataIsThisCompanie, defaultValues.accountPaid.layouts[0].validateIfDataIsThisCompanie[0]])
                                    } } >
                                    <i className="fa fa-plus"></i>
                                </button>        
                            </th>
                        </tr>
                    </thead>
                    <tbody>{
                        validateIfDataIsThisCompanie()
                    }
                    </tbody>
                </table>
            </div>           
        </>

    )
    
}

export default FieldsValidation