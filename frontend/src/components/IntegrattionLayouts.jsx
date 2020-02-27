import React from 'react'
import Select from 'react-select'
import * as Yup from 'yup'
import { Formik } from 'formik'

import './styles.css'
import api from '../services/api'
import IntegrattionLayoutsHeader from './IntegrattionLayoutsHeader'
import IntegrattionLayoutsFieldsList from './IntegrattionLayoutsFieldsList'

let validationSchema = Yup.object().shape({
    system: Yup.string().required('O nome do sistema é obrigatório'),
    fileType: Yup.string().required('Selecione uma opção válida'),
    layoutType: Yup.string().required('Selecione uma opção válida'),
    header: Yup.array().of( Yup.object().shape({
        nameField: Yup.string().required('O nome da coluna é obrigatório')
    })),
    fields: Yup.array().of( Yup.object().shape({ 
        nameField: Yup.string().required('Selecione uma opção válida'),
        positionInFile: Yup.number().integer('Selecione uma opção válida'),
        positionInFileEnd: Yup.number(),
        nameColumn: Yup.string(),
        formatDate: Yup.number(),
    }))
})

let initialValues={
    system: "",
    fileType: "",
    layoutType: "",
    header: [ { nameField: ""} ],
    fields: [ {
        nameField: "",
        positionInFile: "",
        positionInFileEnd: "",
        nameColumn: "",
        formatDate: ""
    } ]
}

const fileTypes = [
    { value: 'excel', label: 'Excel'},
    { value: 'txt', label: 'Texto'}
]

const layoutTypes = [
    { value: 'financy', label: 'Financeiro'},
    { value: 'extract', label: 'Extrato Bancário'}
]

export default function IntegrattionLayouts(){

    // Salva os dados no MongoDB
    // async function handleSubmit(event, data) {
    //     event.preventDefault()

    //     const response = await api.post('/integrattion_layouts', { ...data } )

    //     console.log(response)
    // }

    return (
        <div className="card">
            <div className="card-header">
                <h5 className="mb-0">Configuração de Layout</h5>
            </div>

            <div className="card-body">
                <Formik
                    initialValues={initialValues}
                    validationSchema={validationSchema}
                >
                    { ({ values, errors, touched, handleChange, handleBlur, setFieldTouched, setFieldValue }) => (
                        <form action="" className="container-fluid">
                            {/* Campo "Sistema" */}
                            <div className="form-group row">
                                <label htmlFor="system" className="col-form-label">Sistema:</label>
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

                            {/* Campo Tipo Arquivo e Tipo Layout */}
                            <div className="form-group row">
                                <label htmlFor="fileType" className="col-form-label">Tipo Arquivo:</label>
                                <div className="col-3">
                                    <Select 
                                        id="fileType"
                                        options={fileTypes}
                                        className={`selected ${touched.fileType && errors.fileType ? "has-error" : null }`}
                                        isSearchable={true}
                                        placeholder="Selecione"
                                        value={fileTypes.filter(option => option.value === values.fileType)[0]}
                                        onChange={selectedOption => handleChange("fileType")(selectedOption.value)}
                                        onBlur={() => setFieldTouched("fileType", true)}
                                    />
                                </div>

                                <label htmlFor="layoutType" className="col-form-label">Tipo Layout:</label>
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
                            
                            <div className="form row">
                                <label className="col-form-label">Nome dos campos que identifica as colunas do Arquivo:</label>
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
                                <label className="col-form-label">Configuração dos Campos do Layout:</label>
                            </div>

                            <div className="form row">
                                <table className="table ml-3 table-striped table-bordered table-hover">
                                    <thead>
                                        <tr className="d-flex">
                                            <th className="col-4 fields-of-table">Campo</th>
                                            <th className="col-1 fields-of-table">Posição Inicial</th>
                                            <th className="col-1 fields-of-table">Posição Final</th>
                                            <th className="col-3 fields-of-table">Nome Coluna</th>
                                            <th className="col-1 fields-of-table">Formato Data</th>
                                            <th className="col-2 fields-of-table">Ações</th>
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
                                    <button className="btn btn-primary mr-2 col-1 offset-4" type="submit">Salvar</button>
                                    <button className="btn btn-secondary col-1" type="reset">Cancelar</button>
                                </div>
                            </div>
                        </form>
                    )}
                </Formik>
            </div>
        </div>
    )
}