import React from 'react'
import Select from 'react-select'
import Creatable from 'react-select/creatable'
import { Col, Form } from "react-bootstrap"
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

const typeValidationOptions = [
    { value: 'isEqual', label: 'É igual à'},
    { value: 'isDifferent', label: 'É diferente de'},
    { value: 'isDate', label: 'É uma data'},
    { value: 'isLessThan', label: 'É menor que'},
    { value: 'isLessThanOrEqual', label: 'É menor ou igual à'},
    { value: 'isBiggerThan', label: 'É maior que'},
    { value: 'isBiggerThanOrEqual', label: 'É maior ou igual à'},
    { value: 'contains', label: 'Contém'},
    { value: 'notContains', label: 'Não Contém'}
]

const nextValidationOrAndOptions = [
    { value: 'and', label: 'E'},
    { value: 'or', label: 'OU'}
]

let positionInFileOptions = [...ClassUtil.createAnObjetOfCount()]
let positionInFileEndOptions = [...ClassUtil.createAnObjetOfCount()]

function LinesOfFile( { values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched, setValues } ){

    function validateField(name, idx){
        try {
            return touched.linesOfFile[idx][name] && errors.linesOfFile[idx][name] ? "has-error" : null
        } catch (error) {
            return null
        }
    }

    function ButtonsCheckOrAddOfLine(){
        const objNewLine = { 
            nameOfLine: { value: '', label: '' },
            informationIsOnOneLineBelowTheMain: false,
            validations: [{
                positionInFile: 0,
                positionInFileEnd: 0,
                typeValidation: "",
                valueValidation: "",
                nextValidationOrAnd: "and"
            }]
        }

        if(values.linesOfFile.length === 0 ){
            return (
                <button className="btn btn-primary btn-sm btn10px ml-3 mt-1" type="button" style={{height:25}}
                    onClick={() => {
                        setFieldValue("linesOfFile", [...values.linesOfFile, objNewLine])
                    } } >
                    <i className="fa fa-check"></i>
                </button>
            )
        } else {
            return (
                <button className="btn btn-success btn-sm btn10px ml-3 mt-1" type="button" style={{height:25}}
                    onClick={() => {
                        setFieldValue("linesOfFile", [...values.linesOfFile, objNewLine ])
                    } } >
                    <i className="fa fa-plus"></i>
                </button>
            )
        }
    }

    function HrBetweenOfLines(idx){
        if(( values.linesOfFile.length - 1 ) !== idx ){
            return (
                <hr className="my-2" />
            )
        }
    }

    function fieldValueValidation(idx, idxValidation){
        let disabled = false
        if(values.linesOfFile[idx].validations[idxValidation].typeValidation === "isDate") {
            disabled = true
        }

        return(
            <Col >
                <Form.Control
                    id={`linesOfFile[${idx}].validations[${idxValidation}].valueValidation`}
                    name={`valueValidation`}
                    type="text"
                    className={`selected ${validateField('valueValidation', idx, idxValidation)} text-center`}
                    placeholder="Informe a validação"
                    value={values.linesOfFile[idx].validations[idxValidation].valueValidation}
                    disabled={disabled}
                    onChange={handleChange(`linesOfFile[${idx}].validations[${idxValidation}].valueValidation`)}
                    onBlur={() => setFieldTouched(`linesOfFile[${idx}].validations[${idxValidation}].valueValidation`, true)}
                />
            </Col>
        )
    }

    function fieldPositionInFileEnd(idx, idxValidation){
        let disabled = false
        if(values.fileType !== "txt") {
            disabled = true
        }

        return(
            <Col >
                <Creatable 
                    id={`linesOfFile[${idx}].validations[${idxValidation}].positionInFileEnd`}
                    name={`positionInFileEnd`}
                    options={positionInFileEndOptions}
                    className={`selected ${validateField('positionInFileEnd', idx)} select-center`}
                    isSearchable={true}
                    isDisabled={disabled}
                    placeholder="Selecione"
                    value={positionInFileEndOptions.filter(option => option.value === values.linesOfFile[idx].validations[idxValidation].positionInFileEnd)[0]}
                    onChange={selectedOption => handleChange(`linesOfFile[${idx}].validations[${idxValidation}].positionInFileEnd`)(selectedOption.value)}
                    onBlur={() => setFieldTouched(`linesOfFile[${idx}].validations[${idxValidation}].positionInFileEnd`, true)}
                    formatCreateLabel={(string) => `Criar a opção "${string}"`}
                />
            </Col>
        )
    }

    function handleNameOfLine(event, idx){        
        setFieldValue(`linesOfFile[${idx}].nameOfLine.label`, event.target.value)     
        setFieldValue(`linesOfFile[${idx}].nameOfLine.value`, event.target.value.normalize('NFD').replace(/([\u0300-\u036f]|[^0-9a-zA-Z])/g, '').toLowerCase())
    }
    
    return (
        <>
            <div className="form row mt-4">
                <label className="col-form-label font-weight-600">Os campos deste layout estão distribuídos em várias linhas, ou seja, linhas que armazenam dados diferentes:</label>                
                {ButtonsCheckOrAddOfLine()}
            </div>
            
            <div className="form row pb-0 mt-1">
                <div className="table ml-3 table-bordered div-table-2px">{
                    values.linesOfFile.map( (field, idx) => (
                        <React.Fragment key={`linesOfFile[${idx}].reactfragment`}>
                            <div key={`linesOfFile[${idx}]`}>
                                <Form.Row className="my-1 d-flex container col-12" id={`linesOfFile[${idx}]`}> 
                                    <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Nome da Linha:</Form.Label>
                                    <Col lg={5}>
                                        <Form.Group as={Col} className="pl-0 m-0">
                                            <Form.Control
                                                id={`linesOfFile[${idx}].nameOfLine.label`}
                                                name={`nameOfLine`}
                                                type="text"
                                                className={`selected ${validateField('nameOfLine', idx)}`}
                                                placeholder="Informe o nome que deseja pra linha"
                                                value={values.linesOfFile[idx].nameOfLine.label}
                                                onChange={(event) => handleNameOfLine(event, idx)}
                                                onBlur={() => setFieldTouched(`linesOfFile[${idx}].nameOfLine.label`, true)}
                                            />
                                        </Form.Group>
                                    </Col>

                                    <Col lg={4}>
                                        <Form.Check
                                            className="ml-5 mt-1 font-weight-600"
                                            type='checkbox'
                                            id={`linesOfFile[${idx}].informationIsOnOneLineBelowTheMain`}
                                            label={`Esta linha está abaixo da linha principal`}
                                            custom={true}
                                            value={values.linesOfFile[idx].informationIsOnOneLineBelowTheMain}
                                            onChange={handleChange(`linesOfFile[${idx}].informationIsOnOneLineBelowTheMain`)}
                                        />
                                    </Col>

                                    <Col lg={1}>
                                        <button className="btn btn-danger btn-sm btn10px ml-3 mt-1" type="button" style={{height:25}}
                                            onClick={() => {
                                                const updatedFields = [...values.linesOfFile]
                                                updatedFields.splice(idx, 1)
                                                setFieldValue(`linesOfFile`, updatedFields)
                                            } }
                                        >
                                            <i className="fa fa-trash"></i>
                                        </button> 
                                    </Col>                                      
                                </Form.Row>

                                <ExpansionPanel key={`linesOfFile[${idx}]`} className="mt-1 ml-4 mr-3 mb-2">
                                    <ExpansionPanelSummary
                                        expandIcon={<ExpandMoreRounded />}
                                        aria-controls="panel1a-content"
                                        id="panel1a-header"
                                    >
                                        <Typography className="font-weight-600">Validações pra esta linha ser válida:</Typography>
                                    </ExpansionPanelSummary>
                                    <ExpansionPanelDetails className="pl-2 pt-0 pb-2">
                                        <div className="form row">
                                            <table className="table table-bordered table-hover ml-3 mt-1 mb-0">
                                                <thead>
                                                    <tr className="d-flex justify-content-center text-center">
                                                        <th className="col-2 fields-of-table align-center">Posição Inicial</th>
                                                        <th className="col-2 fields-of-table align-center">Posição Final</th>
                                                        <th className="col-2 fields-of-table align-center">Tipo Validação</th>
                                                        <th className="col-3 fields-of-table align-center">Valor</th>
                                                        <th className="col-2 fields-of-table align-center">E/OU</th>
                                                        <th className="col-1 fields-of-table align-center">
                                                            <div className="font-weight-600">Ações</div>
                                                            <button className="btn btn-success btn-sm btn10px ml-3" type="button" style={{height:25}}
                                                                onClick={() => {
                                                                    setFieldValue(`linesOfFile[${idx}].validations`, [...values.linesOfFile[idx].validations, { 
                                                                        positionInFile: 0,
                                                                        positionInFileEnd: 0,
                                                                        typeValidation: "",
                                                                        valueValidation: "",
                                                                        nextValidationOrAnd: "and"
                                                                    }])
                                                                } } >
                                                                <i className="fa fa-plus"></i>
                                                            </button>        
                                                        </th>
                                                    </tr>
                                                </thead>
                                                <tbody>{
                                                    values.linesOfFile[idx].validations.map( (field, idxValidation) => (
                                                        <tr key={`linesOfFile[${idx}].validations[${idxValidation}]`} className="d-flex justify-content-center text-center">
                                                            <td key={`linesOfFile[${idx}].validations[${idxValidation}].positionInFile`} className="col-2 align-center">
                                                                <Col>
                                                                    <Creatable 
                                                                        id={`linesOfFile[${idx}].validations[${idxValidation}].positionInFile`}
                                                                        name={`positionInFile`}
                                                                        options={positionInFileOptions}
                                                                        className={`selected ${validateField('positionInFile', idx)} select-center`}
                                                                        isSearchable={true}
                                                                        placeholder="Selecione"
                                                                        value={positionInFileOptions.filter(option => option.value === values.linesOfFile[idx].validations[idxValidation].positionInFile)[0]}
                                                                        onChange={selectedOption => handleChange(`linesOfFile[${idx}].validations[${idxValidation}].positionInFile`)(selectedOption.value)}
                                                                        onBlur={() => setFieldTouched(`linesOfFile[${idx}].validations[${idxValidation}].positionInFile`, true)}
                                                                        formatCreateLabel={(string) => `Criar a opção "${string}"`}
                                                                    />
                                                                </Col>
                                                            </td>
                                                            <td key={`linesOfFile[${idx}].validations[${idxValidation}].positionInFileEnd`} className="col-2 align-center">
                                                                {fieldPositionInFileEnd(idx, idxValidation)}
                                                            </td>
                                                            <td key={`linesOfFile[${idx}].validations[${idxValidation}].typeValidation`} className="col-2 align-center">
                                                                <Col>
                                                                    <Select 
                                                                        id={`linesOfFile[${idx}].validations[${idxValidation}].typeValidation`}
                                                                        name={`typeValidation`}
                                                                        options={typeValidationOptions}
                                                                        className={`selected ${validateField('typeValidation', idx)} select-center`}
                                                                        isSearchable={true}
                                                                        placeholder="Selecione"
                                                                        value={typeValidationOptions.filter(option => option.value === values.linesOfFile[idx].validations[idxValidation].typeValidation)[0]}
                                                                        onChange={selectedOption => handleChange(`linesOfFile[${idx}].validations[${idxValidation}].typeValidation`)(selectedOption.value)}
                                                                        onBlur={() => setFieldTouched(`linesOfFile[${idx}].validations[${idxValidation}].typeValidation`, true)}
                                                                    />
                                                                </Col>
                                                            </td>
                                                            <td key={`linesOfFile[${idx}].validations[${idxValidation}].valueValidation`} className="col-3 align-center">
                                                                {fieldValueValidation(idx, idxValidation)}
                                                            </td>
                                                            <td key={`linesOfFile[${idx}].validations[${idxValidation}].nextValidationOrAnd`} className="col-2 align-center">
                                                                <Col>
                                                                    <Select 
                                                                        id={`linesOfFile[${idx}].validations[${idxValidation}].nextValidationOrAnd`}
                                                                        name={`nextValidationOrAnd`}
                                                                        options={nextValidationOrAndOptions}
                                                                        className={`selected ${validateField('nextValidationOrAnd', idx)} select-center`}
                                                                        isSearchable={true}
                                                                        placeholder="Selecione"
                                                                        value={nextValidationOrAndOptions.filter(option => option.value === values.linesOfFile[idx].validations[idxValidation].nextValidationOrAnd)[0]}
                                                                        onChange={selectedOption => handleChange(`linesOfFile[${idx}].validations[${idxValidation}].nextValidationOrAnd`)(selectedOption.value)}
                                                                        onBlur={() => setFieldTouched(`linesOfFile[${idx}].validations[${idxValidation}].nextValidationOrAnd`, true)}
                                                                    />
                                                                </Col>
                                                            </td>
                                                            <td key={`linesOfFile[${idx}].validations[${idxValidation}].button`} className="col-1 align-center">
                                                                <button className="btn btn-danger ml-2 btn-sm btn10px" type="button" 
                                                                    onClick={() => {
                                                                        const updatedFields = [...values.linesOfFile[idx].validations]
                                                                        updatedFields.splice(idxValidation, 1)
                                                                        setFieldValue(`linesOfFile[${idx}].validations`, updatedFields)
                                                                    } }
                                                                >
                                                                    <i className="fa fa-trash"></i>
                                                                </button>
                                                            </td>
                                                        </tr>
                                                    ))
                                                }
                                                </tbody>
                                            </table>
                                        </div>           
                                    </ExpansionPanelDetails>
                                </ExpansionPanel>
                            </div>
                            {HrBetweenOfLines(idx)}
                        </React.Fragment>
                    ))}               
                </div>
            </div>            
        </>

    )
    
}

export default LinesOfFile