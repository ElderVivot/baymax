import React, { useState } from 'react'

import './styles.css'
import api from '../../services/api'
import IntegrattionLayoutsHeader from '../integrattion_layouts_header/index'

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

    async function handleSubmit(event) {
        event.preventDefault()

        const response = await api.post('/integrattion_layouts', {
            system,
            "fileType": valueFileType,
            "layoutType": valueLayoutType
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
                    < IntegrattionLayoutsHeader />

                    <div className="form-row mb-0">
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