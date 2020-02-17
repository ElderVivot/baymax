import 'bootstrap/dist/css/bootstrap.min.css'
import '@fortawesome/fontawesome-free/css/all.css'
import React from 'react';
import './App.css';

import Routes from './routes'
// import IntegrattionLayouts from './components/integrattion_layouts/index'

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
