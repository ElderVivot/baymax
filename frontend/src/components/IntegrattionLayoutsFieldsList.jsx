import React from 'react'

import IntegrattionLayoutsFieldsNewOrEdit from './IntegrattionLayoutsFieldsNewOrEdit'


function IntegrattionLayoutsFieldsList( { idx, fieldsFile, errors, touched, handleChange, handleBlur, setFieldTouched, setFieldValue } ){

    const addField = () => {
        setFieldValue("fields", [...fieldsFile, { 
            nameField: "",
            positionInFile: "",
            positionInFileEnd: "",
            nameColumn: "",
            formatDate: ""
         }])
    }
    
    const deleteField = () => {
        const updatedfieldsFile = [...fieldsFile]
        updatedfieldsFile.splice(idx, 1)
        setFieldValue("fields", updatedfieldsFile)
    }

    const EditField = () => {
        return (
            < IntegrattionLayoutsFieldsNewOrEdit
                key={`fieldFile-${idx}`}
                idx={idx}
                setFieldValueParent={setFieldValue}
            />
        )
    }

    function Buttons(){
        if (fieldsFile.length === idx+1) {
            return (
                <div>
                    <button className="btn btn-success" type="button" 
                        onClick={addField}>
                        <i className="fa fa-plus"></i>
                    </button>
                    {EditField()}
                    <button className="btn btn-danger ml-2" type="button" 
                        onClick={deleteField}>
                        <i className="fa fa-trash"></i>
                    </button>
                </div>
            )
        } else {
            return (
                <div>
                    <button className="btn btn-warning" type="button" 
                        >
                        <i className="fa fa-pencil-alt"></i>
                    </button>
                    <button className="btn btn-danger ml-2" type="button" 
                        onClick={deleteField}>
                        <i className="fa fa-trash"></i>
                    </button>
                </div>
                
            )
        }
    }
    
    return (
        <>
            <tr className="d-flex">
                <td className="col-4">{fieldsFile[idx].nameField}</td>
                <td className="col-1">{fieldsFile[idx].positionInFile}</td>
                <td className="col-1">{fieldsFile[idx].positionInFileEnd}</td>
                <td className="col-3">{fieldsFile[idx].nameColumn}</td>
                <td className="col-1">{fieldsFile[idx].formatDate}</td>
                <td className="col-2">
                    <Buttons />
                </td>
            </tr>
        </>
    )
}

export default IntegrattionLayoutsFieldsList