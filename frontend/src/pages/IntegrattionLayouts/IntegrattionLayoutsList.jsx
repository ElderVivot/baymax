import '../styles.css'
import React, { useEffect, useState } from 'react'
import api from '../../services/api'
import MaterialTabel from 'material-table'
import IconEdit from '../../components/IconEdit'
import IconDelete from '../../components/IconDelete'
import IconNew from '../../components/IconNew'
// import IconDownload from '../../components/IconDownload'

const IntegrattionLayoutsList = ( {history} ) => {
    const [integrattionLayouts, setIntegrattionLayouts ] = useState([])
    const [actionDelete, setActionDelete] = useState(false)

    const editIntegrattionLayout = (id) => {
        history.push(`/integrattion_layouts/${id}`)
    }

    const addIntegrattionLayout = () => {
        history.push('/integrattion_layouts')
    }

    const deleteIntegrattionLayout = async (id) => {
        const wishDelete = window.confirm("Tem certeza que deseja deletar este layout?")
        if(wishDelete === true){
            try {
                const response = await api.delete(`/integrattion_layouts/${id}`)

                if(response.statusText === "OK"){
                    setActionDelete(true)
                } else {
                    console.log(response)                  
                }
            } catch (error) {
                console.log(error)                
            }
        }
        history.push('/integrattion_layouts_list')
    }

    const columns = [{        
        field: 'system',
        title: 'Sistema',
        cellStyle: {
            width: 'calc(40%)'
        }        
    }, {
        field: 'fileType',
        title: 'Tipo Arquivo',
        cellStyle: {
            width: 'calc(20%)'
        }
    }, {
        field: 'lenghtHeader',
        title: 'Qtd Campos Cabeçalho',
        cellStyle: {
            width: 'calc(15%)'
        }
    }, {
        field: 'lenghtFields',
        title: 'Qtd Campos do Arquivo',
        cellStyle: {
            width: 'calc(15%)'
        }
    }, {
        // este objeto vazio exsit pra largura do header ficar correta
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
    }, [actionDelete])

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
            <MaterialTabel
                options={{
                    filtering: true,
                    grouping: true, 
                    actionsColumnIndex: -1,
                    exportButton: true,
                    paging: false
                }}
                localization={{
                    header: {
                        actions: 'Ações'
                    },
                    grouping: {
                        placeholder: 'Arraste um campo aqui para agrupar'
                    },
                    toolbar: {
                        exportTitle: "Exportar",
                        exportName: "Exportar para CSV",
                        searchTooltip: "Pesquisar",
                        searchPlaceholder: "Pesquisar",
                        nRowsSelected: '{0} linha(s) selecionada'
                    },
                    body: {
                        emptyDataSourceMessage: 'Não há dados para serem exibidos',
                        filterRow: {
                            filterTooltip: 'Filtro'
                        }
                    },
                    pagination: {
                        labelRowsSelect: "linhas",
                        labelDisplayedRows: '{from}-{to} de {count}'
                    }
                }}
                data={ integrattionLayoutsListData } 
                columns={ columns } 
                title="Layouts"
                actions={[
                    {
                        icon: IconNew,
                        tooltip: 'Adicionar',
                        isFreeAction: true,
                        onClick: () => addIntegrattionLayout()
                    },
                    _ => ({
                        icon: IconEdit,
                        tooltip: 'Editar',
                        iconProps: {
                            classes: {label: 'teste'}
                        },
                        onClick: (event, rowData) => editIntegrattionLayout(rowData.id)
                    }),
                    _ => ({
                        icon: IconDelete,
                        tooltip: 'Deletar',
                        onClick: (event, rowData) => deleteIntegrattionLayout(rowData.id)
                    })
                ]}
            />
        </main>
      )
     
}

export default IntegrattionLayoutsList;