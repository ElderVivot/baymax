import React from 'react'

function IntegrattionLayoutsFieldsList( { idx, fieldsFile, handleFieldFileChange } ){
    
    return (
        <>
            <tr className="d-flex">
                <td className="col-4">{fieldsFile[idx].nameField.label}</td>
                <td className="col-1">{fieldsFile[idx].positionInFile.label}</td>
                <td className="col-1">{fieldsFile[idx].positionInFileEnd.label}</td>
                <td className="col-3">{fieldsFile[idx].nameColumn}</td>
                <td className="col-1">{fieldsFile[idx].formatDate.label}</td>
            </tr>
        </>
    );
}

export default IntegrattionLayoutsFieldsList