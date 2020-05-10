import './styles.css'
import React, { useEffect, useState, useRef } from 'react'
import { HotTable } from '@handsontable/react'
import 'handsontable/languages/pt-BR'
// const { setIntervalAsync } = require('set-interval-async/dynamic')

const columns = require('./SettingsColumns')
const SettingsCompaniesSettings = require('../../services/SettingsCompaniesSettings')
const PostCompaniesSettings = require('../../services/PostCompaniesSettings')

const CompaniesSettingsList = ( {history} ) => {
    const hotTableComponent = useRef(null)
    const [dataSheet, setDataSheet] = useState([])
    
    useEffect(() => {
        async function loadCompaniesSettings() {
            try {
                const settingsCompaniesSettings = new SettingsCompaniesSettings()

                const dataSettingsCompaniesSettings = await settingsCompaniesSettings.process()
                setDataSheet(dataSettingsCompaniesSettings)
            } catch (error) {
                console.log(error)
            }
        }

        loadCompaniesSettings()
    }, [])

    // setIntervalAsync( async () => {
    //     try {
    //         const postCompaniesSettings = new PostCompaniesSettings()
    //         await postCompaniesSettings.process(hotTableComponent.current.hotInstance.getData())
    //     } catch (error) {
    //         console.log(error)
    //     }
    // }, 200000)
    
    async function handleChanges(changes){
        try {
            for(let [row] of changes) {
                const dataRow = hotTableComponent.current.hotInstance.getDataAtRow(row)
                const postCompaniesSettings = new PostCompaniesSettings(dataRow)
                await postCompaniesSettings.postData()
            }
        } catch (error) {
            return
        }
    }

    function handleAfterLoadData(initialLoad) {
        try {
            const filtersPlugin = hotTableComponent.current.hotInstance.getPlugin('filters')
            console.log(filtersPlugin)
            
            filtersPlugin.addCondition(3, 'by_value', [['Ativa']]);
            filtersPlugin.filter();

            filtersPlugin.addCondition(0, 'by_value', [[1]]);
            filtersPlugin.filter();
        } catch (error) {
            return
        }
    }

    return (
        <main className="content card container-fluid pt-3">
            <HotTable
                ref={hotTableComponent}
                language={'pt-BR'}
                settings={{
                    data: dataSheet,
                    rowHeaders: true,
                    colHeaders: true,
                    width: '100vw',
                    // height: 1000,
                    colWidths: [70, 270, 130, 70, 170, 130, 90, 100, 100, 60, 180, 180, 80, 200, 300, 170, 100, 180, 100, 150, 150, 150, 150, 70, 70, 70, 70, 70, 100, 60, 350],
                    // autoColumnSize: {syncLimit: 300},
                    autoRowSize: true,
                    autoWrapCol: true,
                    autoWrapRow: true,
                    // rowHeights: 23,
                    // columnHeaderHeight: 23,
                    rowHeaderWidth: 30,
                    afterLoadData: (initialLoad) => handleAfterLoadData(initialLoad),
                    // afterLoadData: (initialLoad) => console.log(initialLoad),
                    afterInit: () => console.log('teste 2'),
                    afterChange: (changes) => handleChanges(changes),
                    columns: columns,
                    dropdownMenu: true,
                    filters: true,
                    multiColumnSorting: true,
                    className: "htCenter htMiddle",
                    manualColumnResize: true,
                    manualRowResize: true,
                    contextMenu: true,
                    hiddenColumns: {
                        columns: [2, 6, 7, 8, 19, 20, 24, 25, 30],
                        indicators: true
                    },
                    // fixedColumnsLeft: 2,
                    manualColumnFreeze: true,
                    licenseKey: 'non-commercial-and-evaluation'
                }}
            />
        </main>
      )
}

export default CompaniesSettingsList