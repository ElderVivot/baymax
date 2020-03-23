import React from 'react'
import {Switch, Route, Redirect} from 'react-router-dom'

import Home from './components/Home'
import IntegrattionLayoutsList from './pages/IntegrattionLayoutsNewEdit/IntegrattionLayoutsList'
import IntegrattionLayouts from './pages/IntegrattionLayoutsNewEdit/IntegrattionLayouts'

export default function Routes() {
    return (
        <Switch>
            <Route exact path='/' component={Home} />
            <Route exact path="/integrattion_layouts_list" component={IntegrattionLayoutsList} />
            <Route path="/integrattion_layouts" component={IntegrattionLayouts} />
            <Redirect from='*' to='/' />
        </Switch>
    )
}