import '../styles.css'
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
        title: 'CNPJ'
    }]
    
    useEffect(() => {
        async function loadCompaniesSettings() {
            try {
                // const response = await api.get('/integrattion_companies')

                const responseCompanies = await api.get(`/extract_companies`)

                if(responseCompanies.statusText === "OK"){
                    setCompanies(responseCompanies.data)
                }
                
                // setIntegrattionCompanies(response.data)
            } catch (error) {
                console.log(error)
            }
        }

        loadCompaniesSettings()
    }, [])

    // function returnDataEmp(codi_emp){
    //     return companies.filter( companie => companie.codi_emp === codi_emp )[0]
    // }

    // const rows = [
    //     { id: 0, title: "Task 1", complete: 20 },
    //     { id: 1, title: "Task 2", complete: 40 },
    //     { id: 2, title: "Task 3", complete: 60 }
    //   ];
    
    return (
        <main className="content card container-fluid pt-3">
            {console.log(companies)}
            <ReactDataGrid
                rowGetter={ i => companies[i] } 
                columns={ columns } 
                rowsCount={3}
                minHeight={150}
            />
        </main>
      )
     
}

export default CompaniesSettingsList;