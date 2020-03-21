import 'bootstrap/dist/css/bootstrap.min.css'
import '@fortawesome/fontawesome-free/css/all.css'
import React from 'react';
import './App.css';

import Logo from './components/Logo'
import Header from './components/Header'
import Footer from './components/Footer'
import Routes from './routes'
import { BrowserRouter } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Logo />
        <Header />
        <Routes />
        <Footer />      
      </div>
    </BrowserRouter>
  );
}

export default App;
