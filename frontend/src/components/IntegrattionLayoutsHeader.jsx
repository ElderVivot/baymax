import React from 'react'

function IntegrattionLayoutsHeader({ idx, fieldsHeader, handleFieldHeaderChange }){

    const fieldHeaderId = `nameField-${idx}`
    
    return (
        <>
            <tr className="form-group row">
                <td className="col">
                    <input 
                        type="text"
                        name={fieldHeaderId}
                        data-idx={idx}
                        id={fieldHeaderId}
                        className="nameField form-control"
                        value={fieldsHeader[idx].nameField}
                        onChange={handleFieldHeaderChange}
                    />
                </td>
                <td>
                    <button className="btn btn-success">
                        <i className="fa fa-plus"></i>
                    </button>
                    <button className="btn btn-danger ml-2">
                        <i className="fa fa-trash"></i>
                    </button>
                </td>
            </tr>
        </>
    )
}

export default IntegrattionLayoutsHeader