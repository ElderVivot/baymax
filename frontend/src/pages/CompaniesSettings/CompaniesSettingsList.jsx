import './styles.css'
import React, { useEffect, useState, useRef } from 'react'
import { HotTable } from '@handsontable/react'
const { setIntervalAsync } = require('set-interval-async/dynamic')

const columns = require('./SettingsColumns')
const UnionIntegrattionAndExtractsCompanies = require('../../services/UnionIntegrattionAndExtractsCompanies')
const PostCompaniesSettings = require('../../services/PostCompaniesSettings')

const CompaniesSettingsList = ( {history} ) => {
    const hotTableComponent = useRef(null)
    const [actionUpdate, setActionUpdate] = useState(false)
    const [dataSheet, setDataSheet] = useState([])
    
    useEffect(() => {
        async function loadCompaniesSettings() {
            try {
                const unionIntegrattionAndExtractsCompanies = new UnionIntegrattionAndExtractsCompanies()

                const dataIntegrattionAndExtractsCompanies = await unionIntegrattionAndExtractsCompanies.process()
                setDataSheet(dataIntegrattionAndExtractsCompanies)
                
                setActionUpdate(true)
            } catch (error) {
                console.log(error)
            }
        }

        loadCompaniesSettings()
    }, [actionUpdate])

    setIntervalAsync( async () => {
        try {
            const postCompaniesSettings = new PostCompaniesSettings()
            await postCompaniesSettings.process(hotTableComponent.current.hotInstance.getData())
        } catch (error) {
            console.log(error)
        }
    }, 200000)
    
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
                    colWidths: [70, 270, 130, 70, 170, 130, 90, 100, 100, 60, 180, 180, 80, 200, 300, 170, 100, 180, 100, 150, 150, 150, 150, 70, 70, 70, 70, 70, 100, 60, 350],
                    // autoColumnSize: {syncLimit: 300},
                    autoRowSize: {syncLimit: 5},
                    autoWrapCol: true,
                    autoWrapRow: true,
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
                        columns: [2, 6, 7, 8, 19, 20, 24, 25, 30],
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