import './styles.css'
import React, { useEffect, useState, useRef } from 'react'
import api from '../../services/api'
import { HotTable } from '@handsontable/react'

const columns = require('./SettingsColumns').columns
const util = require('../../utils/util')
const settingsCompanies = require('../../utils/settingsCompanies')

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

                hotTableComponent.current.hotInstance.getPlugin('filters').addHook('teste', () => console.log('teste'))
                console.log(hotTableComponent.current.hotInstance.getPlugin('filters'))
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
            cgce_emp: settingsCompanies.formatCgceEmp(companie.tins_emp, companie.cgce_emp),
            stat_emp: settingsCompanies.statEmp(companie.stat_emp),
            regime_emp: settingsCompanies.regimeEmp(companie.regime_emp),
            regime_caixa_emp: settingsCompanies.regimeCaixaEmp(companie.regime_caixa_emp),
            dcad_emp: util.transformToDate(companie.dcad_emp),
            dina_emp: util.transformToDate(companie.dina_emp),
            telefone_emp: `${companie.dddf_emp}-${companie.fone_emp}`,
            email_emp: companie.email_emp,
            isCompanyBranch: settingsCompanies.isCompanyBranch(companie.tins_emp, companie.cgce_emp),
            layoutsAccountPaid: returnDataLayoutAccountPaid(companie.codi_emp).system,
            nome_municipio_emp: companie.nome_municipio_emp,
            esta_emp: companie.esta_emp,
            ramo_emp: companie.ramo_emp
        })
    ))
    
    const handleChanges = () => {
        try {
            console.log('')
            // console.log(hotTableComponent)
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
                    colWidths: [70, 270, 130, 70, 170, 130, 90, 100, 100, 60, 180, 180, 80, 200, 300, 170, 100, 180, 100, 150, 150, 150, 150, 70, 70, 70, 70, 70, 100, 60, 350],
                    // autoColumnSize: {syncLimit: 300},
                    autoRowSize: {syncLimit: 300},
                    rowHeights: 23,
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
                        columns: [2, 6, 7, 8, 19, 20, 24, 25],
                        indicators: true
                    },
                    fixedColumnsLeft: 2,
                    manualColumnFreeze: true,
                    licenseKey: 'non-commercial-and-evaluation',
                }}
            />
        </main>
      )
     
}

export default CompaniesSettingsList