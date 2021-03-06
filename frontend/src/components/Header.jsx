import './Header.css'
import React from 'react'
import { Navbar, Nav, NavDropdown } from 'react-bootstrap'

export default props =>
    <header className="header d-flex align-items-end pl-4 mb-0">
        <Navbar expand="lg pb-1 pl-4">
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link href="/" className="text-settings-header">Home</Nav.Link>
                    <NavDropdown title={ <span className="text-settings-header pl-3">Configurações</span> } id="basic-nav-dropdown">
                        <NavDropdown.Item href="/integrattion_layouts_list" className="text-settings-general">Layouts</NavDropdown.Item>
                        <NavDropdown.Item href="/integrattion_companies_list" className="text-settings-general">Vincular Layouts nas Empresas</NavDropdown.Item>
                        <NavDropdown.Item href="/companies_settings" className="text-settings-general">Empresas Integração</NavDropdown.Item>
                    </NavDropdown>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    </header>

