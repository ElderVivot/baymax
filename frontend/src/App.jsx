import 'bootstrap/dist/css/bootstrap.min.css'
import '@fortawesome/fontawesome-free/css/all.css'
import React from 'react';
import './App.css';

import Routes from './routes'

function App() {
  return (
    <div className="App">

      <div className="content">
        <Routes />
      </div>
      
    </div>
  );
}

export default App;
