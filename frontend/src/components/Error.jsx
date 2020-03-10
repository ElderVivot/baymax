import React from "react"
import './Error.css'

const Error = ({ touched, message }) => {
  if (message) {
    return <div className="form-message invalid offset-1">{message}</div>;
  }
  return <div className="form-message valid"></div>;
}

export default Error