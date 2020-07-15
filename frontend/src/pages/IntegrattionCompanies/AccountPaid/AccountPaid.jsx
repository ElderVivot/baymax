import React, { useEffect, useState } from 'react'
import Select from 'react-select'
import { Col, Form } from "react-bootstrap"
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreRounded from '@material-ui/icons/ExpandMoreRounded';
import FieldsValidation from './FieldsValidateIfThisCompanie'
import BanksCorrelation from './BanksAndAccountCorrelation'

const { api } = require('../../../services/api')

function AccountPaid( { values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched, defaultValues } ){
    const [integrattionLayouts, setIntegrattionLayouts ] = useState([])
    
    useEffect(() => {
        async function loadLayouts() {
            try {
                const response = await api.get(`/integrattion_layouts`)

                if(response.statusText === "OK"){
                    setIntegrattionLayouts(response.data)                    
                }
            } catch (error) {
                console.log(error)
            }
        }
        loadLayouts()
    }, [])

    let layoutsOptions = []
    integrattionLayouts.map(layout => layoutsOptions.push({
        value: `${layout['_id']}`, label: `${layout['system']}`
    }))

    function validateField(vector){
        try {
            if(vector.length === 2){
                return errors.accountPaid[vector[0]][vector[1]] ? "has-error" : null
            }
            if(vector.length === 3){
                return errors.accountPaid[vector[0]][vector[1]][vector[2]] ? "has-error" : null
            }
            if(vector.length === 4){
                return errors.accountPaid[vector[0]][vector[1]][vector[2]][vector[3]] ? "has-error" : null
            }
        } catch (error) {
            return null
        }
    }

    function messageError(vector){
        try {
            let message = null
            if(vector.length === 2){
                message = errors.accountPaid[vector[0]][vector[1]]
            }
            if(vector.length === 3){
                message = errors.accountPaid[vector[0]][vector[1]][vector[2]]
            }
            if(vector.length === 4){
                message = errors.accountPaid[vector[0]][vector[1]][vector[2]][vector[3]]
            }

            if(message.indexOf('must be a') >= 0) {
                message = 'Campo obrigatório'
            }
            return message
        } catch (error) {
            return null
        }
    }

    let hasLayouts
    try {
        hasLayouts = values.accountPaid.layouts.length
    } catch (error) {
        hasLayouts = 0
    }

    function ButtonsCheckOrDelete(){
        if(hasLayouts === 0 ){
            return (
                <button className="btn btn-primary btn-sm btn10px ml-3 mt-1" type="button" style={{height:25}}
                    onClick={() => {
                        setFieldValue("accountPaid", {
                            isReliable: true,
                            layouts: [{
                                idLayout: '',
                                bankAndAccountCorrelation: [],
                                validateIfDataIsThisCompanie: []
                            }]
                        })
                    } } >
                    <i className="fa fa-check"></i>
                </button>
            )
        } else {
            return (
                <button className="btn btn-danger btn-sm btn10px ml-3 mt-1" type="button" style={{height:25}}
                    onClick={() => {
                        setFieldValue("accountPaid", {})
                    } } >
                    <i className="fa fa-trash"></i>
                </button>
            )
        }
    }

    function HrBetweenOfLines(idx){
        if(( values.accountPaid.layouts.length - 1 ) !== idx ){
            return (
                <hr className="my-2" />
            )
        }
    }

    function fieldLayouts(){
        
        if(hasLayouts > 0){
            return (
                <div className="form row pb-0 mt-1">
                    <div className="table ml-3 table-bordered div-table-2px container-fluid">
                        <div className="">
                            <label className="col-form-label font-weight-600">Layouts:</label>                
                            <button className="btn btn-success btn-sm btn10px ml-3" type="button" style={{height:25}}
                                onClick={() => {
                                    setFieldValue("accountPaid.layouts", [...values.accountPaid.layouts, {
                                        isReliable: true,
                                        layouts: [{
                                            idLayout: '',
                                            bankAndAccountCorrelation: [],
                                            validateIfDataIsThisCompanie: []
                                        }]
                                    } ])
                                } } >
                                <i className="fa fa-plus"></i>
                            </button>
                        </div>

                        <Form.Row className="mt-2">
                            <Col lg={10}>
                                <Form.Check
                                    className="font-weight-600"
                                    type='checkbox'
                                    id={`accountPaid.isReliable`}
                                    name={`accountPaid.isReliable`}
                                    label={`A informação do banco onde foi feito o "pagamento" que vem dos arquivos financeiros do cliente geralmente estão corretos.`}
                                    custom={true}
                                    value={false}
                                    checked={values.accountPaid.isReliable}
                                    onChange={handleChange(`accountPaid.isReliable`)}
                                />
                            </Col>
                        </Form.Row>

                        <div className="table ml-2 table-bordered mt-2 mb-2">{
                            values.accountPaid.layouts.map( (_, idx ) => (
                                <React.Fragment key={`accountPaid[${idx}].reactfragment`}>
                                    <div key={`accountPaid[${idx}]`} className='mt-1'>
                                        <Form.Row className="my-1 d-flex container col-12" id={`linesOfFile[${idx}]`}> 
                                            <Form.Label as="label" htmlFor="field" className="col-form-label font-weight-600">Nome do Layout:</Form.Label>
                                            <Col lg={5}>
                                                <Form.Group as={Col} className="pl-0 m-0">
                                                    <Select 
                                                        name={`accountPaid.layouts[${idx}].idLayout`}
                                                        options={layoutsOptions}
                                                        className={`selected ${validateField(['layouts', idx, 'idLayout'])}`}
                                                        isSearchable={true}
                                                        placeholder="Selecione"
                                                        value={layoutsOptions.filter(option => option.value === values.accountPaid.layouts[idx].idLayout)[0]}
                                                        onChange={selectedOption => handleChange(`accountPaid.layouts[${idx}].idLayout`)(selectedOption.value)}
                                                        onBlur={() => setFieldTouched(`accountPaid.layouts[${idx}].idLayout`, true)}
                                                    />
                                                    <Form.Control.Feedback type="invalid">{messageError(['layouts', idx, 'idLayout'])}</Form.Control.Feedback>
                                                </Form.Group>
                                            </Col>

                                            <Col lg={1}>
                                                <button className="btn btn-danger btn-sm btn10px ml-3 mt-1" type="button" style={{height:25}}
                                                    onClick={() => {
                                                        const update = [...values.accountPaid.layouts]
                                                        update.splice(idx, 1)
                                                        setFieldValue(`accountPaid.layouts`, update)
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
                                                <Typography className="font-weight-600">Opções Avançadas:</Typography>
                                            </ExpansionPanelSummary>
                                            <ExpansionPanelDetails className="pl-2 pt-0 pb-2">

                                                < BanksCorrelation
                                                    values={values}
                                                    errors={errors}
                                                    touched={touched}
                                                    handleChange={handleChange}
                                                    handleBlur={handleBlur}
                                                    setFieldValue={setFieldValue}
                                                    setFieldTouched={setFieldTouched}
                                                    defaultValues={defaultValues}
                                                    idxAccountPaid={idx}
                                                />
                                                
                                                <hr className="form row my-2 ml-1" />

                                                < FieldsValidation
                                                    values={values}
                                                    errors={errors}
                                                    touched={touched}
                                                    handleChange={handleChange}
                                                    handleBlur={handleBlur}
                                                    setFieldValue={setFieldValue}
                                                    setFieldTouched={setFieldTouched}
                                                    defaultValues={defaultValues}
                                                    idxAccountPaid={idx}
                                                    integrattionLayouts={integrattionLayouts}
                                                />

                                            </ExpansionPanelDetails>
                                        </ExpansionPanel>
                                    </div>
                                    {HrBetweenOfLines(idx)}
                                </React.Fragment>
                            ))
                        }</div>
                    </div>
                </div>         
            )
        }

    }
    
    return (
        <>
            <div className="form row mt-3">
                <label className="col-form-label font-weight-600">Configurar Layouts de Contas Pagas:</label>                
                {ButtonsCheckOrDelete()}
            </div>
            {fieldLayouts()}
               
        </>

    )
    
}

export default AccountPaid