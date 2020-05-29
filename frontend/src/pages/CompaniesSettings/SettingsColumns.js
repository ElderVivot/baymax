const columns = [
    {   data: 'codi_emp',
        title: 'Código',
        type: 'numeric',
        filter: true,
        readOnly: true
    }, { data: 'nome_emp',
        title: 'Nome Empresa',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'cgce_emp',
        title: 'CNPJ Empresa',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'stat_emp',
        title: 'Status',
        type: 'text',
        filter: true,
        readOnly: true,
        // filters: {
        //     conditions: [['eq', 'Ativa']],
        //     operation: 'disjunction'
        // }
    }, { data: 'groupCompanie',
        title: 'Grupo',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'regime_emp',
        title: 'Regime',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'regime_caixa_emp',
        title: 'Reg. Caixa?',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'dcad_emp',
        title: 'Cliente Desde',
        type: 'date',
        filter: true,
        dateFormat: 'DD/MM/YYYY',
        correctFormat: true,
        readOnly: true
    }, { data: 'dina_emp',
        title: 'Inativo',
        type: 'date',
        filter: true,
        dateFormat: 'DD/MM/YYYY',
        correctFormat: true,
        readOnly: true
    }, { data: 'isCompanyBranch',
        title: 'Filial?',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'statusAccountPaid',
        title: 'Status Integração',
        type: 'dropdown',
        filter: true,
        source: ['Pendente', 'Analisando', 'Enviado Email', 'Não tem Financeiro', 'Não é possível Realizar', 'Cliente não vai Enviar Dados', 'Explicar pro Contábil', 'Concluída - ERP', 'Concluída - Excel', 'Concluída - Comp. Pagto', 'Concluída - Modelo Antigo', 'Feito em Outro Sistema', 'Mov. Pequena - Ñ Compensa', 'Feito no Honorários', 'Empresa Inativa', 'É Filial', 'Sem Movimento']
    }, { data: 'responsibleFinancialClient',
        title: 'Com quem Falar no Cliente?',
        type: 'text',
        filter: true,
        wordWrap: true
    }, { data: 'telefoneAccountPaid',
        title: 'Telefone',
        type: 'text',
        filter: true
    }, { data: 'emailAccountPaid',
        title: 'Email',
        type: 'text',
        filter: true
    }, { data: 'obsAccountPaid',
        title: 'Observações',
        type: 'text',
        filter: true
    }, { data: 'layoutsAccountPaid',
        title: 'Layouts Contas Pagas',
        type: 'text',
        filter: true
    }, { data: 'dateAccountPaid',
        title: 'Integração',
        type: 'date',
        filter: true,
        dateFormat: 'DD/MM/YYYY',
        correctFormat: true
    }, { data: 'analystReceivedTraining',
        title: 'Quem Recebeu Treinamento?',
        type: 'text',
        filter: true
    }, { data: 'dateReceivedTraining',
        title: 'Explicação',
        type: 'date',
        filter: true,
        dateFormat: 'DD/MM/YYYY',
        correctFormat: true
    }, { data: 'fiscalTeam',
        title: 'Equipe Fiscal',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'fiscalResponsible',
        title: 'Responsável Fiscal',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'accountingTeam',
        title: 'Equipe Contábil',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'accountingResponsible',
        title: 'Responsável Contábil',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'qtdEntryNotes',
        title: 'NF Ent.',
        type: 'numeric',
        filter: true,
        readOnly: true
    }, { data: 'qtdOutputNotes',
        title: 'NF Sai.',
        type: 'numeric',
        filter: true,
        readOnly: true
    }, { data: 'qtdServiceNotes',
        title: 'NF Ser.',
        type: 'numeric',
        filter: true,
        readOnly: true
    }, { data: 'qtdLancManual',
        title: 'Lan. Man.',
        type: 'numeric',
        filter: true,
        readOnly: true
    }, { data: 'qtdLancImported',
        title: 'Lan. Imp.',
        type: 'numeric',
        filter: true,
        readOnly: true
    }, { data: 'nome_municipio_emp',
        title: 'Cidade',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'esta_emp',
        title: 'UF',
        type: 'text',
        filter: true,
        readOnly: true
    }, { data: 'ramo_emp',
        title: 'Ramo',
        type: 'text',
        filter: true,
        readOnly: true
    }
]

module.exports = columns