import React from 'react'
import {Switch, Route, Redirect} from 'react-router-dom'

import Home from './components/Home'
import IntegrattionLayoutsList from './pages/IntegrattionLayouts/IntegrattionLayoutsList'
import IntegrattionLayouts from './pages/IntegrattionLayouts/IntegrattionLayouts'
import IntegrattionCompanies from './pages/IntegrattionCompanies/IntegrattionCompanies'

export default function Routes() {
    return (
        <Switch>
            <Route exact path='/' component={Home} />
            <Route exact path="/integrattion_layouts_list" component={IntegrattionLayoutsList} />
            <Route path="/integrattion_layouts" component={IntegrattionLayouts} />
            <Route path="/integrattion_companies" component={IntegrattionCompanies} />
            <Redirect from='*' to='/' />
        </Switch>
    )
}