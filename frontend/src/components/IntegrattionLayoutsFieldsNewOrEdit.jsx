import React, {useState} from 'react'
import Select from 'react-select'
import Creatable from 'react-select/creatable'
import { Modal, Button, Col, Form } from "react-bootstrap"

class ClassUtil{
    static createAnObjetOfCount(numberInicial=1, numberFinal=100){
        let obj = [{value: -1, label: "Posição Variável"}]
        while(numberInicial <= numberFinal){
            obj.push({
                value: numberInicial, label: `${numberInicial}`
            })
            numberInicial++
            console.log(numberInicial)
        }
        return obj
    }
}

const objetOfCount = ClassUtil.createAnObjetOfCount()

function IntegrattionLayoutsFieldsNewOrEdit( { idx, fieldsFile, handleFieldFileChange } ){

    const [show, setShow] = useState(false);
      
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

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
    
    const positionInFileOptions = objetOfCount
    
    return (
        <>
            <Button variant="primary" onClick={handleShow}>
                New
            </Button>
        
            <Modal show={show} onHide={handleClose} dialogClassName="width-modal" >
                <Modal.Body>
                    <Form.Row>
                        <Form.Label as="label" htmlFor="field" className="col-form-label">Campo:</Form.Label>
                        <Col lg={4}>
                            <Select 
                                id={`nameField-${idx}`}
                                options={fieldsOptions}
                                onChange={ (event, action, attributes={nameClass: 'nameField', idx, eventType: 'selected'}) => handleFieldFileChange(event, attributes) }
                                className="selected"
                                isSearchable="true"
                                placeholder="Selecione"
                                value={fieldsFile[idx].nameField}
                            />
                        </Col>
                    </Form.Row>
                    <Form.Row className="mt-2">
                        <Form.Label as="label" htmlFor="field" className="col-form-label">Posição que se encontra no Arquivo:</Form.Label>
                        <Col lg={3}>
                            <Creatable 
                                id={`positionInFile-${idx}`}
                                options={positionInFileOptions}
                                onChange={ (event, action, attributes={nameClass: 'positionInFile', idx, eventType: 'selected'}) => handleFieldFileChange(event, attributes) }
                                className="selected"
                                isSearchable="true"
                                autoFocus={true}
                                placeholder="Selecione"
                                value={fieldsFile[idx].positionInFile}
                                formatCreateLabel={(string) => `Criar ${string}`}
                            />
                        </Col>
                    </Form.Row>

                    <Form.Row className="mt-2">
                        <Form.Label as="label" htmlFor="field" className="col-form-label">Nome da Coluna Correspondente:</Form.Label>
                        <Col lg={6}>
                            <Form.Control
                                type="text"
                                placeholder="Informe o nome da coluna que identifica este campo"
                                value={fieldsFile[idx].nameColumn}
                                onChange={ (event, action, attributes={nameClass: 'nameColumn', idx}) => handleFieldFileChange(event, attributes) }
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