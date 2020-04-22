import React from 'react'
import {Switch, Route, Redirect} from 'react-router-dom'

import Home from './components/Home'
import IntegrattionLayoutsList from './pages/IntegrattionLayouts/IntegrattionLayoutsList'
import IntegrattionLayouts from './pages/IntegrattionLayouts/IntegrattionLayouts'
import IntegrattionCompanies from './pages/IntegrattionCompanies/IntegrattionCompanies'
import IntegrattionCompaniesList from './pages/IntegrattionCompanies/IntegrattionCompaniesList'
import CompaniesSettings from './pages/CompaniesSettings/CompaniesSettingsList'

export default function Routes() {
    return (
        <Switch>
            <Route exact path='/' component={Home} />
            <Route exact path="/integrattion_layouts_list" component={IntegrattionLayoutsList} />
            <Route exact path="/integrattion_companies_list" component={IntegrattionCompaniesList} />
            <Route path="/companies_settings" component={CompaniesSettings} />
            <Route path="/integrattion_layouts" component={IntegrattionLayouts} />
            <Route path="/integrattion_companies" component={IntegrattionCompanies} />
            <Redirect from='*' to='/' />
        </Switch>
    )
}