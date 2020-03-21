import 'bootstrap/dist/css/bootstrap.min.css'
import '@fortawesome/fontawesome-free/css/all.css'
import React from 'react';
import './App.css';

import Logo from './components/Logo'
import Header from './components/Header'
import Footer from './components/Footer'
import Routes from './routes'

function App() {
  return (
    <div className="app">

      <Logo />
      <Header />
      <Routes />
      <Footer />
      
    </div>
  );
}

export default App;
