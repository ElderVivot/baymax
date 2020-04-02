import './styles.css'
import React, { useEffect, useState } from 'react'
import api from '../../services/api'
import BootstrapTable from 'react-bootstrap-table-next'
import filterFactory, { textFilter, Comparator } from 'react-bootstrap-table2-filter';

const IntegrattionLayoutsList = ( {history} ) => {
    const [integrattionLayouts, setIntegrattionLayouts ] = useState([])

    const editIntegrattionLayout = (id) => {
        history.push(`/integrattion_layouts/${id}`)
    }

    const addIntegrattionLayout = () => {
        history.push('/integrattion_layouts')
    }

    const deleteIntegrattionLayout = async (id) => {
        const wishDelete = window.confirm("Deseja deletar?")
        if(wishDelete === true){
            try {
                const response = await api.delete(`/integrattion_layouts/${id}`)

                // if(response.status === 200){
                //     return(
                //         <div class="alert alert-primary" role="alert">Layout excluído com sucesso</div>
                //     )                    
                // } else {
                //     return(
                //         <div class="alert alert-danger" role="alert">Não foi possível deletar. Tente novamente</div>
                //     )                    
                // }
            } catch (error) {
                console.log(error)
                // return(
                //     <div class="alert alert-danger" role="alert">Não foi possível deletar. Tente novamente</div>
                // )                
            }
            
            history.push('/integrattion_layouts_list')
        }
    }

    const systemFilter = textFilter({
        placeholder: 'Informe o nome sistema',
        style: { height: 25 }
    })
    const fileTypeFilter = textFilter({
        placeholder: 'Informe o tipo arquivo',
        style: { height: 25 }
    })
    const filterLenght = textFilter({
        placeholder: 'Informe a Quantidade',
        comparator: Comparator.EQ,
        style: { height: 25 }
    })

    const columns = [{
        dataField: 'system',
        text: 'Sistema',
        sort: true,
        filter: systemFilter
    }, {
        dataField: 'fileType',
        text: 'Tipo Arquivo',
        sort: true,
        filter: fileTypeFilter
    }, {
        dataField: 'lenghtHeader',
        text: 'Qtd Campos Cabeçalho',
        sort: true,
        filter: filterLenght
    }, {
        dataField: 'lenghtFields',
        text: 'Qtd Campos do Arquivo',
        sort: true,
        filter: filterLenght
    }, { 
        dataField: "actions", 
        isDummyField: true,
        text: "Ações",
        sort: false,
        headerFormatter: (column, colIndex) => {
            return (
                <div>
                    <div style={{"marginBottom": 2}}>{column.text}</div>
                    <button className="btn btn-success btn-sm btn10px" style={{"marginTop": 1}} type="button" onClick={addIntegrattionLayout}>
                        <i className="fa fa-plus"></i>
                    </button>
                </div>
            )
        },
        formatter: (cellContent, row) => {
            return (
                <div>
                    <button className="btn btn-warning ml-2 btn-sm btn10px btn10px" type="button" onClick={() => editIntegrattionLayout(row.id)}>
                        <i className="fa fa-pencil-alt"></i>
                    </button>
                    <button className="btn btn-danger ml-2 btn-sm btn10px btn10px" type="button" onClick={() => deleteIntegrattionLayout(row.id)}>
                        <i className="fa fa-trash"></i>
                    </button>
                </div>
            )
        }
    }]
    
    useEffect(() => {
        async function loadIntegrattionLayouts() {
            try {
                const response = await api.get('/integrattion_layouts')
                
                setIntegrattionLayouts(response.data)
            } catch (error) {
                console.log(error)
            }
        }

        loadIntegrattionLayouts()
    }, [])

    let integrattionLayoutsListData = []
    integrattionLayouts.map( fieldsLayout => (
        integrattionLayoutsListData.push({
            id: fieldsLayout._id,
            system: fieldsLayout.system,
            fileType: fieldsLayout.fileType,
            lenghtHeader: fieldsLayout.header.length,
            lenghtFields: fieldsLayout.fields.length
        })
    ) )

    return (
        <main className="content card container-fluid pt-3">
            <div className="container-fluid d-flex text-center justify-content-center header-table border py-1">Layouts</div>
            <BootstrapTable 
                keyField='id' 
                data={ integrattionLayoutsListData } 
                columns={ columns } 
                filter={ filterFactory() }    
                bordered
                hover
            />
        </main>
      )
     
}

export default IntegrattionLayoutsList;