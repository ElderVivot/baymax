import React from 'react'
import {BrowserRouter, Switch, Route} from 'react-router-dom'

import IntegrattionLayouts from './components/integrattion_layouts/index'

export default function Routes() {
    return (
        <BrowserRouter>
            <Switch>
                <Route path="/" component={IntegrattionLayouts} />
            </Switch>
        </BrowserRouter>
    )
}