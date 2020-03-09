import React, {useState} from 'react'
import Select from 'react-select'
import Creatable from 'react-select/creatable'
import { Modal, Button, Col, Form } from "react-bootstrap"
import * as Yup from 'yup'
import { Formik } from 'formik'

const validationSchema = Yup.object().shape({ 
    nameField: Yup.string().required('Selecione uma opção válida'),
    positionInFile: Yup.number('Valor deve ser um número').required('Campo obrigatório'),
    positionInFileEnd: Yup.number(),
    nameColumn: Yup.string(),
    formatDate: Yup.string(),
})

class ClassUtil{
    static createAnObjetOfCount(numberInicial=1, numberFinal=100){
        let obj = [{value: "0", label: "Posição Variável"}]
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

let positionInFileOptions = ClassUtil.createAnObjetOfCount()

function IntegrattionLayoutsFieldsNewOrEdit( { idx, setFieldValueParent, fieldsOptions, initialValues } ){

    positionInFileOptions = addOptionInCreatable(positionInFileOptions, initialValues.positionInFile)
    fieldsOptions = addOptionInCreatable(fieldsOptions, initialValues.nameField, true)
    
    const fieldPosition = `fields[${idx}]`

    const [show, setShow] = useState(false)

    const handleClose = () => setShow(false)
    const handleShow = () => setShow(true)

    function handleSave(event, values) {
        event.preventDefault()
        const nameField = values.nameField
        const positionInFile = values.positionInFile
        const nameColumn = values.nameColumn

        setFieldValueParent(`${fieldPosition}.nameField`, nameField)
        setFieldValueParent(`${fieldPosition}.positionInFile`, positionInFile)
        setFieldValueParent(`${fieldPosition}.nameColumn`, nameColumn)

        setShow(false)
    }

    function fieldFormatDate(values, errors, touched, handleChange, setFieldTouched, fieldsOptions){
        let nameLabelOfNameField = fieldsOptions.filter(option => option.value === values.nameField)[0]
        nameLabelOfNameField = nameLabelOfNameField || { label: "" }
        nameLabelOfNameField = nameLabelOfNameField.label.toUpperCase().split(' ')
        if(nameLabelOfNameField.indexOf("DATA") >= 0){
            return (
                <Form.Row className="mt-2">
                    <Form.Label as="label" htmlFor="field" className="col-form-label">Formato Data:</Form.Label>
                    <Col lg={4}>
                        <Select 
                            id={`${fieldPosition}.formatDate`}
                            name={`nameField`}
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
        }
                
    }
    
    return (
        <>
            <Button variant="warning" className="ml-2" 
                onClick={handleShow}>
                <i className="fa fa-pencil-alt"></i>
            </Button>

            <Formik 
                initialValues={initialValues}
                validationSchema={validationSchema}
            >
                { ({ values, errors, touched, handleChange, handleBlur, setFieldTouched }) => (
                <Modal show={show} dialogClassName="width-modal" >
                    <pre>{JSON.stringify(errors, null, 2)}</pre>

                    <Modal.Body>
                        <Form.Row>
                            <Form.Label as="label" htmlFor="field" className="col-form-label">Campo:</Form.Label>
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
                            <Form.Label as="label" htmlFor="field" className="col-form-label">Posição que se encontra no Arquivo:</Form.Label>
                            <Col lg={3}>
                                <Creatable 
                                    id={`${fieldPosition}.positionInFile`}
                                    name={`positionInFile`}
                                    options={positionInFileOptions}
                                    className={`selected ${touched.positionInFile && errors.positionInFile ? "has-error" : null }`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={positionInFileOptions.filter(option => option.value === values.positionInFile)[0]}
                                    onChange={selectedOption => handleChange(`positionInFile`)(selectedOption.value)}
                                    onBlur={() => setFieldTouched(`positionInFile`, true)}
                                    formatCreateLabel={(string) => `Criar a opção "${string}"`}
                                />
                            </Col>
                        </Form.Row>

                        <Form.Row className="mt-2">
                            <Form.Label as="label" htmlFor="field" className="col-form-label">Nome da Coluna Correspondente:</Form.Label>
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
                    </Modal.Body>

                    <Modal.Footer>
                        <Button variant="secondary" onClick={handleClose}>
                            Fechar
                        </Button>
                        <Button variant="primary" onClick={(event, _, attributes=values) => handleSave(event, attributes)}>
                            Salvar
                        </Button>
                    </Modal.Footer>
                </Modal>
                )}
            </Formik>
        </>
    );
}

export default IntegrattionLayoutsFieldsNewOrEdit