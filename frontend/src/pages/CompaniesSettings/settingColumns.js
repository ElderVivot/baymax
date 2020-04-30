const columns = [
    {
        data: 'codi_emp',
        title: 'Código',
        type: 'numeric',
        filter: true,
        readOnly: true
    }, {
        data: 'nome_emp',
        title: 'Nome Empresa',
        type: 'text',
        filter: true,
        readOnly: true
    }, {
        data: 'cgce_emp',
        title: 'CNPJ Empresa',
        type: 'text',
        filter: true,
        readOnly: true
    }, {
        data: 'stat_emp',
        title: 'Status',
        type: 'text',
        filter: true,
        readOnly: true
    }, {
        data: 'dcad_emp',
        title: 'Cliente Desde',
        type: 'date',
        filter: true,
        dateFormat: 'DD/MM/YYYY',
        correctFormat: true,
        readOnly: true
    }, {
        data: 'dina_emp',
        title: 'Inativo',
        type: 'date',
        filter: true,
        dateFormat: 'DD/MM/YYYY',
        correctFormat: true,
        readOnly: true
    }, {
        data: 'isCompanyBranch',
        title: 'Filial?',
        type: 'text',
        filter: true,
        readOnly: true
    }, {
        data: 'statusAccountPaid',
        title: 'Status Integração',
        type: 'dropdown',
        filter: true,
        source: ['Pendente', 'Enviado Email', 'Analisando', 'Não é possível Realizar', 'Explicar pro Contábil', 'Concluída', 'Concluída - Modelo Antigo']
    }, {
        data: 'responsibleFinancialClient',
        title: 'Com quem Falar no Cliente?',
        type: 'text',
        filter: true,
        wordWrap: true
    }, {
        data: 'telefone_emp',
        title: 'Telefone',
        type: 'text',
        filter: true
    }, {
        data: 'email_emp',
        title: 'Email',
        type: 'text',
        filter: true
    }, {
        data: 'obsAccountPaid',
        title: 'Observações',
        type: 'text',
        filter: true
    }, {
        data: 'layoutsAccountPaid',
        title: 'Layouts Contas Pagas',
        type: 'text',
        filter: true
    }, {
        data: 'dateAccountPaid',
        title: 'Integração',
        type: 'date',
        filter: true,
        dateFormat: 'DD/MM/YYYY',
        correctFormat: true
    }, {
        data: 'analystReceivedTraining',
        title: 'Quem Recebeu Treinamento?',
        type: 'text',
        filter: true
    }, {
        data: 'dateReceivedTraining',
        title: 'Explicação',
        type: 'date',
        filter: true,
        dateFormat: 'DD/MM/YYYY',
        correctFormat: true
    }
]

module.exports.columns = columns