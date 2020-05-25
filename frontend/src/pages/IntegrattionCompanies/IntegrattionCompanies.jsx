import React, { useEffect, useState } from 'react'
import Select from 'react-select'
import { Form } from "react-bootstrap"
import * as Yup from 'yup'
import { Formik } from 'formik'
import '../styles.css'
import AccountPaid from './AccountPaid/AccountPaid'
import ProofPayment from './ProofPayment/ProofPayment'
const { api } = require('../../services/api')

let validationSchema = Yup.object().shape({
    codi_emp: Yup.number().required('É obrigatório selecionar a empresa'),
    accountPaid: Yup.object().shape({
        isReliable: Yup.boolean(),
        layouts: Yup.array().of( Yup.object().shape({ 
            idLayout: Yup.string().required('É obrigatório selecionar o layout'),
            bankAndAccountCorrelation: Yup.array().of( Yup.object().shape({
                bankFile: Yup.string().required('Campo obrigatório'),
                accountFile: Yup.string(),
                bankNew: Yup.string().required('Campo obrigatório'),
                accountNew: Yup.string()
            })),
            validateIfDataIsThisCompanie: Yup.array().of( Yup.object().shape({
                nameField: Yup.string().required('Campo obrigatório'),
                typeValidation: Yup.string().required('Campo obrigatório'),
                valueValidation: Yup.string().required('Campo obrigatório'),
                nextValidationOrAnd: Yup.string().required('Campo obrigatório')
            }))
        }))
    }),
    proofPayment: Yup.array().of( Yup.object().shape({
        value: Yup.number(),
        label: Yup.string()
    }))
})

const defaultValues = {
    codi_emp: '',
    accountPaid: {
        isReliable: true,
        layouts: [{
            idLayout: '',
            bankAndAccountCorrelation: [{
                bankFile: "",
                accountFile: "",
                bankNew: "",
                accountNew: ""
            }],
            validateIfDataIsThisCompanie: [{
                nameField: "",
                typeValidation: "",
                valueValidation: "",
                nextValidationOrAnd: "and"
            }]
        }]
    },
    proofPayment: [{
        value: "",
        label: ""
    }]
}

const initialValuesStruct = {
    codi_emp: '',
    accountPaid: '',
    proofPayment: []
}

let codiEmpOptions = []

export default function IntegrattionCompanies({history}){
    let initialValues = { ...initialValuesStruct }

    const [integrattionCompanies, setIntegrattionCompanies ] = useState([])
    // const [companies, setCompanies ] = useState([])

    // pega da url o id pra poder carregar os dados de edição
    const url = window.location.href
    const id = url.split('/')[4]

    useEffect(() => {
        async function loadIntegrattionCompanies() {
            try {
                let response = undefined

                if(id !== undefined){
                    response = await api.get(`/integrattion_companies/${id}`)
                } else {
                    response = await api.get(`/integrattion_companies`)
                }

                const responseCompanies = await api.get(`/extract_companies`)

                if(responseCompanies.statusText === "OK"){
                    codiEmpOptions = []
                    responseCompanies.data.map(companie => codiEmpOptions.push({
                        value: `${companie['codi_emp']}`, label: `${companie['codi_emp']} - ${companie['razao_emp']}`
                    }))
                }
                
                setIntegrattionCompanies(response.data)
            } catch (error) {
                console.log(error)
            }
        }
        loadIntegrattionCompanies()
    }, [id])
    
    if(integrattionCompanies._id !== undefined){

        for (let [key, value] of Object.entries(defaultValues)) {
            if( integrattionCompanies[key] === undefined ){
                integrattionCompanies[key] = value
            }
            
            if( key === "accountPaid" && integrattionCompanies[key].layouts.length > 0 ){
                for(let [keyAccountPaid, valueAccountPaid] of Object.entries(defaultValues['accountPaid'])){
                    if( integrattionCompanies[key][keyAccountPaid] === undefined ){
                        integrattionCompanies[key][keyAccountPaid] = valueAccountPaid
                    }

                    if(keyAccountPaid === 'layouts'){
                        for(let keyLayout in Object.entries(integrattionCompanies[key][keyAccountPaid])){
                            for(let [keyFieldLayout, valueFieldLayout] of Object.entries(defaultValues[key][keyAccountPaid][0])){
                                if(integrattionCompanies[key][keyAccountPaid][keyLayout][keyFieldLayout] === undefined && keyFieldLayout !== 'validateIfDataIsThisCompanie' && keyFieldLayout !== 'bankAndAccountCorrelation' ){
                                    integrattionCompanies[key][keyAccountPaid][keyLayout][keyFieldLayout] = valueFieldLayout
                                }
                                
                                if( ( keyFieldLayout === 'validateIfDataIsThisCompanie' || keyFieldLayout === 'bankAndAccountCorrelation' ) && integrattionCompanies[key][keyAccountPaid][keyLayout][keyFieldLayout] !== undefined){
                                    for(let keyValidateIfDataIsThisCompanie in Object.entries(integrattionCompanies[key][keyAccountPaid][keyLayout][keyFieldLayout])){
                                        for(let [keyFieldValidateIfDataIsThisCompanie, valueFieldkeyValidateIfDataIsThisCompanie] of Object.entries(defaultValues[key][keyAccountPaid][0][keyFieldLayout][0])){
                                            if(integrattionCompanies[key][keyAccountPaid][keyLayout][keyFieldLayout][keyValidateIfDataIsThisCompanie][keyFieldValidateIfDataIsThisCompanie] === undefined){
                                                integrattionCompanies[key][keyAccountPaid][keyLayout][keyFieldLayout][keyValidateIfDataIsThisCompanie][keyFieldValidateIfDataIsThisCompanie] = valueFieldkeyValidateIfDataIsThisCompanie
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

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
                                            value={codiEmpOptions.filter(option => option.value === `${values.codi_emp}`)[0]}
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

                            < ProofPayment
                                values={values}
                                errors={errors}
                                touched={touched}
                                handleChange={handleChange}
                                handleBlur={handleBlur}
                                setFieldValue={setFieldValue}
                                setFieldTouched={setFieldTouched}
                                defaultValues={defaultValues}
                            /> 
                            
                            <div className="form-row mt-2">
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