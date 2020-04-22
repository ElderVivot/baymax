import '../styles.css'
import './IntegrattionCompanies.css'
import React, { useEffect, useState } from 'react'
import api from '../../services/api'
import ReactDataGrid from 'react-data-grid'

const CompaniesSettingsList = ( {history} ) => {
    const [integrattionCompanies, setIntegrattionCompanies ] = useState([])
    const [actionDelete, setActionDelete] = useState(false)
    const [companies, setCompanies ] = useState([])

    // const editIntegrattionCompanie = (id) => {
    //     history.push(`/companies_settings/${id}`)
    // }

    // const addIntegrattionCompanie = () => {
    //     history.push('/companies_settings')
    // }

    // const deleteIntegrattionCompanie = async (id) => {
    //     const wishDelete = window.confirm("Tem certeza que deseja deletar este layout?")
    //     if(wishDelete === true){
    //         try {
    //             const response = await api.delete(`/companies_settings/${id}`)

    //             if(response.statusText === "OK"){
    //                 setActionDelete(true)
    //             } else {
    //                 console.log(response)                  
    //             }
    //         } catch (error) {
    //             console.log(error)                
    //         }
    //     }
    //     history.push('/companies_settings')
    // }

    const columns = [{        
        key: 'codi_emp',
        title: 'Código'    
    }, {
        key: 'nome_emp',
        title: 'Nome Empresa',
    }, {
        key: 'cgce_emp',
        title: 'Layouts Contas Pagas'
    }, 
    ]
    
    useEffect(() => {
        async function loadCompaniesSettings() {
            try {
                const response = await api.get('/integrattion_companies')

                const responseCompanies = await api.get(`/extract_companies`)

                if(responseCompanies.statusText === "OK"){
                    setCompanies(responseCompanies.data)
                }
                
                setIntegrattionCompanies(response.data)
            } catch (error) {
                console.log(error)
            }
        }

        loadCompaniesSettings()
    }, [actionDelete])

    // function returnDataEmp(codi_emp){
    //     return companies.filter( companie => companie.codi_emp === codi_emp )[0]
    // }

    return (
        <main className="content card container-fluid pt-3">
            <ReactDataGrid
                data={ i => companies[i] } 
                columns={ columns } 
            />
        </main>
      )
     
}

export default CompaniesSettingsList;