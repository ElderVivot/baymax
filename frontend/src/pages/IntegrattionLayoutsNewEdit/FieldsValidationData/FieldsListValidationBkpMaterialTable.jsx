import React from 'react'
import MaterialTabel from 'material-table'
import IconEdit from '../../../components/IconEdit'
import IconDelete from '../../../components/IconDelete'
import IconNew from '../../../components/IconNew'

const fieldsOptions = [
    { value: 'paymentDate', label: 'Data de Pagamento'},
    { value: 'document', label: 'NF ou Documento'},
    { value: 'cgceProvider', label: 'CNPJ Fornedor'},
    { value: 'nameProvider', label: 'Nome Fornecedor'},
    { value: 'bank', label: 'Banco/Caixa'},
    { value: 'account', label: 'Conta Corrente'},
    { value: 'amountPaid', label: 'Valor Pago'},
    { value: 'amountOriginal', label: 'Valor Original'},
    { value: 'amountInterest', label: 'Valor Juros'},
    { value: 'amountFine', label: 'Valor Multa'},
    { value: 'amountDiscount', label: 'Valor Desconto'},
    { value: 'amountDevolution', label: 'Valor Devolução'},
    { value: 'dueDate', label: 'Data de Vencimento'},
    { value: 'issueDate', label: 'Data de Emissão'},
    { value: 'historic', label: 'Histórico'},
    { value: 'category', label: 'Categoria'},
    { value: 'accountPlan', label: 'Plano de Contas'},
    { value: 'parcelNumber', label: 'Número da Parcela'},
    { value: 'companyBranch', label: 'Filial/Empresa'},
    { value: 'typeMoviment', label: 'Tipo Movimento'},
]

function IntegrattionLayoutsFieldsListValidation( { fieldsValidation, setFieldValue } ){

    const columns = [{        
        field: 'nameField',
        title: 'Campo',
        cellStyle: {
            width: 'calc(40%)'
        }        
    }, {
        field: 'typeValidation',
        title: 'Tipo Validação',
        cellStyle: {
            width: 'calc(20%)'
        }
    }, {
        field: 'valueValidation',
        title: 'Valor Validação',
        cellStyle: {
            width: 'calc(15%)'
        }
    }, {
        field: 'nextValidationOrAnd',
        title: 'E/OU',
        cellStyle: {
            width: 'calc(15%)'
        }
    }, {
        // este objeto vazio exsit pra largura do header ficar correta
    }]

    return (
        <MaterialTabel
            options={{
                filtering: false,
                actionsColumnIndex: -1,
                paging: false,
                showTitle: false,
                search: false,
                toolbar: true
            }}
            localization={{
                header: {
                    actions: 'Ações'
                },
                body: {
                    emptyDataSourceMessage: 'Não há dados para serem exibidos'
                }
            }}
            data={ fieldsValidation } 
            columns={ columns }
            // actions={[
            //     _ => ({
            //         icon: IconEdit,
            //         tooltip: 'Editar',
            //         iconProps: {
            //             classes: {label: 'teste'}
            //         },
            //         onClick: (event, rowData) => console.log('Editar')
            //     }),
            //     _ => ({
            //         icon: IconDelete,
            //         tooltip: 'Deletar',
            //         onClick: (event, rowData) => console.log('Deletar')
            //     })
            // ]}
            editable={{
                onRowAdd: newData =>
                    new Promise((resolve, reject) => {
                    setTimeout(() => {
                        {
                        const data = fieldsValidation
                        data.push(newData);
                        setFieldValue( 'fieldsValidation', data)
                        }
                        resolve()
                    }, 1000)
                }),
                onRowUpdate: (newData, oldData) =>                 
                  new Promise((resolve, reject) => {
                    setTimeout(() => {
                      {
                        const data = fieldsValidation
                        const index = data.indexOf(oldData)
                        data[index] = newData
                        setFieldValue( 'fieldsValidation', data)
                      }
                      resolve()
                    }, 1000)
                  }),
                onRowDelete: oldData =>
                  new Promise((resolve, reject) => {
                    setTimeout(() => {
                      {
                        let data = fieldsValidation
                        const index = data.indexOf(oldData);
                        data.splice(index, 1);
                        setFieldValue( 'fieldsValidation', data)
                      }
                      resolve()
                    }, 1000)
                  }),
              }}
        />
    )
    
}

export default IntegrattionLayoutsFieldsListValidation