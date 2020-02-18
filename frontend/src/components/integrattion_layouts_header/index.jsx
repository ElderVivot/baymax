import React, { useState } from 'react'

let teste = []

export default function IntegrattionLayoutsHeader(props){

    const [fieldsHeader, setFieldsHeader] = useState(props.header)

    const updateFieldHeader = (key, event) => {
        fieldsHeader[key] = {
            nameField: event
        }

        setFieldsHeader([...fieldsHeader])
    }

    teste = fieldsHeader

    return (
        <>
            <table className="col-12">
                <tbody>
                    {
                        fieldsHeader.map( (field, key) => (
                            <tr className="form-group row" key={key}>
                                <td className="col">
                                    <input 
                                        id={key}
                                        type="text" 
                                        className="form-control" 
                                        placeholder="Informe um valor que compõe o cabaçalho "
                                        value={field.nameField}
                                        onChange={(event) => updateFieldHeader(key, event.target.value)}
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
                        ))
                    }
                </tbody>
            </table>
        </>
    )
}