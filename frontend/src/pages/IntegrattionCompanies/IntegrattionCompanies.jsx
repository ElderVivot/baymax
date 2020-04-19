import React, { useEffect, useState } from 'react'
import Select from 'react-select'
import { Form } from "react-bootstrap"
import * as Yup from 'yup'
import { Formik } from 'formik'

import '../styles.css'
import api from '../../services/api'

import AccountPaid from './AccountPaid/AccountPaid'

let validationSchema = Yup.object().shape({
    codi_emp: Yup.number().required('É obrigatório selecionar a empresa'),
    accountPaid: Yup.object().shape({
        layouts: Yup.array().of( Yup.object().shape({ 
            idLayout: Yup.string().required('É obrigatório selecionar o layout'),
        }))
    })
})

const defaultValues = {
    codi_emp: Number,
    accountPaid: {
        layouts: [{
            idLayout: ''
        }]
    }
}

let initialValues = {
    codi_emp: '',
    accountPaid: ''
}

let codiEmpOptions = []
async function companies() {
    try {
        const response = await api.get(`/extract_companies`)

        if(response.statusText === "OK"){
            response.data.map(companie => codiEmpOptions.push({
                value: `${companie['codi_emp']}`, label: `${companie['codi_emp']} - ${companie['razao_emp']}`
            }))
        }
    } catch (error) {
        console.log(error)
    }
}
companies()

export default function IntegrattionCompanies({history}){
    const [integrattionCompanies, setIntegrattionCompanies ] = useState([])

    // pega da url o id pra poder carregar os dados de edição
    const url = window.location.href
    const id = url.split('/')[4]

    useEffect(() => {
        async function loadIntegrattionCompanies() {
            try {
                let response = undefined

                // if(id !== undefined){
                //     response = await api.get(`/integrattion_companies/${id}`)
                // } else {
                //     response = await api.get(`/integrattion_companies`)
                // }
                
                // setIntegrattionCompanies(response.data)
            } catch (error) {
                console.log(error)
            }
        }
        loadIntegrattionCompanies()
    }, [id])
    
    if(integrattionCompanies._id !== undefined){

        initialValues = integrattionCompanies
    }

    return (
        <main className="content card container-fluid">
            <div className="card-header">
                <h5 className="mb-0">Configuração de Empresas X Layouts</h5>                
            </div>

            <div className="card-body">
                <Formik
                    enableReinitialize={true}
                    initialValues={initialValues}
                    validationSchema={validationSchema}
                    onSubmit={ 
                        async (values, { setSubmitting, resetForm }) => {
                            setSubmitting(true)

                            try {
                                let response = undefined

                                if(id !== undefined){
                                    response = await api.put(`/integrattion_companies/${id}`, { ...values } )
                                } else {
                                    response = await api.post('/integrattion_companies', { ...values } )
                                }

                                if(response.status !== 200){
                                    console.log(response)
                                }
                            } catch (error) {
                                console.log(error)
                            }
                            setSubmitting(false)                        
                            resetForm()
                            history.push('/integrattion_companies_list')
                    }}
                >
                    { ({ values, errors, touched, handleChange, handleBlur, setFieldTouched, setFieldValue, handleSubmit, isSubmitting }) => (
                        <form onSubmit={handleSubmit} className="container-fluid">
                            {/* <div className="d-flex">
                                <pre>{JSON.stringify(values, null, 2)}</pre>
                                <pre className="ml-4">{JSON.stringify(errors, null, 2)}</pre>
                            </div> */}
                            <div className="form-group row mb-0">                            
                                <label htmlFor="system" className="col-form-label font-weight-600">Empresa:</label>
                                <div className="col-8">
                                    <Form.Group className="mb-0">
                                        <Select 
                                            name={`codi_emp`}
                                            options={codiEmpOptions}
                                            className={`selected ${errors.codi_emp ? "has-error" : null }`}
                                            isSearchable={true}
                                            placeholder="Selecione"
                                            value={codiEmpOptions.filter(option => option.value === values.codi_emp)[0]}
                                            onChange={selectedOption => handleChange(`codi_emp`)(selectedOption.value)}
                                            onBlur={() => setFieldTouched(`codi_emp`, true)}
                                        />
                                        <Form.Control.Feedback type="invalid">{errors.codi_emp}</Form.Control.Feedback>
                                    </Form.Group>
                                </div>
                            </div>

                            < AccountPaid
                                values={values}
                                errors={errors}
                                touched={touched}
                                handleChange={handleChange}
                                handleBlur={handleBlur}
                                setFieldValue={setFieldValue}
                                setFieldTouched={setFieldTouched}
                                defaultValues={defaultValues}
                            /> 
                            
                            <div className="form-row">
                                <div className="col-12">
                                    <button className="btn btn-primary mr-2 col-1 offset-4" type="submit" disabled={isSubmitting}>Salvar</button>
                                    <button className="btn btn-secondary col-1" type="reset" 
                                        onClick={
                                            () => {
                                                const wishCanceled = window.confirm("Tem certeza que deseja cancelar?")
                                                if(wishCanceled === true){
                                                    history.push('/integrattion_companies_list')
                                                }
                                            }}
                                    >Cancelar</button>
                                </div>
                            </div>
                        </form>
                    )}
                </Formik>
            </div>
        </main>
    )
}