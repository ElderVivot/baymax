import React from 'react'
import Creatable from 'react-select/creatable'
import { Col, Form } from "react-bootstrap"

const bankNewOptions = [
    { value: 'ITAU', label: 'ITAÚ' }, 
    { value: 'BRASIL', label: 'BANCO DO BRASIL' },
    { value: 'CEF', label: 'CAIXA ECONÔMICA FEDERAL' },
    { value: 'DINHEIRO', label: 'DINHEIRO' },
    { value: 'SANTANDER', label: 'SANTANDER' },
    { value: 'BRADESCO', label: 'BRADESCO' },
    { value: 'SICOOB', label: 'SICOOB' },
    { value: 'SICREDI', label: 'SICREDI' },
    { value: 'BANPARA', label: 'BANPARÁ' },
    { value: 'SAFRA', label: 'SAFRA' }
]

function BanksCorrelation( { values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched, defaultValues, idxAccountPaid } ){

    function validateField(vector){
        try {
            if(vector.length === 2){
                return errors.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation[vector[0]][vector[1]] ? "has-error" : null
            }
            if(vector.length === 3){
                return errors.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation[vector[0]][vector[1]][vector[2]] ? "has-error" : null
            }
        } catch (error) {
            return null
        }
    }

    function messageError(vector){
        try {
            let message = null
            if(vector.length === 2){
                message = errors.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation[vector[0]][vector[1]]
            }
            if(vector.length === 3){
                message = errors.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation[vector[0]][vector[1]][vector[2]]
            }

            if(message.indexOf('must be a') >= 0) {
                message = 'Campo obrigatório'
            }
            return message
        } catch (error) {
            return null
        }
    }

    function bankAndAccountCorrelation(){
        try {
            if(values.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation === undefined){
                values.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation = []
            }

            return (
                values.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation.map( (field, idx) => (
                    <tr key={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}]`} className="d-flex justify-content-center text-center">
                        <td key={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].nameField`} className="col-4 align-center">
                            <Col>
                                <Form.Group className="mb-0">
                                    <Form.Control
                                        name={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].bankFile`}
                                        type="text"
                                        className={`selected ${validateField([idx, 'bankFile'])} text-center`}
                                        placeholder="Informe o banco"
                                        value={values.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation[idx].bankFile}
                                        onChange={handleChange(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].bankFile`)}
                                        onBlur={() => setFieldTouched(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].bankFile`, true)}
                                    />
                                    <Form.Control.Feedback type="invalid">{messageError([idx, 'bankFile'])}</Form.Control.Feedback>
                                </Form.Group>
                            </Col>
                        </td>
                        <td key={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].accountFile`} className="col-2 align-center">
                            <Col>
                                <Form.Group className="mb-0">
                                    <Form.Control
                                        name={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].accountFile`}
                                        type="text"
                                        className={`selected ${validateField([idx, 'accountFile'])} text-center`}
                                        placeholder="Informe a conta"
                                        value={values.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation[idx].accountFile}
                                        onChange={handleChange(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].accountFile`)}
                                        onBlur={() => setFieldTouched(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].accountFile`, true)}
                                    />
                                    <Form.Control.Feedback type="invalid">{messageError([idx, 'accountFile'])}</Form.Control.Feedback>
                                </Form.Group>
                            </Col>
                        </td>
                        <td key={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].bankNew`} className="col-3 align-center">
                            <Col>
                                <Creatable 
                                    id={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].bankNew`}
                                    name={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].bankNew`}
                                    options={bankNewOptions}
                                    className={`selected ${validateField('bankNew', idx)} select-center`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={bankNewOptions.filter(option => option.value === values.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation[idx].bankNew)[0]}
                                    onChange={selectedOption => handleChange(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].bankNew`)(selectedOption.value)}
                                    onBlur={() => setFieldTouched(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].bankNew`, true)}
                                    formatCreateLabel={(string) => `Criar a opção "${string}"`}
                                />
                            </Col>
                        </td>
                        <td key={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].accountNew`} className="col-2 align-center">
                            <Col>
                                <Form.Group className="mb-0">
                                    <Form.Control
                                        name={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].accountNew`}
                                        type="text"
                                        className={`selected ${validateField([idx, 'accountNew'])} text-center`}
                                        placeholder="Informe a conta"
                                        value={values.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation[idx].accountNew}
                                        onChange={handleChange(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].accountNew`)}
                                        onBlur={() => setFieldTouched(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].accountNew`, true)}
                                    />
                                    <Form.Control.Feedback type="invalid">{messageError([idx, 'accountNew'])}</Form.Control.Feedback>
                                </Form.Group>
                            </Col>
                        </td>
                        <td key={`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation[${idx}].button`} className="col-1 align-center">
                            <button className="btn btn-danger ml-2 btn-sm btn10px" type="button" 
                                onClick={() => {
                                    const updatedFields = [...values.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation]
                                    updatedFields.splice(idx, 1)
                                    setFieldValue(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation`, updatedFields)
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
            <div className="form row ml-2 mt-1">
                <label className="col-form-label font-weight-600">De Para dos Bancos/Caixa entre arquivo financeiro e extrato bancário:</label>                
            </div>

            <div className="form row">
                <table className="table ml-3 table-bordered table-hover mb-0">
                    <thead>
                        <tr className="d-flex justify-content-center text-center">
                            <th className="col-4 fields-of-table align-center">Banco do Arquivo</th>
                            <th className="col-2 fields-of-table align-center">Conta do Arquivo</th>
                            <th className="col-3 fields-of-table align-center">Novo Banco</th>
                            <th className="col-2 fields-of-table align-center">Nova Conta</th>
                            <th className="col-1 fields-of-table align-center">
                                <div className="font-weight-600">Ações</div>
                                <button className="btn btn-success btn-sm btn10px ml-3" type="button" style={{height:25}}
                                    onClick={() => {
                                        setFieldValue(`accountPaid.layouts[${idxAccountPaid}].bankAndAccountCorrelation`, [...values.accountPaid.layouts[idxAccountPaid].bankAndAccountCorrelation, defaultValues.accountPaid.layouts[0].bankAndAccountCorrelation[0]])
                                    } } >
                                    <i className="fa fa-plus"></i>
                                </button>        
                            </th>
                        </tr>
                    </thead>
                    <tbody>{
                        bankAndAccountCorrelation()
                    }
                    </tbody>
                </table>
            </div>
        </>

    )
    
}

export default BanksCorrelation