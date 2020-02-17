import React from 'react'

export default function IntegrattionLayoutsHeader(){

    return (
        <tr className="form-group row">
            <td className="col">
                <input 
                    id="header"
                    type="text" 
                    className="form-control" 
                    placeholder="Informe um valor que compõe o cabaçalho "
                    // value={system}
                    // onChange={event => setSystem(event.target.value)}
                />
            </td>
            <td>
                <button className="btn btn-warning">
                    <i className="fa fa-pencil"></i>
                </button>
                <button className="btn btn-danger ml-2">
                    <i className="fa fa-trash"></i>
                </button>
            </td>

        </tr>
    )
}