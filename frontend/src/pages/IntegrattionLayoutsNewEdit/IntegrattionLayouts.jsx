import React, { useEffect, useState } from 'react'
import Select from 'react-select'
import * as Yup from 'yup'
import { Formik } from 'formik'

import './styles.css'
import api from '../../services/api'
import IntegrattionLayoutsHeader from './FieldsHeader/FieldsHeader'
import IntegrattionLayoutsFieldsList from './FieldsBody/FieldsList'
import Error from '../../components/Error'

let validationSchema = Yup.object().shape({
    system: Yup.string().required('O nome do sistema é obrigatório'),
    fileType: Yup.string().required('Selecione uma opção válida'),
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
        informationIsOnOneLineBelowTheMain: Yup.boolean(),
        lineThatTheDataIs: Yup.string()
    })),
    validationLineToPrint: Yup.array().of( Yup.object().shape({
        nameField: String,
        typeValidation: String,
        valueValidation: String
    })),
    linesOfFile: Yup.array().of( Yup.object().shape({
        nameOfLine: String,
        validations: Yup.array().of( Yup.object().shape({
            positionInFile: Number,
            positionInFileEnd: Number,
            typeValidation: String,
            valueValidation: String,
            nextValidationOrAnd: String
        }))    
    }))
})

let initialValues = {
    system: "",
    fileType: "",
    layoutType: "",
    header: [ { nameColumn: ""} ],
    fields: [ {
        nameField: "",
        positionInFile: "",
        positionInFileEnd: "",
        nameColumn: "",
        formatDate: "",
        splitField: "",
        positionFieldInTheSplit: 0,
        positionFieldInTheSplitEnd: 0,
        informationIsOnOneLineBelowTheMain: false,
        lineThatTheDataIs: ""
    } ],
    validationLineToPrint: [{
        nameField: "",
        typeValidation: "",
        valueValidation: ""
    }],
    linesOfFile: [{
        nameOfLine: "",
        validations: [{
            positionInFile: "",
            positionInFileEnd: "",
            typeValidation: "",
            valueValidation: "",
            nextValidationOrAnd: ""
        }]        
    }]
}

const fileTypes = [
    { value: 'excel', label: 'Excel'},
    { value: 'txt', label: 'Texto'}
]

const layoutTypes = [
    { value: 'account_paid', label: 'Contas Pagas'},
    { value: 'extract', label: 'Extrato Bancário'}
]

// function getOffset(element){
//     const rect = element.getBoundingClientRect();
//     return {
//         left: rect.left + window.scrollX,
//         top: rect.top + window.scrollY
//     };
// }

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
        
        initialValues = integrattionLayout

        for (var [key, value] of Object.entries(integrattionLayout)) {
            console.log(key + ' ' + value);
        }
        // initialValues.fields.map()
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
                    onSubmit={ async (values, { setSubmitting, resetForm }) => {
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
                            <div className="form-group row mb-0">
                                <label htmlFor="system" className="col-form-label font-weight-600">Sistema:</label>
                                <div className="col">
                                    <input 
                                        id="system"
                                        type="text" 
                                        className={`form-control ${touched.system && errors.system ? "has-error" : null }`}
                                        placeholder="Informe o nome do sistema"
                                        value={values.system}
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                    />
                                </div>
                            </div>
                            <div className="form-group row mb-0">
                                <Error touched={touched.system} message={errors.system}/>
                            </div>
                            {/* {console.log(document.getElementById('system'))} */}

                            <div className="form-group row mt-2 mb-0">
                                <label htmlFor="fileType" className="col-form-label font-weight-600">Tipo Arquivo:</label>
                                <div className="col-3">
                                    <Select 
                                        id="fileType"
                                        options={fileTypes}
                                        className={`selected height-calc ${touched.fileType && errors.fileType ? "has-error" : null }`}
                                        isSearchable={true}
                                        placeholder="Selecione"
                                        value={fileTypes.filter(option => option.value === values.fileType)[0]}
                                        onChange={selectedOption => handleChange("fileType")(selectedOption.value)}
                                        onBlur={() => setFieldTouched("fileType", true)}
                                    />
                                </div>

                                <label htmlFor="layoutType" className="col-form-label font-weight-600">Tipo Layout:</label>
                                <div className="col-3">
                                    <Select 
                                        id="layoutType"
                                        options={layoutTypes}
                                        className={`selected ${touched.layoutType && errors.layoutType ? "has-error" : null }`}
                                        isSearchable="true"
                                        placeholder="Selecione"
                                        value={layoutTypes.filter(option => option.value === values.layoutType)[0]}
                                        onChange={selectedOption => handleChange("layoutType")(selectedOption.value)}
                                        onBlur={() => setFieldTouched("layoutType", true)}
                                    />
                                </div>
                            </div>
                            <div className="form-group row mb-0">
                                <Error className="m-0 p-0" touched={touched.fileType} message={errors.fileType}/>
                            </div>
                            
                            <div className="form row mt-2 mb-0">
                                <label className="col-form-label font-weight-600">Nome dos campos que identifica as colunas do Arquivo (informe 2 ou 3):</label>
                                <button className="btn btn-success btn-sm btn10px ml-3 mt-1" type="button" style={{height:25}}
                                    onClick={() => setFieldValue("header", [...values.header, { nameColumn: "" }]) }>
                                    <i className="fa fa-plus"></i>
                                </button>
                                
                            </div>
                            <table className="col-12">
                                <tbody>
                                    {
                                        values.header.map( (field, idx) => (
                                            < IntegrattionLayoutsHeader
                                                key={`fieldHeader-${idx}`}
                                                idx={idx}
                                                fieldsHeader={values.header}
                                                errors={errors}
                                                touched={touched}
                                                handleChange={handleChange}
                                                handleBlur={handleBlur}
                                                setFieldValue={setFieldValue}
                                            /> 
                                        ))
                                    }
                                </tbody>
                            </table>

                            <div className="form row mt-2">
                                <label className="col-form-label font-weight-600">Configuração dos Campos do Layout:</label>                                
                            </div>

                            <div className="form row">
                                <table className="table ml-3 table-striped table-bordered table-hover">
                                    <thead>
                                        <tr className="d-flex justify-content-center text-center">
                                        {/* <tr className="flex-container"> */}
                                            <th className="col-4 fields-of-table align-center">Campo</th>
                                            <th className="col-1 fields-of-table align-center">Posição Inicial</th>
                                            <th className="col-1 fields-of-table align-center">Posição Final</th>
                                            <th className="col-3 fields-of-table align-center">Nome Coluna</th>
                                            <th className="col-1 fields-of-table align-center">Formato Data</th>
                                            <th className="col-2 fields-of-table align-center">
                                                <div className="div">Ações</div>
                                                <button className="btn btn-success btn-sm btn10px ml-3" type="button" style={{height:25}}
                                                    onClick={() => {
                                                        setFieldValue("fields", [...values.fields, { 
                                                            nameField: "",
                                                            positionInFile: "",
                                                            positionInFileEnd: "",
                                                            nameColumn: "",
                                                            formatDate: ""
                                                        }])
                                                    } }>
                                                    <i className="fa fa-plus"></i>
                                                </button>
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>{
                                        values.fields.map( (field, idx) => (
                                            < IntegrattionLayoutsFieldsList
                                                key={`fieldFile-${idx}`}
                                                idx={idx}
                                                fieldsFile={values.fields}
                                                setFieldValue={setFieldValue}
                                                initialValues={values.fields}
                                            /> 
                                        ))
                                    }
                                    </tbody>
                                </table>
                            </div>

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