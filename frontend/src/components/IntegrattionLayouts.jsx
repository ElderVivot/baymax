import React, { useState } from 'react'
import Select from 'react-select'
import * as yup from 'yup'
import Formik from 'formik'

import './styles.css'
import api from '../services/api'
import IntegrattionLayoutsHeader from './IntegrattionLayoutsHeader'
import IntegrattionLayoutsFieldsNewOrEdit from './IntegrattionLayoutsFieldsNewOrEdit'
import IntegrattionLayoutsFieldsList from './IntegrattionLayoutsFieldsList'

let schema = yup.object().shape({
    system: yup.string().required(),
    fileType: yup.string().required(),
    layoutType: yup.string().required()
})

export default function IntegrattionLayouts(){

    // Muda valor do "Sistema"
    const [system, setSystem] = useState('')

    // Muda valor do "Tipo Arquivo"
    const fileTypes = [
        { value: 'excel', label: 'Excel'},
        { value: 'txt', label: 'Texto'}
    ]
    let valueFileType = ''
    function handleFileTypes(fileTypeSelect){
        valueFileType = fileTypeSelect.value
    }

    // Muda valor do "Tipo Layout"
    const layoutTypes = [
        { value: 'financy', label: 'Financeiro'},
        { value: 'extract', label: 'Extrato Bancário'}
    ]
    let valueLayoutType = ''
    function handleLayoutTypes(layoutTypeSelect){
        valueLayoutType = layoutTypeSelect.value
    }

    // --------- Trata os campos do cabeçalho do arquivo (adicionar, alterar, excluir) -------------
    const blankFieldsHeader = { nameField: '' }
    const [fieldsHeader, setFieldsHeader] = useState( [ { ...blankFieldsHeader } ]) 

    const handleFieldHeaderChange = (event) => {
        let nameClass = event.target.className
        nameClass = nameClass.split(' ')[0]

        const updatedFieldHeader = [...fieldsHeader]
        // na linha abaixo o dataset.idx eu pego o ID da posição no array, e o nameClass eu pego o campo (field) dentro do objeto daquele array
        updatedFieldHeader[event.target.dataset.idx][nameClass] = event.target.value
        setFieldsHeader(updatedFieldHeader)
    };

    const addFieldHeader = () => {
        setFieldsHeader([...fieldsHeader, { ...blankFieldsHeader }])
    };
    
    const deleteFieldHeader = (event) => {
        const updatedFieldHeader = [...fieldsHeader]
        // na linha abaixo o dataset.idx eu pego o ID da posição no array, e o nameClass eu pego o campo (field) dentro do objeto daquele array
        updatedFieldHeader.splice([event.target.dataset.idx], 1)
        setFieldsHeader(updatedFieldHeader)
    };
    // --------------- Fim do Tratamento dos dados do Cabeçalho ---------------

    // --------- Trata os campos do arquivo (adicionar, alterar, excluir) -------------
    const blankFieldsFile = { 
        nameField: { value: '', label: ''},
        positionInFile: { value: '', label: '' },
        positionInFileEnd: { value: '', label: '' },
        nameColumn: '',
        formatDate: {value: '', label: ''}
    }
    const [fieldsFile, setFieldsFile] = useState( [ { ...blankFieldsFile } ]) 

    const handleFieldFileChange = (event, attributes="") => {
        
        let nameClass = ""
        let idx = -1
        let value = ""
        if(attributes === "") {
            nameClass = event.target.className
            nameClass = nameClass.split(' ')[0]

            idx = event.target.dataset.idx

            value = event.target.value
        } else {
            nameClass = attributes.nameClass
            idx = attributes.idx

            if(attributes.eventType === "selected"){
                value = event
            } else {
                value = event.target.value
            }
        }

        const updatedFieldFile = [...fieldsFile]
        updatedFieldFile[idx][nameClass] = value
        setFieldsFile(updatedFieldFile)
    };
    console.log(fieldsFile)

    // const addFieldFile = () => {
    //     setFieldsFile([...fieldsFile, { ...blankFieldsFile }])
    // };
    
    // const deleteFieldFile = (event) => {
    //     const updatedFieldFile = [...fieldsFile]
    //     // na linha abaixo o dataset.idx eu pego o ID da posição no array, e o nameClass eu pego o campo (field) dentro do objeto daquele array
    //     updatedFieldFile.splice([event.target.dataset.idx], 1)
    //     setFieldsFile(updatedFieldFile)
    // };
    // --------------- Fim do Tratamento dos dados do Arquivo ---------------
    
    // Salva os dados no MongoDB
    async function handleSubmit(event) {
        event.preventDefault()

        const response = await api.post('/integrattion_layouts', {
            system,
            "fileType": valueFileType,
            "layoutType": valueLayoutType,
            "header": fieldsHeader
        } )

        console.log(response)
    }

    return (
        <div className="card">
            <div className="card-header">
                <h5 className="mb-0">Configuração de Layout</h5>
            </div>

            <div className="card-body">
                <form action="" className="container-fluid">
                    {/* Campo "Sistema" */}
                    <div className="form-group row">
                        <label htmlFor="system" className="col-form-label">Sistema:</label>
                        <div className="col">
                            <input 
                                id="system"
                                type="text" 
                                className="form-control" 
                                placeholder="Informe o nome do sistema"
                                value={system}
                                onChange={event => setSystem(event.target.value)}
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
                                onChange={handleFileTypes}
                                className="selected"
                                isSearchable="true"
                                placeholder="Selecione"
                            />
                        </div>

                        <label htmlFor="layoutType" className="col-form-label">Tipo Layout:</label>
                        <div className="col-3">
                            <Select 
                                id="layoutType"
                                options={layoutTypes}
                                onChange={handleLayoutTypes}
                                className="selected"
                                isSearchable="true"
                                placeholder="Selecione"
                            />
                        </div>
                    </div>
                    
                    <div className="form row">
                        <label className="col-form-label">Nome dos campos que identifica as colunas do Arquivo:</label>
                    </div>
                    <table className="col-12">
                        <tbody>
                            {
                                fieldsHeader.map( (field, idx) => (
                                    < IntegrattionLayoutsHeader
                                        key={`fieldHeader-${idx}`}
                                        idx={idx}
                                        fieldsHeader={fieldsHeader}
                                        handleFieldHeaderChange={handleFieldHeaderChange}
                                        addFieldHeader={addFieldHeader}
                                        deleteFieldHeader={deleteFieldHeader}
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
                                fieldsFile.map( (field, idx) => (
                                    < IntegrattionLayoutsFieldsList
                                        key={`fieldFile-${idx}`}
                                        idx={idx}
                                        fieldsFile={fieldsFile}
                                    /> 
                                ))
                            }
                            </tbody>
                        </table>
                    </div>
                    
                    < IntegrattionLayoutsFieldsNewOrEdit
                        key={`fieldFile-${0}`}
                        idx={0}
                        fieldsFile={fieldsFile}
                        handleFieldFileChange={handleFieldFileChange}
                    />

                    <div className="form-row">
                        <div className="col-12">
                            <button className="btn btn-primary mr-2 col-1 offset-4" type="submit" onClick={event => handleSubmit(event)}>Salvar</button>
                            <button className="btn btn-secondary col-1" type="reset">Cancelar</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    )
}