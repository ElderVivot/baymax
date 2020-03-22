import './styles.css'
import React, { useEffect, useState } from 'react'
import api from '../../services/api'
import BootstrapTable from 'react-bootstrap-table-next'
import filterFactory, { textFilter, Comparator } from 'react-bootstrap-table2-filter';

const IntegrattionLayoutsList = () => {
    const [integrattionLayouts, setIntegrattionLayouts ] = useState([])

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
        formatter: (cellContent, row) => {
            return (
                <div>
                    <button className="btn btn-success btn-sm" type="button" 
                        >
                        <i className="fa fa-plus"></i>
                    </button>
                    <button className="btn btn-warning ml-2 btn-sm" type="button" 
                        >
                        <i className="fa fa-pencil-alt"></i>
                    </button>
                    <button className="btn btn-danger ml-2 btn-sm" type="button" 
                        >
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