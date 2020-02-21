import React, { useState } from 'react'

import './styles.css'
import api from '../services/api'
import IntegrattionLayoutsHeader from './IntegrattionLayoutsHeader'

export default function IntegrattionLayouts(){

    const [system, setSystem] = useState('')
    
    const [fileType] = useState(['Selecione', 'Excel', 'Texto'])
    const addFileType = fileType.map( add => add )
    let valueFileType = ''
    function handleFileType(event){
        valueFileType = event.target.value
    }

    const [layoutType] = useState(['Selecione', 'Financeiro'])
    const addLayoutType = layoutType.map( add => add )
    let valueLayoutType = ''
    function handleLayoutType(event){
        valueLayoutType = event.target.value
    }

    const blankFieldsHeader = { nameField: '' };
    const [fieldsHeader, setFieldsHeader] = useState( [ { ...blankFieldsHeader } ]) 

    const handleFieldHeaderChange = (event) => {
        let nameClass = event.target.className
        nameClass = nameClass.split(' ')[0]

        const updatedFieldHeader = [...fieldsHeader];
        // na linha abaixo o dataset.idx eu pego o ID da posição no array, e o nameClass eu pego o campo (field) dentro do objeto daquele array
        updatedFieldHeader[event.target.dataset.idx][nameClass] = event.target.value;
        setFieldsHeader(updatedFieldHeader);
    };

    const addFieldHeader = () => {
        setFieldsHeader([...fieldsHeader, { ...blankFieldsHeader }]);
    };

    const deleteFieldHeader = (event) => {
        const updatedFieldHeader = [...fieldsHeader];
        // na linha abaixo o dataset.idx eu pego o ID da posição no array, e o nameClass eu pego o campo (field) dentro do objeto daquele array
        updatedFieldHeader.splice([event.target.dataset.idx], 1)
        setFieldsHeader(updatedFieldHeader);
    };
    
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

                    <div className="form-group row">
                        <label htmlFor="fileType" className="col-form-label">Tipo Arquivo:</label>
                        <div className="col-3">
                            <select 
                                id="fileType"
                                name="fileType" 
                                className="form-control"
                                onChange={event => handleFileType(event)}
                            >
                                {
                                    addFileType.map( (fileType) => <option key={fileType} value={fileType}>{fileType}</option> )
                                }
                            </select>
                        </div>

                        <label htmlFor="layoutType" className="col-form-label">Tipo Layout:</label>
                        <div className="col-3">
                            <select 
                                id="layoutType"
                                name="layoutType" 
                                className="form-control"
                                onChange={event => handleLayoutType(event)}
                            >
                                {
                                    addLayoutType.map( (layoutType) => <option key={layoutType} value={layoutType}>{layoutType}</option> )
                                }
                            </select>
                        </div>
                    </div>
                    
                    <div className="form row">
                        <label className="col-form-label">Campos que identificam o Cabeçalho do Arquivo:</label>
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