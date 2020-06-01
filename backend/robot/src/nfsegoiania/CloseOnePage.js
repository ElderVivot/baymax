const CloseOnePage = async(page) => {
    try {
        await page.close()
        console.log('\t[Final-Empresa] - Fechando aba')
        console.log('\t-------------------------------------------------')
    } catch (error) {
        console.log(error)
    }
}

module.exports = CloseOnePage