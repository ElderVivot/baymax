import React from 'react'
import Select from 'react-select'
import { Col, Form } from "react-bootstrap"

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

function FieldsValidation( { values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched, defaultValues } ){

    let fieldsOptions = []
    fieldsOptions.push(...values.fields.map( value => value["nameField"] ))

    function validateField(vector){
        try {
            if(vector.length === 2){
                return errors.validationLineToPrint[vector[0]][vector[1]] ? "has-error" : null
            }
            if(vector.length === 3){
                return errors.validationLineToPrint[vector[0]][vector[1]][vector[2]] ? "has-error" : null
            }
        } catch (error) {
            return null
        }
    }

    function messageError(vector){
        try {
            let message = null
            if(vector.length === 2){
                message = errors.validationLineToPrint[vector[0]][vector[1]]
            }
            if(vector.length === 3){
                message = errors.validationLineToPrint[vector[0]][vector[1]][vector[2]]
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
        if(values.validationLineToPrint[idx].typeValidation === "isDate") {
            disabled = true
            values.validationLineToPrint[idx].valueValidation = ' '
        } else {
            if(values.validationLineToPrint[idx].valueValidation === ' '){
                values.validationLineToPrint[idx].valueValidation = ''
            }
        }

        return(
            <Col >
                <Form.Group className="mb-0">
                    <Form.Control
                        id={`validationLineToPrint[${idx}].valueValidation`}
                        name={`validationLineToPrint[${idx}].valueValidation`}
                        type="text"
                        className={`selected ${validateField([idx, 'valueValidation'])} text-center`}
                        placeholder="Informe a validação"
                        value={values.validationLineToPrint[idx].valueValidation}
                        disabled={disabled}
                        onChange={handleChange(`validationLineToPrint[${idx}].valueValidation`)}
                        onBlur={() => setFieldTouched(`validationLineToPrint[${idx}].valueValidation`, true)}
                    />
                    <Form.Control.Feedback type="invalid">{messageError([idx, 'valueValidation'])}</Form.Control.Feedback>
                </Form.Group>
            </Col>
        )
    }
    
    return (
        <>
            <div className="form row mt-2">
                <label className="col-form-label font-weight-600">Os dados deste layout deverão ser gerados apenas se:</label>                
            </div>

            <div className="form row">
                <table className="table ml-3 table-bordered table-hover">
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
                                        setFieldValue("validationLineToPrint", [...values.validationLineToPrint, defaultValues.validationLineToPrint[0]])
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
                                        <Form.Group className="mb-0">
                                            <Select 
                                                id={`validationLineToPrint[${idx}].nameField`}
                                                name={`validationLineToPrint[${idx}].nameField`}
                                                options={fieldsOptions}
                                                className={`selected ${validateField([idx, 'nameField'])} select-center`}
                                                isSearchable={true}
                                                placeholder="Selecione"
                                                value={fieldsOptions.filter(option => option.value === values.validationLineToPrint[idx].nameField)[0]}
                                                onChange={selectedOption => handleChange(`validationLineToPrint[${idx}].nameField`)(selectedOption.value)}
                                                onBlur={() => setFieldTouched(`validationLineToPrint[${idx}].nameField`, true)}
                                            />
                                            <Form.Control.Feedback type="invalid">{messageError([idx, 'nameField'])}</Form.Control.Feedback>
                                        </Form.Group>
                                    </Col>
                                </td>
                                <td key={`validationLineToPrint[${idx}].typeValidation`} className="col-2 align-center">
                                    <Col>
                                        <Form.Group className="mb-0">
                                            <Select 
                                                id={`validationLineToPrint[${idx}].typeValidation`}
                                                name={`validationLineToPrint[${idx}].typeValidation`}
                                                options={typeValidationOptions}
                                                className={`selected ${validateField([idx, 'typeValidation'])} select-center`}
                                                isSearchable={true}
                                                placeholder="Selecione"
                                                value={typeValidationOptions.filter(option => option.value === values.validationLineToPrint[idx].typeValidation)[0]}
                                                onChange={selectedOption => handleChange(`validationLineToPrint[${idx}].typeValidation`)(selectedOption.value)}
                                                onBlur={() => setFieldTouched(`validationLineToPrint[${idx}].typeValidation`, true)}
                                            />
                                            <Form.Control.Feedback type="invalid">{messageError([idx, 'typeValidation'])}</Form.Control.Feedback>
                                        </Form.Group>
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

export default FieldsValidation