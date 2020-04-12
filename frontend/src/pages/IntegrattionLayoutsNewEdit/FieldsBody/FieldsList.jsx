import React from 'react'

import IntegrattionLayoutsFieldsNewOrEdit from './FieldsNewOrEdit'

function IntegrattionLayoutsFieldsList( { values, errors, touched, handleChange, handleBlur, setFieldValue, setFieldTouched, defaultValues, initialValues } ){

    return (
        <>
            <div className="form row mt-2">
                <label className="col-form-label font-weight-600">Configuração dos Campos do Layout:</label>                                
            </div>

            <div className="form row">
                <table className="table ml-3 table-striped table-bordered table-hover">
                    <thead>
                        <tr className="d-flex justify-content-center text-center">
                            <th className="col-4 fields-of-table align-center">Campo</th>
                            <th className="col-1 fields-of-table align-center">Posição Inicial</th>
                            <th className="col-1 fields-of-table align-center">Posição Final</th>
                            <th className="col-3 fields-of-table align-center">Nome Coluna</th>
                            <th className="col-1 fields-of-table align-center">Formato Data</th>
                            <th className="col-2 fields-of-table align-center">
                                <div className="font-weight-600">Ações</div>
                                <button className="btn btn-success btn-sm btn10px ml-3" type="button" style={{height:25}}
                                    onClick={() => {
                                        setFieldValue("fields", [...values.fields, defaultValues.fields[0]])
                                    } }>
                                    <i className="fa fa-plus"></i>
                                </button>
                            </th>
                        </tr>
                    </thead>
                    <tbody>{
                        values.fields.map( (field, idx) => (
                            <tr key={`values.fields[${idx}]`} className="d-flex justify-content-center text-center">
                                <td className="col-4 align-center">{values.fields[idx].nameField.label}</td>
                                <td className="col-1 align-center">{values.fields[idx].positionInFile}</td>
                                <td className="col-1 align-center">{values.fields[idx].positionInFileEnd}</td>
                                <td className="col-3 align-center">{values.fields[idx].nameColumn}</td>
                                <td className="col-1 align-center">{values.fields[idx].formatDate}</td>
                                <td className="col-2 align-center">
                                    <div>
                                        < IntegrattionLayoutsFieldsNewOrEdit
                                            key={`values.fields[${idx}]`}
                                            idx={idx}
                                            values={values}
                                            errors={errors}
                                            touched={touched}
                                            handleChange={handleChange}
                                            handleBlur={handleBlur}
                                            setFieldValue={setFieldValue}
                                            setFieldTouched={setFieldTouched}
                                            initialValues={initialValues}
                                        />

                                        <button className="btn btn-danger ml-2 btn-sm btn10px" type="button"
                                            onClick={() => {
                                                const updatedFieldsFile = [...values.fields]
                                                updatedFieldsFile.splice(idx, 1)
                                                setFieldValue("fields", updatedFieldsFile)
                                            }}>
                                            <i className="fa fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))
                    }
                    </tbody>
                </table>
            </div>

            
        </>
    )
}

export default IntegrattionLayoutsFieldsList