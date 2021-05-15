import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages.header import navbar
from pages.covidworld import layout_world
from pages.covidfrance import layout_france
from pages.modelisation import layout_modelisation
from app import app,server


#layout rendu par l'application
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id='page-content')
])

#callback pour mettre à jour les pages
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname=='/covidworld' or pathname=='/':
        return layout_world
    elif pathname=='/covidfrance':
        return layout_france
    elif pathname=='/modelisation':
       return layout_modelisation


if __name__ == '__main__':
    app.run_server(debug=False)