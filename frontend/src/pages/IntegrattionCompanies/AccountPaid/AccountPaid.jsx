import React from 'react'
import Select from 'react-select'
import Creatable from 'react-select/creatable'
import { Col, Form } from "react-bootstrap"
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreRounded from '@material-ui/icons/ExpandMoreRounded';

function AccountPaid( { values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched, defaultValues } ){

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

    function fieldLayouts(){
        if(values.accountPaid.length > 0){
            return (
                <div className="form row pb-0 mt-1">
                    <div className="table ml-3 table-bordered div-table-2px">
                        <ExpansionPanel className="mt-1 ml-4 mr-3 mb-2">
                            <ExpansionPanelSummary
                                expandIcon={<ExpandMoreRounded />}
                                aria-controls="panel1a-content"
                                id="panel1a-header"
                            >
                                <Typography className="font-weight-600">Layouts:</Typography>
                            </ExpansionPanelSummary>
                            <ExpansionPanelDetails className="pl-2 pt-0 pb-2">
                                
                            </ExpansionPanelDetails>
                        </ExpansionPanel>
                    </div>
                </div>         
            )
        }

    }
    
    return (
        <>
            <div className="form row mt-3">
                <label className="col-form-label font-weight-600">Configurar Layouts de Contas Pagas:</label>                
                <button className="btn btn-primary btn-sm btn10px ml-3 mt-1" type="button" style={{height:25}}
                    onClick={() => {
                        setFieldValue("accountPaid", [...values.accountPaid, defaultValues.accountPaid])
                    } } >
                    <i className="fa fa-check"></i>
                </button>
            </div>
            {fieldLayouts()}
               
        </>

    )
    
}

export default AccountPaid