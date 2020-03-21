import './Logo.css'
import logo from '../assets/imgs/baymax.png'
import React from 'react'
import { Link } from 'react-router-dom'

export default props =>
    <aside className="logo d-flex align-items-center justify-content-center">
        <span className="border border-white rounded p-1">
            <Link to="" className="logo">
                <img src={logo} alt="logo" height="55px" width="55px"/>
            </Link>
        </span>
    </aside>