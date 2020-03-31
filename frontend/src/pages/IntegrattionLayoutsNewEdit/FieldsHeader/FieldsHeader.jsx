import React from 'react'

function IntegrattionLayoutsHeader({ idx, fieldsHeader, errors, touched, handleChange, handleBlur, setFieldValue }){

    const fieldPosition = `header[${idx}]`
    
    function validateField(nameColumn){
        try {
            return touched.header[idx][nameColumn] && errors.header[idx][nameColumn] ? "has-error" : null
        } catch (error) {
            return null
        }
    }
    
    const deleteField = () => {
        const updatedFieldsHeader = [...fieldsHeader]
        updatedFieldsHeader.splice(idx, 1)
        setFieldValue("header", updatedFieldsHeader)
    }

    function ButtonDelete(isDisabled=false){
        return( 
            <button className="btn btn-danger ml-2 btn-sm btn10px" type="button" 
                onClick={deleteField} disabled={isDisabled}>
                <i className="fa fa-trash"></i>
            </button>
        )
    }

    function Buttons(){
        return (
            <div >
                {ButtonDelete()}
            </div>
        )
    }
    
    return (
        <>
            <tr className="form-group row d-flex mb-0 pb-0 text-center justify-content-center align-items-center">
                <td className="col-11">
                    <div className="input-group">
                        <div className="input-group-prepend">
                            <span className="input-group-text" style={{"color": "black !important"}}>{idx+1}</span>
                        </div>
                        <input 
                            type="text"
                            name={`${fieldPosition}.nameColumn`}
                            id={`${fieldPosition}.nameColumn`}
                            className={`form-control ${validateField("nameColumn") }`}
                            value={fieldsHeader[idx].nameColumn}
                            onChange={handleChange}
                            onBlur={handleBlur}
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