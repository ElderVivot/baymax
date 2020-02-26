import React, {useState} from 'react'
import Select from 'react-select'
import Creatable from 'react-select/creatable'
import { Modal, Button, Col, Form } from "react-bootstrap"

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

function IntegrattionLayoutsFieldsNewOrEdit( { idx, fieldsFile, errors, touched, handleChange, handleBlur, setFieldTouched } ){

    const fieldPosition = `fields[${idx}]`

    const [show, setShow] = useState(true)

    const handleClose = () => setShow(false)
    const handleShow = () => setShow(true)

    function validateField(nameField){
        try {
            return touched.fields[idx][nameField] && errors.fields[idx][nameField] ? "has-error" : null
        } catch (error) {
            return null
        }
    }
    
    return (
        <>
            <Button variant="warning" className="ml-2" 
                onClick={handleShow}>
                <i className="fa fa-pencil-alt"></i>
            </Button>

            <Modal show={show} dialogClassName="width-modal" >
                <Modal.Body>
                    <Form.Row>
                        <Form.Label as="label" htmlFor="field" className="col-form-label">Campo:</Form.Label>
                        <Col lg={4}>
                            <Select 
                                id={`${fieldPosition}.nameField`}
                                name={`${fieldPosition}.nameField`}
                                options={fieldsOptions}
                                className={`selected ${validateField("nameField")}`}
                                isSearchable={true}
                                placeholder="Selecione"
                                value={fieldsOptions.filter(option => option.value === fieldsFile[idx].nameField)[0]}
                                onChange={selectedOption => handleChange(`${fieldPosition}.nameField`)(selectedOption.value)}
                                onBlur={() => setFieldTouched(`${fieldPosition}.nameField`, true)}
                            />
                        </Col>
                    </Form.Row>
                    <Form.Row className="mt-2">
                        <Form.Label as="label" htmlFor="field" className="col-form-label">Posição que se encontra no Arquivo:</Form.Label>
                        <Col lg={3}>
                            <Creatable 
                                id={`${fieldPosition}.positionInFile`}
                                name={`${fieldPosition}.positionInFile`}
                                options={positionInFileOptions}
                                className={`selected ${validateField("positionInFile")}`}
                                isSearchable={true}
                                placeholder="Selecione"
                                value={positionInFileOptions.filter(option => option.value === fieldsFile[idx].positionInFile)[0]}
                                onChange={selectedOption => handleChange(`${fieldPosition}.positionInFile`)(selectedOption.value)}
                                onBlur={() => setFieldTouched(`${fieldPosition}.positionInFile`, true)}
                                formatCreateLabel={(string) => `Criar ${string}`}
                            />
                        </Col>
                    </Form.Row>

                    <Form.Row className="mt-2">
                        <Form.Label as="label" htmlFor="field" className="col-form-label">Nome da Coluna Correspondente:</Form.Label>
                        <Col lg={6}>
                            <Form.Control
                                id={`${fieldPosition}.nameColumn`}
                                name={`${fieldPosition}.nameColumn`}
                                type="text"
                                placeholder="Informe o nome da coluna que identifica este campo"
                                value={fieldsFile[idx].nameColumn}
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
                    <Button variant="primary" onClick={handleClose}>
                        Save Changes
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}

export default IntegrattionLayoutsFieldsNewOrEdit