import './styles.css'
import React, { useEffect, useState, useRef } from 'react'
import api from '../../services/api'
import { HotTable } from '@handsontable/react'

const columns = require('./settingColumns').columns
const util = require('../../utils/util')

function statEmp(status){
    if(status === 'A'){
        return 'Ativa'
    } else if(status === 'I'){
        return 'Inativa'
    } else if(status === 'M'){
        return 'Sem Movimento'
    } else if(status === 'C'){
        return 'Em Constituição'
    } else if(status === 'B'){
        return 'Em Processo Baixa'
    } else {
        return status
    }
}

function isCompanyBranch(tins_emp, cgce_emp){
    try {
        if(tins_emp !== 1){
            return 'Não'
        } else {
            if(cgce_emp.substring(8, 12) === '0001'){
                return 'Não'
            } else {
                return 'Sim'
            }
        }
    } catch (error) {
        return 'Não'
    }
}

function formatCgceEmp(tins_emp, cgce_emp){
    try {
        if(tins_emp === 1){
            return `${cgce_emp.substring(0, 2)}.${cgce_emp.substring(2, 5)}.${cgce_emp.substring(5, 8)}/${cgce_emp.substring(8, 12)}-${cgce_emp.substring(12)}`
        } else if(tins_emp === 2){
            return `${cgce_emp.substring(0, 3)}.${cgce_emp.substring(3, 6)}.${cgce_emp.substring(6, 9)}-${cgce_emp.substring(9)}`
        } else {
            return cgce_emp
        }
    } catch (error) {
        return 'Não'
    }
}

const CompaniesSettingsList = ( {history} ) => {
    const hotTableComponent = useRef(null)
    const [actionUpdate, setActionUpdate] = useState(false)
    const [integrattionLayouts, setIntegrattionLayouts ] = useState([])
    const [integrattionCompanies, setIntegrattionCompanies ] = useState([])
    const [extractCompanies, setExtractCompanies ] = useState([])

    function returnDataLayoutAccountPaid(codi_emp){
        let accountPaid = {}
        try {
            accountPaid = integrattionCompanies.filter( companie => companie.codi_emp === codi_emp )[0].accountPaid
        } catch (error) {
            accountPaid = {}
        }
        
        let system = ''
        try {
            for(let layoutAccountPaid of accountPaid.layouts){
                system += `${integrattionLayouts.filter( layout => layout._id === layoutAccountPaid.idLayout )[0].system}, `
            }
            system = system.substring(0, system.length - 2)
            return {system}
        } catch (error) {
            return {system: ''}
        }
    }

    useEffect(() => {
        async function loadCompaniesSettings() {
            try {
                const responseLayouts = await api.get(`/integrattion_layouts`)
                if(responseLayouts.statusText === "OK"){
                    setIntegrattionLayouts(responseLayouts.data)
                }

                const responseIntegrattionCompanies = await api.get(`/integrattion_companies`)
                if(responseIntegrattionCompanies.statusText === "OK"){
                    setIntegrattionCompanies(responseIntegrattionCompanies.data)
                }

                const responseExtractCompanies = await api.get(`/extract_companies`)
                if(responseExtractCompanies.statusText === "OK"){
                    setExtractCompanies(responseExtractCompanies.data)                    
                    setActionUpdate(true)                 
                }
            } catch (error) {
                console.log(error)
            }
        }

        loadCompaniesSettings()
    }, [actionUpdate])

    let dataSheet = []
    extractCompanies.map( companie => (
        dataSheet.push({
            codi_emp: companie.codi_emp,
            nome_emp: companie.nome_emp,
            cgce_emp: formatCgceEmp(companie.tins_emp, companie.cgce_emp),
            stat_emp: statEmp(companie.stat_emp),
            dcad_emp: util.transformToDate(companie.dcad_emp),
            dina_emp: util.transformToDate(companie.dina_emp),
            telefone_emp: `${companie.dddf_emp}-${companie.fone_emp}`,
            email_emp: companie.email_emp,
            isCompanyBranch: isCompanyBranch(companie.tins_emp, companie.cgce_emp),
            layoutsAccountPaid: returnDataLayoutAccountPaid(companie.codi_emp).system
        })
    ))
    
    const handleChanges = () => {
        try {
            console.log(hotTableComponent.current.hotInstance.getData())
        } catch (error) {
            return
        }
    }

    return (
        <main className="content card container-fluid pt-3">
            <HotTable
                ref={hotTableComponent}
                settings={{
                    data: dataSheet,
                    rowHeaders: true,
                    colHeaders: true,
                    // width: '100%',
                    // height: 1000,
                    colWidths: [70, 300, 130, 70, 100, 100, 60, 180, 180, 80, 200, 300, 200, 100, 180, 100],
                    // autoColumnSize: {syncLimit: 300},
                    autoRowSize: {syncLimit: 300},
                    // rowHeights: 23,
                    // columnHeaderHeight: 23,
                    rowHeaderWidth: 30,
                    afterChange: () => handleChanges(),
                    columns: columns,
                    dropdownMenu: true,
                    filters: true,
                    multiColumnSorting: true,
                    className: "htCenter htMiddle",
                    manualColumnResize: true,
                    manualRowResize: true,
                    // contextMenu: contextMenu,
                    // contextMenu: true,
                    hiddenColumns: {
                        // columns: [2, 3],
                        indicators: true
                    },
                    // fixedColumnsLeft: 2,
                    manualColumnFreeze: true,
                    licenseKey: 'non-commercial-and-evaluation',
                }}
            />
        </main>
      )
     
}

export default CompaniesSettingsList