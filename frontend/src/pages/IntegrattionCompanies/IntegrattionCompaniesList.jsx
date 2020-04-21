import '../styles.css'
import React, { useEffect, useState } from 'react'
import api from '../../services/api'
import MaterialTabel from 'material-table'
import IconEdit from '../../components/IconEdit'
import IconDelete from '../../components/IconDelete'
import IconNew from '../../components/IconNew'
// import IconDownload from '../../components/IconDownload'

const IntegrattionCompaniesList = ( {history} ) => {
    const [integrattionCompanies, setIntegrattionCompanies ] = useState([])
    const [actionDelete, setActionDelete] = useState(false)

    const editIntegrattionCompanie = (id) => {
        history.push(`/integrattion_companies/${id}`)
    }

    const addIntegrattionCompanie = () => {
        history.push('/integrattion_companies')
    }

    const deleteIntegrattionCompanie = async (id) => {
        const wishDelete = window.confirm("Tem certeza que deseja deletar este layout?")
        if(wishDelete === true){
            try {
                const response = await api.delete(`/integrattion_companies/${id}`)

                if(response.statusText === "OK"){
                    setActionDelete(true)
                } else {
                    console.log(response)                  
                }
            } catch (error) {
                console.log(error)                
            }
        }
        history.push('/integrattion_companies_list')
    }

    const columns = [{        
        field: 'codi_emp',
        title: 'Código',
        cellStyle: {
            width: 'calc(10%)'
        }        
    }, {
        field: 'nome_emp',
        title: 'Nome Empresa',
        cellStyle: {
            width: 'calc(30%)'
        }
    }, {
        field: 'cgce_emp',
        title: 'CNPJ',
        cellStyle: {
            width: 'calc(15%)'
        }
    }, {
        field: 'accountPaid',
        title: 'Layouts Contas Pagas',
        cellStyle: {
            width: 'calc(40%)'
        }
    }, {
        // este objeto vazio exsit pra largura do header ficar correta
    }]
    
    useEffect(() => {
        async function loadIntegrattionCompanies() {
            try {
                const response = await api.get('/integrattion_companies')
                
                setIntegrattionCompanies(response.data)
            } catch (error) {
                console.log(error)
            }
        }

        loadIntegrattionCompanies()
    }, [actionDelete])

    let integrattionCompaniesListData = []
    integrattionCompanies.map( fieldsCompanie => (
        integrattionCompaniesListData.push({
            id: fieldsCompanie._id,
            codi_emp: fieldsCompanie.codi_emp,
            nome_emp: '',
            cgce_emp: '',
            accountPaid: ''
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
                data={ integrattionCompaniesListData } 
                columns={ columns } 
                title="Empresas X Layouts"
                actions={[
                    {
                        icon: IconNew,
                        tooltip: 'Adicionar',
                        isFreeAction: true,
                        onClick: () => addIntegrattionCompanie()
                    },
                    _ => ({
                        icon: IconEdit,
                        tooltip: 'Editar',
                        iconProps: {
                            classes: {label: 'teste'}
                        },
                        onClick: (event, rowData) => editIntegrattionCompanie(rowData.id)
                    }),
                    _ => ({
                        icon: IconDelete,
                        tooltip: 'Deletar',
                        onClick: (event, rowData) => deleteIntegrattionCompanie(rowData.id)
                    })
                ]}
            />
        </main>
      )
     
}

export default IntegrattionCompaniesList;