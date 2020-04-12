import React from 'react'
import { Form } from "react-bootstrap"

function IntegrattionLayoutsHeader({ values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched }){

    function validateField(idx, nameColumn){
        try {
            return touched.header[idx][nameColumn] && errors.header[idx][nameColumn] ? "has-error" : null
        } catch (error) {
            return null
        }
    }

    function messageError(idx, nameColumn){
        try {
            return errors.header[idx][nameColumn]
        } catch (error) {
            return null
        }
    }
    
    return (
        <>
            <div className="form row mt-3 mb-0">
                <label className="col-form-label font-weight-600">Nome dos campos que identifica as colunas do Arquivo:</label>
                <button className="btn btn-success btn-sm btn10px ml-3 mt-1" type="button" style={{height:25}}
                    onClick={() => setFieldValue("header", [...values.header, { nameColumn: "" }]) }>
                    <i className="fa fa-plus"></i>
                </button>
                
            </div>

            {values.header.map( (field, idx) => (
                <div key={`values.header[${idx}]`} className="form row container d-flex mb-0 pb-0 mt-1 col-12">
                    <div className="col-11 p-0">
                        <div className="input-group align-items-baseline p-0">
                            <div className="input-group-prepend">
                                <span className="input-group-text m-0" style={{"color": "black !important"}}>{idx+1}</span>
                            </div>
                            <div className="col p-0">
                                <Form.Group className="mb-0">
                                    <Form.Control 
                                        id="nameColumn"
                                        type="text"
                                        name={`header[${idx}].nameColumn`}
                                        className={`form-control ${validateField(idx, 'nameColumn')}`}
                                        placeholder="Informe o nome da coluna"
                                        value={values.header[idx].nameColumn}
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                    />
                                    <Form.Control.Feedback type="invalid">{messageError(idx, 'nameColumn')}</Form.Control.Feedback>
                                </Form.Group>
                            </div>
                        </div>
                    </div>
                    
                    <div className="col-1 p-0 d-flex mt-1 align-items-baseline justify-content-center">
                        <button className="btn btn-danger ml-2 btn-sm btn10px" type="button" 
                            onClick={() => {
                                const updatedFieldsHeader = [...values.header]
                                updatedFieldsHeader.splice(idx, 1)
                                setFieldValue("header", updatedFieldsHeader)
                            }}>
                            <i className="fa fa-trash"></i>
                        </button>
                    </div>
                </div>
            ))}
        </>
    )
}

export default IntegrattionLayoutsHeader