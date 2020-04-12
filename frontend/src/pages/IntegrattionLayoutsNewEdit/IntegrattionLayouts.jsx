import React, { useEffect, useState } from 'react'
import Select from 'react-select'
import { Form } from "react-bootstrap"
import * as Yup from 'yup'
import { Formik } from 'formik'

import './styles.css'
import api from '../../services/api'
import IntegrattionLayoutsHeader from './FieldsHeader/FieldsHeader'
import IntegrattionLayoutsFieldsList from './FieldsBody/FieldsList'
import IntegrattionLayoutsFieldsListValidation from './FieldsValidationData/FieldsListValidation'
import LinesOfFile from './LinesOfFile/LinesOfFile'

let validationSchema = Yup.object().shape({
    system: Yup.string().required('O nome do sistema é obrigatório'),
    fileType: Yup.string().required('Selecione uma opção válida'),
    splitFile: Yup.string(),
    layoutType: Yup.string().required('Selecione uma opção válida'),
    header: Yup.array().of( Yup.object().shape({
        nameColumn: Yup.string().required('O nome da coluna é obrigatório')
    })),
    fields: Yup.array().of( Yup.object().shape({ 
        nameField: Yup.string().required('Selecione uma opção válida'),
        positionInFile: Yup.number().integer('Selecione uma opção válida'),
        positionInFileEnd: Yup.number(),
        nameColumn: Yup.string(),
        formatDate: Yup.string(),
        splitField: Yup.string(),
        positionFieldInTheSplit: Yup.number(),
        positionFieldInTheSplitEnd: Yup.number(),        
        lineThatTheDataIs: Yup.string()
    })),
    validationLineToPrint: Yup.array().of( Yup.object().shape({
        nameField: Yup.string(),
        typeValidation: Yup.string(),
        valueValidation: Yup.string(),
        nextValidationOrAnd: Yup.string()
    })),
    linesOfFile: Yup.array().of( Yup.object().shape({
        nameOfLine: Yup.object().shape({
            value: Yup.string(),
            label: Yup.string().required('O nome da linha é obrigatório')
        }),
        informationIsOnOneLineBelowTheMain: Yup.boolean(),
        validations: Yup.array().of( Yup.object().shape({
            positionInFile: Yup.number().required('Campo obrigatório'),
            positionInFileEnd: Yup.number(),
            typeValidation: Yup.string().required('Campo obrigatório'),
            valueValidation: Yup.string().required('Campo obrigatório'),
            nextValidationOrAnd: Yup.string().required('Campo obrigatório')
        }))    
    }))
})

const defaultValues = {
    system: "",
    fileType: "",
    splitFile: "",
    layoutType: "account_paid",
    header: [ { nameColumn: ""} ],
    fields: [ {
        nameField: "",
        positionInFile: "",
        positionInFileEnd: 0,
        nameColumn: "",
        formatDate: "",
        splitField: "",
        positionFieldInTheSplit: 0,
        positionFieldInTheSplitEnd: 0,
        lineThatTheDataIs: ""
    } ],
    validationLineToPrint: [{
        nameField: "",
        typeValidation: "",
        valueValidation: "",
        nextValidationOrAnd: "and"
    }],
    linesOfFile: [{
        nameOfLine: { value: '', label: '' },
        informationIsOnOneLineBelowTheMain: false,
        validations: [{
            positionInFile: "",
            positionInFileEnd: 0,
            typeValidation: "",
            valueValidation: "",
            nextValidationOrAnd: "and"
        }]        
    }]
}

let initialValues = {
    system: "",
    fileType: "",
    splitFile: "",
    layoutType: "account_paid",
    header: [],
    fields: [ {
        nameField: "",
        positionInFile: "",
        positionInFileEnd: 0,
        nameColumn: "",
        formatDate: "",
        splitField: "",
        positionFieldInTheSplit: 0,
        positionFieldInTheSplitEnd: 0,
        lineThatTheDataIs: ""
    } ],
    validationLineToPrint: [{
        nameField: "paymentDate",
        typeValidation: "isDate",
        valueValidation: "",
        nextValidationOrAnd: "and"
    }, {
        nameField: "amountPaid",
        typeValidation: "isDifferent",
        valueValidation: "0",
        nextValidationOrAnd: "and"
    }],
    linesOfFile: []
}

const fileTypes = [
    { value: 'excel', label: 'Excel'},
    { value: 'txt', label: 'Texto'},
    { value: 'csv', label: 'CSV'},
    { value: 'pdf', label: 'PDF'}
]

// const layoutTypes = [
//     { value: 'account_paid', label: 'Contas Pagas'},
//     { value: 'extract', label: 'Extrato Bancário'}
// ]

export default function IntegrattionLayouts({history}){
    const [integrattionLayout, setIntegrattionLayout ] = useState([])

    // pega da url o id pra poder carregar os dados de edição
    const url = window.location.href
    const id = url.split('/')[4]

    useEffect(() => {
        async function loadIntegrattionLayout() {
            try {
                let response = undefined

                if(id !== undefined){
                    response = await api.get(`/integrattion_layouts/${id}`)
                } else {
                    response = await api.get(`/integrattion_layouts`)
                }
                
                setIntegrattionLayout(response.data)
            } catch (error) {
                console.log(error)
            }
        }
        loadIntegrattionLayout()
    }, [id])
    
    if(integrattionLayout._id !== undefined){

        for (let [key, value] of Object.entries(initialValues)) {
            if( integrattionLayout[key] === undefined ){
                integrattionLayout[key] = value
            }
            // este for pega os campos do header que não existem no mongo e adiciona o valor padrão. Isto é necessário por causa disto daqui do react https://reactjs.org/docs/forms.html#controlled-components
            if( key === "header" && integrattionLayout[key].length > 0 ){
                for(let idxHeader in integrattionLayout[key]){
                    for(let [keyHeader, valueHeader] of Object.entries(initialValues[key][0])){
                        if( integrattionLayout[key][idxHeader][keyHeader] === undefined ){
                            integrattionLayout[key][idxHeader][keyHeader] = valueHeader
                        }
                    }
                }
            }
            if( key === "fields" && integrattionLayout[key].length > 0 ){
                for(let idxFields in integrattionLayout[key]){
                    for(let [keyFields, valueFields] of Object.entries(initialValues[key][0])){
                        if( integrattionLayout[key][idxFields][keyFields] === undefined ){
                            integrattionLayout[key][idxFields][keyFields] = valueFields
                        }
                    }
                }
            }
            if( key === "validationLineToPrint" && integrattionLayout[key].length > 0 ){
                for(let idxValidationLineToPrint in integrattionLayout[key]){
                    for(let [keyValidationLineToPrint, valueValidationLineToPrint] of Object.entries(initialValues[key][0])){
                        if( integrattionLayout[key][idxValidationLineToPrint][keyValidationLineToPrint] === undefined ){
                            integrattionLayout[key][idxValidationLineToPrint][keyValidationLineToPrint] = valueValidationLineToPrint
                        }
                    }
                }
            }
            if( key === "linesOfFile" && integrattionLayout[key].length > 0 ){
                for(let idxLinesOfFile in integrattionLayout[key]){
                    for(let [keyLinesOfFile, valueLinesOfFile] of Object.entries(initialValues[key][0])){
                        if( integrattionLayout[key][idxLinesOfFile][keyLinesOfFile] === undefined ){
                            integrattionLayout[key][idxLinesOfFile][keyLinesOfFile] = valueLinesOfFile
                            // este for de baixo pro array de validations que tem dentro do linesOfFile
                            if( keyLinesOfFile === "validations" && integrattionLayout[key][idxLinesOfFile][keyLinesOfFile].length > 0 ){
                                for(let idxValidations in integrattionLayout[key][idxLinesOfFile][keyLinesOfFile]){
                                    for(let [keyValidations, valueValidations] of Object.entries(integrattionLayout[key][0][keyLinesOfFile][0])){
                                        if( integrattionLayout[key][idxLinesOfFile][keyLinesOfFile][idxValidations][keyValidations] === undefined ){
                                            integrattionLayout[key][idxLinesOfFile][keyLinesOfFile][idxValidations][keyValidations] = valueValidations
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        initialValues = integrattionLayout
    }

    function fieldSplitFile(values, handleChange, handleBlur){
        if(values.fileType !== "excel" && values.fileType !== ""){
            return (
                <>
                    <label htmlFor="layoutType" className="col-form-label font-weight-600">Separador de campos do arquivo:</label>
                    <div className="col-3">
                        <Form.Control 
                            id="splitFile"
                            name="splitFile"
                            type="text" 
                            className={`form-control`}
                            placeholder="Informe o separador se houver"
                            value={values.splitFile}
                            onChange={handleChange}
                            onBlur={handleBlur}
                        />
                    </div>
                </>
            )
        }
    }

    return (
        <main className="content card container-fluid">
            <div className="card-header">
                <h5 className="mb-0">Configuração de Layout</h5>                
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
                                    response = await api.put(`/integrattion_layouts/${id}`, { ...values } )
                                } else {
                                    response = await api.post('/integrattion_layouts', { ...values } )
                                }

                                if(response.status !== 200){
                                    console.log(response)
                                }
                            } catch (error) {
                                console.log(error)
                            }
                            setSubmitting(false)                        
                            resetForm()
                            history.push('/integrattion_layouts_list')
                    }}
                >
                    { ({ values, errors, touched, handleChange, handleBlur, setFieldTouched, setFieldValue, handleSubmit, isSubmitting }) => (
                        <form onSubmit={handleSubmit} className="container-fluid">
                            <pre>{JSON.stringify(errors, null, 2)}</pre>
                            <div className="form-group row mb-0">                            
                                <label htmlFor="system" className="col-form-label font-weight-600">Sistema:</label>
                                <div className="col">
                                    <Form.Group className="mb-0">
                                        <Form.Control 
                                            id="system"
                                            type="text" 
                                            className={`form-control ${errors.system ? "has-error" : null }`}
                                            placeholder="Informe o nome do sistema"
                                            value={values.system}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                        <Form.Control.Feedback type="invalid">{errors.system}</Form.Control.Feedback>
                                    </Form.Group>
                                </div>
                            </div>

                            <div className="form-group row mt-2 mb-0">
                                <label htmlFor="fileType" className="col-form-label font-weight-600">Tipo Arquivo:</label>
                                <div className="col-3">
                                    <Form.Group className="mb-0">
                                        <Select 
                                            id="fileType"
                                            options={fileTypes}
                                            className={`selected height-calc ${errors.fileType ? "has-error" : null }`}
                                            isSearchable={true}
                                            placeholder="Selecione"
                                            value={fileTypes.filter(option => option.value === values.fileType)[0]}
                                            onChange={selectedOption => handleChange("fileType")(selectedOption.value)}
                                            onBlur={() => setFieldTouched("fileType", true)}
                                        />
                                        <Form.Control.Feedback type="invalid">{errors.fileType}</Form.Control.Feedback>
                                    </Form.Group>
                                </div>

                                {fieldSplitFile(values, handleChange, handleBlur)}
                            </div>
                            
                            < IntegrattionLayoutsHeader
                                values={values}
                                errors={errors}
                                touched={touched}
                                handleChange={handleChange}
                                handleBlur={handleBlur}
                                setFieldValue={setFieldValue}
                                setFieldTouched={setFieldTouched}
                            /> 

                            < LinesOfFile
                                values={values}
                                errors={errors}
                                touched={touched}
                                handleChange={handleChange}
                                handleBlur={handleBlur}
                                setFieldValue={setFieldValue}
                                setFieldTouched={setFieldTouched}
                                defaultValues={defaultValues}
                            />

                            <div className="form row mt-2">
                                <label className="col-form-label font-weight-600">Configuração dos Campos do Layout:</label>                                
                            </div>

                            < IntegrattionLayoutsFieldsList
                                values={values}
                                errors={errors}
                                touched={touched}
                                handleChange={handleChange}
                                handleBlur={handleBlur}
                                setFieldValue={setFieldValue}
                                setFieldTouched={setFieldTouched}
                                defaultValues={defaultValues}
                                initialValues={values}
                            />

                            < IntegrattionLayoutsFieldsListValidation
                                values={values}
                                errors={errors}
                                touched={touched}
                                handleChange={handleChange}
                                handleBlur={handleBlur}
                                setFieldValue={setFieldValue}
                                setFieldTouched={setFieldTouched}
                            />

                            <div className="form-row">
                                <div className="col-12">
                                    <button className="btn btn-primary mr-2 col-1 offset-4" type="submit" disabled={isSubmitting}>Salvar</button>
                                    <button className="btn btn-secondary col-1" type="reset">Cancelar</button>
                                </div>
                            </div>
                        </form>
                    )}
                </Formik>
            </div>
        </main>
    )
}