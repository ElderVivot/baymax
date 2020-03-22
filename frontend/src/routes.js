import React from 'react'
import {Switch, Route, Redirect} from 'react-router-dom'

import Home from './components/Home'
import IntegrattionLayoutsList from './pages/IntegrattionLayoutsNewEdit/IntegrattionLayoutsList'

export default function Routes() {
    return (
        <Switch>
            <Route exact path='/' component={Home} />
            <Route path="/integrattion_layouts" component={IntegrattionLayoutsList} />
            <Redirect from='*' to='/' />
        </Switch>
    )
}