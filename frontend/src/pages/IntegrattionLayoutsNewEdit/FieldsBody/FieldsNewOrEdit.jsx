import React, {useState} from 'react'
import Select from 'react-select'
import Creatable from 'react-select/creatable'
import { Modal, Button, Col, Form } from "react-bootstrap"
import * as Yup from 'yup'
import { Formik } from 'formik'
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreRounded from '@material-ui/icons/ExpandMoreRounded';

const validationSchema = Yup.object().shape({ 
    nameField: Yup.string().required('Selecione uma opção válida'),
    positionInFile: Yup.number('Valor deve ser um número').required('Campo obrigatório'),
    positionInFileEnd: Yup.number(),
    nameColumn: Yup.string(),
    formatDate: Yup.string("Selecione uma opção válida"),
    splitField: Yup.string(),
    positionFieldInTheSplit: Yup.number(),
    positionFieldInTheSplitEnd: Yup.number()
})

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

function addOptionInCreatable(vector, value, isString=false){
    // o isString serve pra tirar espaços e caracteres especiais que o usuário tiver digitado no Creatable

    // se o value for em branco já retorna o próprio vector, pois não deve adicionar nada
    if(value === ""){
        return vector
    }

    let valueFormated = ''
    if(isString === true){
        valueFormated = value.normalize('NFD').replace(/([\u0300-\u036f]|[^0-9a-zA-Z])/g, '')
    } else {
        valueFormated = value
    }

    // adiciona uma nova opção quando é um valor que ainda não existe
    if(vector.filter(option => option.value === valueFormated)[0] === undefined){
        vector.push({
            value: `${valueFormated}`, label: `${value}`
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

function IntegrattionLayoutsFieldsNewOrEdit( { idx, setFieldValueParent, fieldsOptions, initialValues, fileType, valuesParent } ){
    
    const [show, setShow] = useState(false)

    const fieldPosition = `fields[${idx}]`

    const handleShow = () => setShow(true)
    
    function ButtonSave(values, errors){
        const existErrors = Object.entries(errors)
        const existValues = Object.values(values)
        let hasValuesValid = 0
        existValues.forEach( 
            function(value){
                if( value !== ""){
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
                <Button variant="primary" onClick={(event, _, attributes=values) => handleSave(event, attributes)}>
                    Salvar
                </Button>
            )
        }
    }

    function handleSave(event, values) {
        event.preventDefault()
        const positionInFile = parseInt(values.positionInFile)
        const positionInFileEnd = parseInt(values.positionInFileEnd)
        const positionFieldInTheSplit = parseInt(values.positionFieldInTheSplit)
        const positionFieldInTheSplitEnd = parseInt(values.positionFieldInTheSplitEnd)
        
        setFieldValueParent(`${fieldPosition}.nameField`, values.nameField)
        setFieldValueParent(`${fieldPosition}.positionInFile`, positionInFile)
        setFieldValueParent(`${fieldPosition}.positionInFileEnd`, positionInFileEnd)
        setFieldValueParent(`${fieldPosition}.nameColumn`, values.nameColumn)
        setFieldValueParent(`${fieldPosition}.formatDate`, values.formatDate)
        setFieldValueParent(`${fieldPosition}.splitField`, values.splitField)
        setFieldValueParent(`${fieldPosition}.positionFieldInTheSplit`, positionFieldInTheSplit)
        setFieldValueParent(`${fieldPosition}.positionFieldInTheSplitEnd`, positionFieldInTheSplitEnd)
        setFieldValueParent(`${fieldPosition}.lineThatTheDataIs`, values.lineThatTheDataIs)

        setShow(false)
    }

    // volta os valores pros iniciais de quando abriu o modal
    function handleCanceled(event, values){
        event.preventDefault()

        for(let value in values){
            values[`${value}`] = initialValues[`${value}`]
        }

        setShow(false)
    }

    let lineThatTheDataIsOptions = []
    lineThatTheDataIsOptions.push(...valuesParent.linesOfFile.map( value => value["nameOfLine"] ))
    console.log(lineThatTheDataIsOptions)

    // se o tipo for txt ou pdf não existe "posição variável (valor 0)"
    if(fileType === "txt" || fileType === "pdf"){
        delete positionInFileOptions[0]
    }
    positionInFileOptions = addOptionInCreatable(positionInFileOptions, initialValues.positionInFile)
    positionInFileEndOptions = addOptionInCreatable(positionInFileEndOptions, initialValues.positionInFileEnd)
    fieldsOptions = addOptionInCreatable(fieldsOptions, initialValues.nameField, true)
    positionFieldInTheSplitOptions = addOptionInCreatable(positionFieldInTheSplitOptions, initialValues.positionFieldInTheSplit)
    positionFieldInTheSplitEndOptions = addOptionInCreatable(positionFieldInTheSplitEndOptions, initialValues.positionFieldInTheSplitEnd)

    function fieldFormatDate(values, errors, touched, handleChange, setFieldTouched, fieldsOptions){
        let nameLabelOfNameField = fieldsOptions.filter(option => option.value === values.nameField)[0]
        nameLabelOfNameField = nameLabelOfNameField || { label: "" }
        nameLabelOfNameField = nameLabelOfNameField.label.toUpperCase().split(' ')
        if(nameLabelOfNameField.indexOf("DATA") >= 0){
            // esta linha faz com que seja obrigado a selecionar este campo quando for uma data
            if(values.formatDate === ""){
                values.formatDate = null
            }
            return (
                <Form.Row className="mt-2">
                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Formato Data:</Form.Label>
                    <Col lg={4}>
                        <Select 
                            id={`${fieldPosition}.formatDate`}
                            name={`formatDate`}
                            options={formatDateOptions}
                            className={`selected ${touched.formatDate && errors.formatDate ? "has-error" : null }`}
                            isSearchable={true}
                            placeholder="Selecione"
                            value={formatDateOptions.filter(option => option.value === values.formatDate)[0]}
                            onChange={selectedOption => handleChange(`formatDate`)(selectedOption.value)}
                            onBlur={() => setFieldTouched(`formatDate`, true)}
                        />
                    </Col>
                </Form.Row>
            )
        } else {
            // zera o valor do campo novamente quando muda de informação
            values.formatDate = ""
        }  
    }

    function fieldPositionInFileEnd(values, errors, touched, handleChange, setFieldTouched){
        if(values.positionInFileEnd === null || values.positionInFileEnd === 0){
            values.positionInFileEnd = values.positionInFile
        }
        
        if(fileType === "txt" || fileType === "pdf"){
            return (
                <Form.Row className="mt-2">
                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Posição final que se encontra no Arquivo:</Form.Label>
                    <Col lg={3}>
                        <Creatable 
                            id={`${fieldPosition}.positionInFileEnd`}
                            name={`positionInFileEnd`}
                            options={positionInFileEndOptions}
                            className={`selected ${touched.positionInFileEnd && errors.positionInFileEnd ? "has-error" : null }`}
                            isSearchable={true}
                            placeholder="Selecione"
                            value={positionInFileEndOptions.filter(option => option.value === `${values.positionInFileEnd}`)[0]}
                            onChange={selectedOption => handleChange(`positionInFileEnd`)(selectedOption.value)}
                            onBlur={() => setFieldTouched(`positionInFileEnd`, true)}
                            formatCreateLabel={(string) => `Criar a opção "${string}"`}
                        />
                    </Col>
                </Form.Row>
            )
        } else {
            // zera o valor do campo novamente quando muda de informação
            values.positionInFileEnd = 0
        }        
    }
    
    function fieldNameColumn(values, errors, touched, handleChange, handleBlur){
        if(fileType !== "txt" && fileType !== "pdf"){
            return (
                <Form.Row className="mt-2">
                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Nome da Coluna Correspondente:</Form.Label>
                    <Col lg={6}>
                        <Form.Control
                            id={`${fieldPosition}.nameColumn`}
                            name={`nameColumn`}
                            type="text"
                            className={`selected ${touched.nameColumn && errors.nameColumn ? "has-error" : null }`}
                            placeholder="Informe o nome da coluna que identifica este campo"
                            value={values.nameColumn}
                            onChange={handleChange}
                            onBlur={handleBlur}
                        />
                    </Col>
                </Form.Row>
            )
        } else {
            values.nameColumn = ""
        }        
    }

    function fieldPositionsSplit(values, errors, touched, handleChange, setFieldTouched){
        
        if(values.splitField !== ""){
            return (
                <>
                    <Form.Row className="mt-2">
                        <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Posição <u>inicial</u> que se encontra dentro do campo dividido:</Form.Label>
                        <Col lg={3}>
                            <Creatable 
                                id={`${fieldPosition}.positionFieldInTheSplit`}
                                name={`positionFieldInTheSplit`}
                                options={positionFieldInTheSplitOptions}
                                className={`selected ${touched.positionFieldInTheSplit && errors.positionFieldInTheSplit ? "has-error" : null }`}
                                isSearchable={true}
                                placeholder="Selecione"
                                value={positionFieldInTheSplitOptions.filter(option => option.value === `${values.positionFieldInTheSplit}`)[0]}
                                onChange={selectedOption => handleChange(`positionFieldInTheSplit`)(selectedOption.value)}
                                onBlur={() => setFieldTouched(`positionFieldInTheSplit`, true)}
                                formatCreateLabel={(string) => `Criar a opção "${string}"`}
                            />
                        </Col>
                    </Form.Row>

                    <Form.Row className="mt-2">
                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Posição <u>final</u> que se encontra dentro do campo dividido:</Form.Label>
                    <Col lg={3}>
                        <Creatable 
                            id={`${fieldPosition}.positionFieldInTheSplitEnd`}
                            name={`positionFieldInTheSplitEnd`}
                            options={positionFieldInTheSplitEndOptions}
                            className={`selected ${touched.positionFieldInTheSplitEnd && errors.positionFieldInTheSplitEnd ? "has-error" : null }`}
                            isSearchable={true}
                            placeholder="Selecione"
                            value={positionFieldInTheSplitEndOptions.filter(option => option.value === `${values.positionFieldInTheSplitEnd}`)[0]}
                            onChange={selectedOption => handleChange(`positionFieldInTheSplitEnd`)(selectedOption.value)}
                            onBlur={() => setFieldTouched(`positionFieldInTheSplitEnd`, true)}
                            formatCreateLabel={(string) => `Criar a opção "${string}"`}
                        />
                    </Col>
                    </Form.Row>
                </>
            )
        } else {
            values.positionFieldInTheSplit = 0
            values.positionFieldInTheSplitEnd = 0
        }        
    }

    return (
        <>
            <Button size="sm" variant="warning" className="ml-2 btn10px" 
                onClick={handleShow}>
                <i className="fa fa-pencil-alt"></i>
            </Button>

            <Formik 
                initialValues={initialValues}
                validationSchema={validationSchema}
            >
                { ({ values, errors, touched, handleChange, handleBlur, setFieldTouched }) => (
                <Modal show={show} dialogClassName="width-modal" >
                    <Modal.Body>
                        <Form.Row>
                            <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Campo:</Form.Label>
                            <Col lg={4}>
                                <Creatable 
                                    id={`${fieldPosition}.nameField`}
                                    name={`nameField`}
                                    options={fieldsOptions}
                                    className={`selected ${touched.nameField && errors.nameField ? "has-error" : null }`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={fieldsOptions.filter(option => option.value === values.nameField)[0]}
                                    onChange={selectedOption => handleChange(`nameField`)(selectedOption.value)}
                                    onBlur={() => setFieldTouched(`nameField`, true)}
                                    formatCreateLabel={(string) => `Criar a opção "${string}"`}
                                />
                            </Col>
                        </Form.Row>

                        {fieldFormatDate(values, errors, touched, handleChange, setFieldTouched, fieldsOptions)}

                        <Form.Row className="mt-2">
                            <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Posição que se encontra no Arquivo:</Form.Label>
                            <Col lg={3}>
                                <Creatable 
                                    id={`${fieldPosition}.positionInFile`}
                                    name={`positionInFile`}
                                    options={positionInFileOptions}
                                    className={`selected ${touched.positionInFile && errors.positionInFile ? "has-error" : null }`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={positionInFileOptions.filter(option => option.value === `${values.positionInFile}`)[0]}
                                    onChange={selectedOption => handleChange(`positionInFile`)(selectedOption.value)}
                                    onBlur={() => setFieldTouched(`positionInFile`, true)}
                                    formatCreateLabel={(string) => `Criar a opção "${string}"`}
                                />
                            </Col>
                        </Form.Row>

                        {fieldPositionInFileEnd(values, errors, touched, handleChange, setFieldTouched)}
                        {fieldNameColumn(values, errors, touched, handleChange, handleBlur)}

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
                                            id={`${fieldPosition}.splitField`}
                                            name={`splitField`}
                                            type="text"
                                            className={`selected ${touched.splitField && errors.splitField ? "has-error" : null }`}
                                            placeholder="Exemplo '-' ou '/' ..."
                                            value={values.splitField}
                                            onChange={handleChange}
                                            onBlur={handleBlur}
                                        />
                                    </Col>
                                </Form.Row>

                                {fieldPositionsSplit(values, errors, touched, handleChange, setFieldTouched)}

                                <Form.Row className="mt-2">
                                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Este campo está na linha:</Form.Label>
                                    <Col lg={4}>
                                        <Select 
                                            id={`${fieldPosition}.lineThatTheDataIs`}
                                            name={`lineThatTheDataIs`}
                                            options={lineThatTheDataIsOptions}
                                            className={`selected ${touched.lineThatTheDataIs && errors.lineThatTheDataIs ? "has-error" : null }`}
                                            isSearchable={true}
                                            placeholder="Selecione"
                                            value={lineThatTheDataIsOptions.filter(option => option.value === values.lineThatTheDataIs)[0]}
                                            onChange={selectedOption => handleChange(`lineThatTheDataIs`)(selectedOption.value)}
                                            onBlur={() => setFieldTouched(`lineThatTheDataIs`, true)}
                                        />
                                    </Col>
                                </Form.Row>
                            </ExpansionPanelDetails>
                        </ExpansionPanel>
                        
                    </Modal.Body>

                    <Modal.Footer>
                        <Button variant="secondary" onClick={(event, _, attributes=values) => handleCanceled(event, attributes)}>
                            Cancelar
                        </Button>
                        {ButtonSave(values, errors)}
                    </Modal.Footer>
                </Modal>
                )}
            </Formik>
        </>
    );
}

export default IntegrattionLayoutsFieldsNewOrEdit