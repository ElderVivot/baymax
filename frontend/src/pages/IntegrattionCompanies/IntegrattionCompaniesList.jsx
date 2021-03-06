import '../styles.css'
import './IntegrattionCompanies.css'
import React, { useEffect, useState } from 'react'
import MaterialTabel from 'material-table'
import IconEdit from '../../components/IconEdit'
import IconDelete from '../../components/IconDelete'
import IconNew from '../../components/IconNew'
// import IconDownload from '../../components/IconDownload'

const { api } = require('../../services/api')

const IntegrattionCompaniesList = ( {history} ) => {
    const [integrattionCompanies, setIntegrattionCompanies ] = useState([])
    const [actionDelete, setActionDelete] = useState(false)
    const [companies, setCompanies ] = useState([])
    const [integrattionLayouts, setIntegrattionLayouts ] = useState([])

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
        title: 'Código'    
    }, {
        field: 'nome_emp',
        title: 'Nome Empresa',
    }, {
        field: 'accountPaid',
        title: 'Layouts Contas Pagas'
    }, 
    // {    field: 'proofOfPayments',
    //     title: 'Comprovantes de Pagamentos'
    // }, {
    //     field: 'extracts',
    //     title: 'Extratos Bancários' }
    ]
    
    useEffect(() => {
        async function loadIntegrattionCompanies() {
            try {
                const response = await api.get('/integrattion_companies')
                const responseCompanies = await api.get(`/extract_companies`)
                const responseLayouts = await api.get(`/integrattion_layouts`)

                if(responseCompanies.statusText === "OK"){
                    setCompanies(responseCompanies.data)
                }

                if(responseLayouts.statusText === "OK"){
                    setIntegrattionLayouts(responseLayouts.data)
                }
                
                setIntegrattionCompanies(response.data)
            } catch (error) {
                console.log(error)
            }
        }

        loadIntegrattionCompanies()
    }, [actionDelete])

    function returnDataEmp(codi_emp){
        try {
            return companies.filter( companie => companie.codi_emp === codi_emp )[0]
        } catch (error) {
            return {nome_emp: ''}
        }
    }

    function returnDataLayoutAccountPaid(accountPaid){
        let system = ''
        try {
            for(let layoutAccountPaid of accountPaid.layouts){
                // console.log(integrattionLayouts)
                system += `${integrattionLayouts.filter( layout => layout._id === layoutAccountPaid.idLayout )[0].system}, `
            }
            system = system.substring(0, system.length - 2)
            return {system}
        } catch (error) {
            return {system: ''}
        }
    }

    let integrattionCompaniesListData = []
    integrattionCompanies.map( fieldsCompanie => {
        const dataEmp = returnDataEmp(fieldsCompanie.codi_emp)
        return integrattionCompaniesListData.push({
            id: fieldsCompanie._id,
            codi_emp: fieldsCompanie.codi_emp,
            nome_emp: dataEmp.nome_emp,
            accountPaid: returnDataLayoutAccountPaid(fieldsCompanie.accountPaid).system
            // proofsOfPayments: '',
            // extracts: ''
        })
    } )

    return (
        <main className="content card container-fluid pt-3">
            <MaterialTabel
                options={{
                    filtering: true,
                    grouping: true, 
                    actionsColumnIndex: -1,
                    exportButton: true,
                    paging: false,
                    doubleHorizontalScroll: true,
                    headerStyle: {
                        zIndex: 10
                    }
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