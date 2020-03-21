import React from 'react'
import {BrowserRouter, Switch, Route, Redirect} from 'react-router-dom'

import Home from './components/Home'
import IntegrattionLayouts from './pages/IntegrattionLayoutsNewEdit/IntegrattionLayouts'

export default function Routes() {
    return (
        <BrowserRouter>
            <Switch>
                <Route exact path='/' component={Home} />
                <Route path="/integrattion_layouts" component={IntegrattionLayouts} />
                <Redirect from='*' to='/' />
            </Switch>
        </BrowserRouter>
    )
}