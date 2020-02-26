import React, {useState} from 'react'
import Select from 'react-select'
import Creatable from 'react-select/creatable'
import { Modal, Button, Col, Form } from "react-bootstrap"
import * as Yup from 'yup'
import { Formik } from 'formik'

let initialValues={
    fields: {
        nameField: "",
        positionInFile: "",
        positionInFileEnd: "",
        nameColumn: "",
        formatDate: ""
    }
}

class ClassUtil{
    static createAnObjetOfCount(numberInicial=1, numberFinal=100){
        let obj = [{value: -1, label: "Posição Variável"}]
        while(numberInicial <= numberFinal){
            obj.push({
                value: `${numberInicial}`, label: `${numberInicial}`
            })
            numberInicial++
        }
        return obj
    }
}

const positionInFileOptions = ClassUtil.createAnObjetOfCount()

const fieldsOptions = [
    { value: 'paymentDate', label: 'Data de Pagamento'},
    { value: 'document', label: 'NF ou Documento'},
    { value: 'cgceProvider', label: 'CNPJ Fornedor'},
    { value: 'nameProvider', label: 'Nome Fornecedor'},
    { value: 'bank', label: 'Banco/Caixa'},
    { value: 'amountPaid', label: 'Valor Pago'},
    { value: 'amountOriginal', label: 'Valor Original'},
    { value: 'amountInterest', label: 'Valor Juros'},
    { value: 'amountFine', label: 'Valor Multa'},
    { value: 'amountDiscount', label: 'Valor Desconto'},
    { value: 'dueDate', label: 'Data de Vencimento'},
    { value: 'issueDate', label: 'Data de Emissão'},
    { value: 'historic', label: 'Histórico'},
    { value: 'category', label: 'Categoria'},
    { value: 'accountPlan', label: 'Plano de Conta'},
]

function IntegrattionLayoutsFieldsNewOrEdit( { idx, setFieldValueParent } ){

    const fieldPosition = `fields[${idx}]`

    const [show, setShow] = useState(false)

    const handleClose = () => setShow(false)
    const handleShow = () => setShow(true)

    function handleSave(event, values) {
        event.preventDefault()
        const nameField = values.fields.nameField
        const positionInFile = values.fields.positionInFile
        const nameColumn = values.fields.nameColumn

        setFieldValueParent(`${fieldPosition}.nameField`, nameField)
        setFieldValueParent(`${fieldPosition}.positionInFile`, positionInFile)
        setFieldValueParent(`${fieldPosition}.nameColumn`, nameColumn)

        setShow(false)
    }
    
    return (
        <>
            <Button variant="warning" className="ml-2" 
                onClick={handleShow}>
                <i className="fa fa-pencil-alt"></i>
            </Button>

            <Formik 
                initialValues={initialValues}
            >
                { ({ values, errors, touched, handleChange, handleBlur, setFieldTouched }) => (
                <Modal show={show} dialogClassName="width-modal" >
                    <Modal.Body>
                        <Form.Row>
                            <Form.Label as="label" htmlFor="field" className="col-form-label">Campo:</Form.Label>
                            <Col lg={4}>
                                <Select 
                                    id={`${fieldPosition}.nameField`}
                                    name={`fields.nameField`}
                                    options={fieldsOptions}
                                    className={`selected ${touched.nameField && errors.nameField ? "has-error" : null }`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={fieldsOptions.filter(option => option.value === values.nameField)[0]}
                                    onChange={selectedOption => handleChange(`fields.nameField`)(selectedOption.value)}
                                    onBlur={() => setFieldTouched(`fields.nameField`, true)}
                                />
                            </Col>
                        </Form.Row>
                        <Form.Row className="mt-2">
                            <Form.Label as="label" htmlFor="field" className="col-form-label">Posição que se encontra no Arquivo:</Form.Label>
                            <Col lg={3}>
                                <Creatable 
                                    id={`${fieldPosition}.positionInFile`}
                                    name={`fields.positionInFile`}
                                    options={positionInFileOptions}
                                    className={`selected ${touched.positionInFile && errors.positionInFile ? "has-error" : null }`}
                                    isSearchable={true}
                                    placeholder="Selecione"
                                    value={positionInFileOptions.filter(option => option.value === values.positionInFile)[0]}
                                    onChange={selectedOption => handleChange(`fields.positionInFile`)(selectedOption.value)}
                                    onBlur={() => setFieldTouched(`fields.positionInFile`, true)}
                                    formatCreateLabel={(string) => `Criar ${string}`}
                                />
                            </Col>
                        </Form.Row>

                        <Form.Row className="mt-2">
                            <Form.Label as="label" htmlFor="field" className="col-form-label">Nome da Coluna Correspondente:</Form.Label>
                            <Col lg={6}>
                                <Form.Control
                                    id={`${fieldPosition}.nameColumn`}
                                    name={`fields.nameColumn`}
                                    type="text"
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
                            Close
                        </Button>
                        <Button variant="primary" onClick={(event, _, attributes=values) => handleSave(event, attributes)}>
                            Save Changes
                        </Button>
                    </Modal.Footer>
                </Modal>
                )}
            </Formik>
        </>
    );
}

export default IntegrattionLayoutsFieldsNewOrEdit