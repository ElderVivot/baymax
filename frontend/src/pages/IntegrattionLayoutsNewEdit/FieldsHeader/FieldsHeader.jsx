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

    const addField = () => {
        setFieldValue("header", [...fieldsHeader, { nameColumn: "" }])
    }
    
    const deleteField = () => {
        const updatedFieldsHeader = [...fieldsHeader]
        updatedFieldsHeader.splice(idx, 1)
        setFieldValue("header", updatedFieldsHeader)
    }

    function ButtonAdd(){
        return (
            <button className="btn btn-success" type="button" 
                onClick={addField}>
                <i className="fa fa-plus"></i>
            </button>
        )
    }

    function ButtonDelete(isDisabled=false){
        if(isDisabled === true){
            return( 
                <button className="btn btn-danger ml-2" type="button" 
                    onClick={deleteField} disabled>
                    <i className="fa fa-trash"></i>
                </button>
            )
        } else {
            return( 
                <button className="btn btn-danger ml-2" type="button" 
                    onClick={deleteField}>
                    <i className="fa fa-trash"></i>
                </button>
            )
        }
    }

    function Buttons(){
        if (fieldsHeader.length === idx+1) {
            if(fieldsHeader.length === 1 && idx === 0){
                return (
                    <div>
                        {ButtonAdd()}
                        {ButtonDelete(true)}
                    </div>
                )
            } else {
                return (
                    <div>
                        {ButtonAdd()}
                        {ButtonDelete()}
                    </div>
                )
            }
        } else {
            return (
                <div className="col-2">
                    {ButtonDelete()}
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