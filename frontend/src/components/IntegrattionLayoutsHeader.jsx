import React from 'react'
import './styles.css'

function IntegrattionLayoutsHeader({ idx, fieldsHeader, handleFieldHeaderChange, addFieldHeader, deleteFieldHeader }){

    const fieldHeaderId = `nameField-${idx}`

    function Buttons(){
        if (fieldsHeader.length === idx+1) {
            return (
                <div>
                    <button className="btn btn-success" type="button" 
                        onClick={addFieldHeader}>
                        <i className="fa fa-plus"></i>
                    </button>
                    <button className="btn btn-danger ml-2" type="button" 
                        onClick={deleteFieldHeader}>
                        <i className="fa fa-trash"></i>
                    </button>
                </div>
            )
        } else {
            return (
                <div className="col-2">
                    <button className="btn btn-danger ml-2" type="button" 
                        onClick={deleteFieldHeader}>
                        <i className="fa fa-trash"></i>
                    </button>
                </div>
                
            )
        }
    }
    
    return (
        <>
            <tr className="form-group row mb-1">
                <td className="col-11">
                    <div className="input-group">
                        <div className="input-group-prepend">
                            <span className="input-group-text">{idx+1}</span>
                        </div>
                        <input 
                            type="text"
                            name={fieldHeaderId}
                            data-idx={idx}
                            id={fieldHeaderId}
                            className="nameField form-control"
                            value={fieldsHeader[idx].nameField}
                            onChange={handleFieldHeaderChange}
                        />
                    </div>
                </td>
                <td>
                    < Buttons />
                </td>
            </tr>
        </>
    )
}

export default IntegrattionLayoutsHeader