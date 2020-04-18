import React, {useState} from 'react'
import Select from 'react-select'
import Creatable from 'react-select/creatable'
import { Modal, Button, Col, Form } from "react-bootstrap"
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreRounded from '@material-ui/icons/ExpandMoreRounded';

class ClassUtil{
    static createAnObjetOfCount(numberInicial=1, numberFinal=100){
        let obj = []
        while(numberInicial <= numberFinal){
            obj.push({
                value: `${numberInicial}`, label: `${numberInicial}`
            })
            numberInicial++
        }
        return obj
    }
}

let fieldsOptions = [
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

function addOptionInCreatable(vector, value, label=undefined){
    // se o value for em branco já retorna o próprio vector, pois não deve adicionar nada
    if(value === "" || value === undefined || value === 0 || value === null){
        return vector
    }

    let valueFormated = ''
    try {
        valueFormated = value.normalize('NFD').replace(/([\u0300-\u036f]|[^0-9a-zA-Z])/g, '').toLowerCase()
    } catch (error) {
        valueFormated = ''
    }
    // se o valor formato não for válido (não conter letra e nada ele já retorna o próprio vetor)
    if(valueFormated === ""){
        return vector
    }

    // adiciona uma nova opção quando é um valor que ainda não existe
    if(vector.filter(option => option.value.toLowerCase() === valueFormated)[0] === undefined){
        vector.push({
            value: `${valueFormated}`, 
            label: label || `${value}`
        })
    }
    return vector
}

const formatDateOptions = [
    { value: 'dd/mm/aaaa', label: 'dd/mm/aaaa'},
    { value: 'aaaa-mm-dd', label: 'aaaa-mm-dd'}
]

let positionInFileOptions = [{value: "0", label: "Posição Variável"}, ...ClassUtil.createAnObjetOfCount()]
let positionInFileEndOptions = ClassUtil.createAnObjetOfCount()
let positionFieldInTheSplitOptions = ClassUtil.createAnObjetOfCount(1, 10)
let positionFieldInTheSplitEndOptions = [{value: "0", label: "Até o Final"}, ...ClassUtil.createAnObjetOfCount(1, 10)]

function FieldsFileEdit( { idx, values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched } ){
    const [initialValues, setInitialValues] = useState({})
    const [show, setShow] = useState(false)

    function handleShow() {
        setShow(true)
        setInitialValues(values.fields[idx]) // quando abrir o modal pega os valores dos fields, pois se o cara clicar em cancelar volta os dados originais antes de abrir o modal
    }

    function validateField(vector){
        try {
            if(vector.length === 2){
                return errors.fields[vector[0]][vector[1]] ? "has-error" : null
            }
            if(vector.length === 3){
                return errors.fields[vector[0]][vector[1]][vector[2]] ? "has-error" : null
            }
        } catch (error) {
            return null
        }
    }

    function messageError(vector){
        try {
            let message = null
            if(vector.length === 2){
                message = errors.fields[vector[0]][vector[1]]
            }
            if(vector.length === 3){
                message = errors.fields[vector[0]][vector[1]][vector[2]]
            }

            if(message.indexOf('must be a `string`') >= 0) {
                message = 'Campo obrigatório'
            } else if(message.indexOf('must be a `number`') >= 0) {
                message = 'Apenas números são válidos.'
            }
            return message
        } catch (error) {
            return null
        }
    }
    
    function ButtonSave(){
        let existErrors = {}
        try {
            existErrors = Object.entries(errors.fields[idx])
        } catch (error) {
            existErrors = {}
        }
        
        const existValues = Object.values(values.fields[idx])
        let hasValuesValid = 0
        existValues.forEach( 
            function(value){
                if( value !== "" && value !== 0 ){
                    hasValuesValid++
                }
            }  
        )

        if(existErrors.length > 0 || hasValuesValid === 0){
            return(
                <Button disabled variant="primary">
                    Salvar
                </Button>
            )
        } else {
            return(
                <Button variant="primary" onClick={ () => setShow(false)}>
                    Salvar
                </Button>
            )
        }
    }

    // volta os valores pros iniciais de quando abriu o modal
    function handleCanceled(event){
        event.preventDefault()

        for(let value in values.fields[idx]){
            values.fields[idx][`${value}`] = initialValues[`${value}`]
            setFieldValue(`fields[${idx}][${value}]`, initialValues[`${value}`])
        }
        setShow(false)
    }

    let lineThatTheDataIsOptions = []
    lineThatTheDataIsOptions.push(...values.linesOfFile.map( value => value["nameOfLine"] ))

    // se o tipo for txt ou pdf não existe "posição variável (valor 0)"
    if(values.fileType === "txt" || values.fileType === "pdf"){
        delete positionInFileOptions[0]
    }
    positionInFileOptions = addOptionInCreatable(positionInFileOptions, values.fields[idx].positionInFile)
    positionInFileEndOptions = addOptionInCreatable(positionInFileEndOptions, values.fields[idx].positionInFileEnd)
    fieldsOptions = addOptionInCreatable(fieldsOptions, values.fields[idx].nameField.value, values.fields[idx].nameField.label)
    positionFieldInTheSplitOptions = addOptionInCreatable(positionFieldInTheSplitOptions, values.fields[idx].positionFieldInTheSplit)
    positionFieldInTheSplitEndOptions = addOptionInCreatable(positionFieldInTheSplitEndOptions, values.fields[idx].positionFieldInTheSplitEnd)

    function fieldFormatDate(){
        let nameLabelOfNameField = ''
        try {
            nameLabelOfNameField = values.fields[idx].nameField.label.toUpperCase().split(' ')
        } catch (error) {
            nameLabelOfNameField = ''
        }

        if(nameLabelOfNameField.indexOf("DATA") >= 0){
            // esta linha faz com que seja obrigado a selecionar este campo quando for uma data
            if(values.fields[idx].formatDate === ""){
                values.fields[idx].formatDate = null
            }
            return (
                <Form.Row className="mt-2">
                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Formato Data:</Form.Label>
                    <Col lg={4}>
                        <Form.Group className="mb-0">
                            <Select 
                                name={`fields[${idx}].formatDate`}
                                options={formatDateOptions}
                                className={`selected ${validateField([idx, 'formatDate'])}`}
                                isSearchable={true}
                                placeholder="Selecione"
                                value={formatDateOptions.filter(option => option.value === values.fields[idx].formatDate)[0]}
                                onChange={selectedOption => handleChange(`fields[${idx}].formatDate`)(selectedOption.value)}
                                onBlur={() => setFieldTouched(`fields[${idx}].formatDate`, true)}
                            />
                            <Form.Control.Feedback type="invalid">{messageError([idx, 'formatDate'])}</Form.Control.Feedback>
                        </Form.Group>
                    </Col>
                </Form.Row>
            )
        } else {
            // zera o valor do campo novamente quando muda de informação
            values.fields[idx].formatDate = ""
        }  
    }

    function fieldPositionInFileEnd(){
        if(values.fileType === "txt" || values.fileType === "pdf"){
            // esta linha faz com que seja obrigado a selecionar este campo
            if(values.fields[idx].positionInFileEnd === 0){
                values.fields[idx].positionInFileEnd = null
            }

            return (
                <Form.Row className="mt-2">
                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Posição final que se encontra no Arquivo:</Form.Label>
                    <Col lg={3}>
                        <Form.Group className="mb-0">
                            <Creatable 
                                name={`fields[${idx}].positionInFileEnd`}
                                options={positionInFileEndOptions}
                                className={`selected ${validateField([idx, 'positionInFileEnd'])}`}
                                isSearchable={true}
                                placeholder="Selecione"
                                value={positionInFileEndOptions.filter(option => option.value === `${values.fields[idx].positionInFileEnd}`)[0]}
                                onChange={selectedOption => handleChange(`fields[${idx}].positionInFileEnd`)(selectedOption.value)}
                                onBlur={() => setFieldTouched(`fields[${idx}].positionInFileEnd`, true)}
                                formatCreateLabel={(string) => `Criar a opção "${string}"`}
                            />
                            <Form.Control.Feedback type="invalid">{messageError([idx, 'positionInFileEnd'])}</Form.Control.Feedback>
                        </Form.Group>
                    </Col>
                </Form.Row>
            )
        } else {
            // zera o valor do campo novamente quando muda de informação
            values.fields[idx].positionInFileEnd = 0
        }        
    }
    
    function fieldNameColumn(){
        if(values.fileType !== "txt" && values.fileType !== "pdf"){
            return (
                <Form.Row className="mt-2">
                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Nome da Coluna Correspondente:</Form.Label>
                    <Col lg={6}>
                        <Form.Control
                            name={`fields[${idx}].nameColumn`}
                            type="text"
                            className={`selected`}
                            placeholder="Informe o nome da coluna que identifica este campo"
                            value={values.fields[idx].nameColumn}
                            onChange={handleChange}
                            onBlur={handleBlur}
                        />
                    </Col>
                </Form.Row>
            )
        }        
    }

    function fieldPositionsSplit(){
        
        if(values.fields[idx].splitField !== ""){
            // esta linha faz com que seja obrigado a selecionar este campo
            if(values.fields[idx].positionFieldInTheSplit === 0){
                values.fields[idx].positionFieldInTheSplit = null
            }

            return (
                <>
                    <Form.Row className="mt-2">
                        <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Posição <u>inicial</u> que se encontra dentro do campo dividido:</Form.Label>
                        <Col lg={3}>
                            <Form.Group className="mb-0">
                                <Creatable 
                                    name={`fields[${idx}].positionFieldInTheSplit`}
                                    options={positionFieldInTheSplitOptions}
                                    className={`selected ${validateField([idx, 'positionFieldInTheSplit'])}`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={positionFieldInTheSplitOptions.filter(option => option.value === `${values.fields[idx].positionFieldInTheSplit}`)[0]}
                                    onChange={selectedOption => handleChange(`fields[${idx}].positionFieldInTheSplit`)(selectedOption.value)}
                                    onBlur={() => setFieldTouched(`fields[${idx}].positionFieldInTheSplit`, true)}
                                    formatCreateLabel={(string) => `Criar a opção "${string}"`}
                                />
                                <Form.Control.Feedback type="invalid">{messageError([idx, 'positionFieldInTheSplit'])}</Form.Control.Feedback>
                            </Form.Group>
                        </Col>
                    </Form.Row>

                    <Form.Row className="mt-2">
                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Posição <u>final</u> que se encontra dentro do campo dividido:</Form.Label>
                    <Col lg={3}>
                        <Form.Group className="mb-0">
                            <Creatable 
                                name={`fields[${idx}].positionFieldInTheSplitEnd`}
                                options={positionFieldInTheSplitEndOptions}
                                className={`selected ${validateField([idx, 'positionFieldInTheSplitEnd'])}`}
                                isSearchable={true}
                                placeholder="Selecione"
                                value={positionFieldInTheSplitEndOptions.filter(option => option.value === `${values.fields[idx].positionFieldInTheSplitEnd}`)[0]}
                                onChange={selectedOption => handleChange(`fields[${idx}].positionFieldInTheSplitEnd`)(selectedOption.value)}
                                onBlur={() => setFieldTouched(`fields[${idx}].positionFieldInTheSplitEnd`, true)}
                                formatCreateLabel={(string) => `Criar a opção "${string}"`}
                            />
                            <Form.Control.Feedback type="invalid">{messageError([idx, 'positionFieldInTheSplitEnd'])}</Form.Control.Feedback>
                        </Form.Group>
                    </Col>
                    </Form.Row>
                </>
            )
        } else {
            values.positionFieldInTheSplit = 0
            values.positionFieldInTheSplitEnd = 0
        }        
    }

    function handleNameField(event, idx){
        setFieldValue(`fields[${idx}].nameField.label`, event.label)
        if( event.__isNew__ !== undefined){
            setFieldValue(`fields[${idx}].nameField.value`, event.value.normalize('NFD').replace(/([\u0300-\u036f]|[^0-9a-zA-Z])/g, '').toLowerCase())
        } else {
            setFieldValue(`fields[${idx}].nameField.value`, event.value)
        }        
    }

    return (
        <>
            <Button size="sm" variant="warning" className="ml-2 btn10px" 
                onClick={handleShow}>
                <i className="fa fa-pencil-alt"></i>
            </Button>

            <Modal show={show} dialogClassName="width-modal" >                
                <Modal.Body>
                    {/* <div className="d-flex">
                        <pre>{JSON.stringify(values.fields[idx], null, 2)}</pre>
                        <pre className="ml-4">{JSON.stringify(errors, null, 2)}</pre>
                    </div> */}
                    <Form.Row>
                        <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Campo:</Form.Label>
                        <Col lg={4}>
                            <Form.Group className="mb-0">
                                <Creatable 
                                    name={`fields[${idx}].nameField`}
                                    options={fieldsOptions}
                                    className={`selected ${validateField([idx, 'nameField', 'label'])}`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={values.fields[idx].nameField}
                                    onChange={(event) => handleNameField(event, idx)}
                                    onBlur={() => setFieldTouched(`fields[${idx}].nameField.label`, true)}
                                    formatCreateLabel={(string) => `Criar a opção "${string}"`}
                                />
                                <Form.Control.Feedback type="invalid">{messageError([idx, 'nameField', 'label'])}</Form.Control.Feedback>
                            </Form.Group>
                        </Col>
                    </Form.Row>

                    {fieldFormatDate()}

                    <Form.Row className="mt-2">
                        <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Posição que se encontra no Arquivo:</Form.Label>
                        <Col lg={3}>
                            <Form.Group className="mb-0">
                                <Creatable 
                                    name={`fields[${idx}].positionInFile`}
                                    options={positionInFileOptions}
                                    className={`selected ${validateField([idx, 'positionInFile'])}`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={positionInFileOptions.filter(option => option.value === `${values.fields[idx].positionInFile}`)[0]}
                                    onChange={selectedOption => handleChange(`fields[${idx}].positionInFile`)(selectedOption.value)}
                                    onBlur={() => setFieldTouched(`fields[${idx}].positionInFile`, true)}
                                    formatCreateLabel={(string) => `Criar a opção "${string}"`}
                                />
                                <Form.Control.Feedback type="invalid">{messageError([idx, 'positionInFile'])}</Form.Control.Feedback>
                            </Form.Group>
                        </Col>
                    </Form.Row>

                    {fieldPositionInFileEnd()}
                    {fieldNameColumn()}

                    <ExpansionPanel className="mt-2 ml-0">
                        <ExpansionPanelSummary
                            expandIcon={<ExpandMoreRounded />}
                            aria-controls="panel1a-content"
                            id="panel1a-header"
                        >
                            <Typography className="font-weight-600">Opções avançadas de configuração:</Typography>
                        </ExpansionPanelSummary>
                        <ExpansionPanelDetails className="pl-2 pt-0 pb-2">
                            <Form.Row className="mt-2">
                                <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Este campo possui o divisor:</Form.Label>
                                <Col lg={4}>
                                    <Form.Control
                                        name={`fields[${idx}].splitField`}
                                        type="text"
                                        className={`selected`}
                                        placeholder="Exemplo '-' ou '/' ..."
                                        value={values.fields[idx].splitField}
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                    />
                                </Col>
                            </Form.Row>

                            {fieldPositionsSplit()}

                            <Form.Row className="mt-2">
                                <Col lg={10}>
                                    <Form.Check
                                        className="font-weight-600"
                                        type='checkbox'
                                        id={`fields[${idx}].groupingField`}
                                        label={`Considerar este campo como "agrupador" pra partidas múltiplas que estão em linhas diferentes!`}
                                        custom={true}
                                        value={values.fields[idx].groupingField}
                                        onChange={handleChange(`fields[${idx}].groupingField`)}
                                    />
                                </Col>
                            </Form.Row>

                            <Form.Row className="mt-2">
                                <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Este campo está na linha:</Form.Label>
                                <Col lg={6}>
                                    <Select 
                                        name={`fields[${idx}].lineThatTheDataIs`}
                                        options={lineThatTheDataIsOptions}
                                        className={`selected`}
                                        isSearchable={true}
                                        placeholder="Selecione uma opção caso este campo esteja em uma linha diferente da principal."
                                        value={lineThatTheDataIsOptions.filter(option => option.value === values.fields[idx].lineThatTheDataIs)[0]}
                                        onChange={selectedOption => handleChange(`fields[${idx}].lineThatTheDataIs`)(selectedOption.value)}
                                        onBlur={() => setFieldTouched(`fields[${idx}].lineThatTheDataIs`, true)}
                                        noOptionsMessage={() => `Não há nenhuma linha cadastrada.`}
                                    />
                                </Col>
                            </Form.Row>
                        </ExpansionPanelDetails>
                    </ExpansionPanel>
                    
                </Modal.Body>

                <Modal.Footer>
                    <Button variant="secondary" onClick={(event) => handleCanceled(event)}>
                        Cancelar
                    </Button>
                    {ButtonSave()}
                </Modal.Footer>
            </Modal>
        </>
    );
}

export default FieldsFileEdit