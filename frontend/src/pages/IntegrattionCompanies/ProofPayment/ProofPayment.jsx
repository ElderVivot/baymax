import React from 'react'
import Select from 'react-select'
import { Col, Form } from "react-bootstrap"

const banksOptions = [
    { value: 341, label: 'Itaú'},
    { value: 33, label: 'Santander'},
    { value: 3, label: 'Amazônia'},
	{ value: 756, label: 'Sicoob'},
	{ value: 237, label: 'Bradesco'}
]

function ProofPayment( { values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched, defaultValues } ){
    
    function handleChangeSelectMulti(event){
        let proofPayment = []
        try {
            event.map( bank => proofPayment.push(bank) )
        } catch (error) {
            // se der erro que dizer que não tem map pra percorrer, ou seja, não tem nada selecionado
            proofPayment = []
        }
        setFieldValue(`proofPayment`, proofPayment)
    }
    
    return (
        <>
            <div className="form row mt-3">
                <label className="col-form-label font-weight-600">Selecione os Bancos que Deseja Ler Comprovante de Pagamento:</label>                
                <Col lg={5}>
                    <Form.Group className="mb-0">
                        <Select 
                            isMulti
                            name="proofPayment"
                            options={banksOptions}
                            value={values.proofPayment}
                            onChange={ event => handleChangeSelectMulti(event)}
                            className="selected"
                            // classNamePrefix="select"
                            placeholder="Selecione"
                        />
                        {/* <Form.Control.Feedback type="invalid">{messageError([idx, 'typeValidation'])}</Form.Control.Feedback> */}
                    </Form.Group>
                </Col>
            </div>               
        </>

    )
    
}

export default ProofPayment