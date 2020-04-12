import React from "react"

const Error = ({ error }) => {
  if (error) {
    return <div className="invalid-feedback">{error}</div>;
  }
}

export default Error