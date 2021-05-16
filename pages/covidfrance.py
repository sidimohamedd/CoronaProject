import pandas as pd
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from app import app
from collections import OrderedDict
import dash_bootstrap_components as dbc


####France data
covid = pd.read_csv('https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.csv', sep=",")
covid.columns = ["date",    "granularite",  "maille_code",  "maille_nom",   "cas_confirmes",    "cas_ehpad",    "cas_confirmes_ehpad",  "cas_possibles_ehpad",  "deces",    "deces_ehpad",  "reanimation",  "hospitalises", "nouvelles_hospitalisations",   "nouvelles_reanimations",   "gueris",   "depistes", "source_nom",   "source_url",   "source_archive",   "source_type"]
covid.drop(["source_nom", "maille_code", "cas_ehpad", "granularite",    "source_archive",   "cas_possibles_ehpad", "source_url", "source_type"], axis=1)

dfr = covid[covid.groupby('maille_nom').date.transform('max') == covid['date']]
dfr = dfr[dfr.granularite != "collectivite-outremer"]
dfr = dfr[dfr.granularite != "monde"]
dfr = dfr[dfr.granularite != "departement"]
dfr = dfr[dfr.granularite != "pays"]


region_options = []
for region in dfr.groupby(['maille_nom']).sum().sort_values(ascending=False, by='deces').index:
    region_options.append({'label':str(region),'value':region})

france = html.Div([

                html.Div(
                            [
                                html.Div([ 
                                    html.H6('Last update : ' + str(dfr.date.max()),
                                    style={'text-align': 'center', "margin-bottom": "0px", "width":"100%", 'font-size': '20px', 'font-weight': 'bold','color': 'rgb(49, 69, 106)'}
                                            )
                                        ],className='one-third column',id='title1'),

                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H3(
                                                    "France Data", style={'text-align': 'center', "margin-bottom": "0px", "width":"100%", 'font-size': '45px', 'font-weight': 'bold','color': 'rgb(49, 69, 106)'},
                                                ),
                                                html.H6(
                                                    "Please select region from the dropdown", style={'text-align': 'center', "margin-bottom": "0px", "width":"100%", 'font-size': '20px', 'font-weight': 'bold','color': 'rgb(49, 69, 106)'},
                                                ),
                                            ]
                                        )
                                    ],
                                    className="one-third column",
                                    id="title",
                                ),

                                html.Div(
                                    [
                                        html.A(
                                            html.Button("More Info", id="learn-more-button"),
                                            href="https://www.santepubliquefrance.fr/dossiers/coronavirus-covid-19",
                                        )
                                    ],
                                    className="one-third column",
                                    id="button",
                                ),

                            ],
                            id="header",
                            className="row container-display",
                            style={'columnCount':3, 'text-align':'center'},
                        ),

                html.Div(
                    [dcc.Dropdown(id='country-picker',options=region_options,value=dfr.groupby(['maille_nom']).sum().sort_values(ascending=False, by='reanimation').index[0])],
                    id="cGraphContainer",
                    className="mini_container",
                    style={
                        'background-color': '#ffffff',
                        'padding': '0px',
                        "text-align":"center"
                          }
                        ),


            html.Div(
                        [

                        html.Div(
                            [html.P("Hospitalizations"), html.H1(id="country_conf_text", style={'font-weight': '700'})],
                            id="ToHo",
                            className="four columns",
                            style={
                                'background-color': 'orange',
                                'color': 'white',
                                'font-size': '20px',
                                'text-align': 'center',
                                'flex': '1'
                                }
                        ),
                        html.Div(
                            [html.P("Reanimations"), html.H1(id="country_deat_text", style={'font-weight': '700'})],
                            id="ToRe",
                            className="four columns",
                            style={
                                'background-color': 'purple',
                                'color': 'white',
                                'font-size': '20px',
                                'text-align': 'center',
                                'flex': '1'
                                }
                        ),
                        html.Div(
                            [html.P("Deaths"), html.H1(id="country_reco_text", style={'font-weight': '700'})],
                            id="NeHo",
                            className="four columns",
                            style={
                                'background-color': 'red',
                                'color': 'white',
                                'font-size': '20px',
                                'text-align': 'center',
                                'flex': '1'
                                }
                        ),
                    ],
                    id="country-info-container",
                    className="row container-display",
                    style = {'text-align': 'center', "columnCount":3}
                ),

        html.Div([

            html.Div(
                        [


                            html.Div(
                                [
                                    html.H5(
                                        "Cumulative Deaths", style={'margin-top': '20px',
                                                                    'font-size': '23px',
                                                                    'font-weight': '700',
                                                                    'text-align': 'center',
                                                                    'color': 'rgb(49, 69, 106)',
                                                                    'padding-top': '15px',
                                                                    'margin-bottom': '20px'
                                                                    }
                                    ),
                                ]
                            ),
                            html.Div(
                                [dcc.Graph(id='country_graph_ehpad_deaths',
                                style={

                                    'height': '400px'
                                    })],
                                id="country_recovGraphContainer",
                                className="pretty_container",
                                style={
                                    'background-color': '#1E88E5',
                                    'padding': '5px',
                                    }
                            )
                        ],
                        className="twelve columns",
                    ),



            ],  className= "row",
                style={'text-align': 'center', "width":"100%", "margin-bottom": "0px", "columnCount":1},

            ),

        html.Div([
            html.Div(
                        [


                            html.Div(
                                [
                                    html.H5(
                                        "Hospitalizations", style={'margin-top': '20px',
                                                                    'font-size': '23px',
                                                                    'font-weight': '700',
                                                                    'text-align': 'center',
                                                                    'color': 'rgb(49, 69, 106)',
                                                                    'padding-top': '15px',
                                                                    'margin-bottom': '20px'
                                                                    }
                                    ),
                                ]
                            ),
                            html.Div(
                                [dcc.Graph(id='country_graph_conf',
                                style={

                                    'height': '400px'
                                    })],
                                id="country_confGraphContainer",
                                className="pretty_container",
                                style={
                                    'background-color': '#1E88E5',
                                    'padding': '5px',
                                    }
                            )
                        ],
                        className="six columns",
                    ),
            html.Div(
                        [


                            html.Div(
                                [
                                    html.H5(
                                        "New Hospitalizations", style={'margin-top': '20px',
                                                                    'font-size': '23px',
                                                                    'font-weight': '700',
                                                                    'text-align': 'center',
                                                                    'color': 'rgb(49, 69, 106)',
                                                                    'padding-top': '15px',
                                                                    'margin-bottom': '20px'
                                                                    }
                                    ),
                                ]
                            ),
                            html.Div(
                                [dcc.Graph(id='country_graph_recov',
                                style={

                                    'height': '400px'
                                    })],
                                id="country_recovGraphContainer",
                                className="pretty_container",
                                style={
                                    'background-color': '#1E88E5',
                                    'padding': '5px',
                                    }
                            )
                        ],
                        className="six columns",
                    ),


            ],  className="row",
                style={'text-align': 'center', "width":"100%", "margin-bottom": "0px", "columnCount":1},
            ),


    html.Div([


           html.Div(
                        [

                            html.Div(
                                [
                                    html.H5(
                                        "Reanimations", style={'margin-top': '20px',
                                                                    'font-size': '23px',
                                                                    'font-weight': '700',
                                                                    'text-align': 'center',
                                                                    'color': 'rgb(49, 69, 106)',
                                                                    'padding-top': '15px',
                                                                    'margin-bottom': '20px'
                                                                    }
                                    ),
                                ]
                            ),
                            html.Div(
                                [dcc.Graph(id='country_graph_deat',
                                style={

                                    'height': '400px'
                                    })],
                                id="country_deatGraphContainer",
                                className="pretty_container",
                                style={
                                    'background-color': '#1E88E5',
                                    'padding': '5px',
                                    }
                            )
                        ],
                        className="six columns",
                    ),


            html.Div(
                        [


                            html.Div(
                                [
                                    html.H5(
                                        "New Reanimations", style={'margin-top': '20px',
                                                                    'font-size': '23px',
                                                                    'font-weight': '700',
                                                                    'text-align': 'center',
                                                                    'color': 'rgb(49, 69, 106)',
                                                                    'padding-top': '15px',
                                                                    'margin-bottom': '20px'
                                                                    }
                                    ),
                                ]
                            ),
                            html.Div(
                                [dcc.Graph(id='country_graph_ehpad',
                                style={

                                    'height': '400px'
                                    })],
                                id="country_confGraphContainer",
                                className="pretty_container",
                                style={
                                    'background-color': '#1E88E5',
                                    'padding': '5px',
                                    }
                            )
                        ],
                        className="six columns",
                    ),



            ],  className="row",
                style={'text-align': 'center', "width":"100%", "margin-bottom": "0px", "columnCount":1},
        ),

            html.Div(
                [
                    html.Div(
                        [
                            html.A(
                                html.H5(
                                    "Data sources: OpenCOVID19-fr", style={'margin-top': '20px',
                                                                'font-size': '14px',
                                                                'text-align': 'center',
                                                                'color': 'rgb(49, 69, 106)',
                                                                'padding-top': '15px',
                                                                'margin-bottom': '20px'
                                                                }
                                ), href="https://github.com/opencovid19-fr/data",
                            ),
                            

                        ]),
                ]),

        ])

"""
@app.callback(Output('graph', 'figure'),
              [Input('country-picker', 'value')])
def update_figure(selected_region):
    filtered_df_conf = covid[covid['maille_nom'] == selected_region]
    filtered_df_conf['date'] =pd.to_datetime(filtered_df_conf.date)
    filtered_df_conf = filtered_df_conf.groupby(['date']).sum().sort_values(ascending=True, by='date')

    filtered_df_recov = covid[covid['maille_nom'] == selected_region]
    filtered_df_recov['date'] =pd.to_datetime(filtered_df_recov.date)
    filtered_df_recov = filtered_df_recov.groupby(['date']).sum().sort_values(ascending=True, by='date')

    filtered_df_death = covid[covid['maille_nom'] == selected_region]
    filtered_df_death['date'] =pd.to_datetime(filtered_df_death.date)
    filtered_df_death = filtered_df_death.groupby(['date']).sum().sort_values(ascending=True, by='date')


    trace1 = go.Scatter(
        x = filtered_df_conf.index,
        y = filtered_df_conf['hospitalises'],
        mode = 'lines',
        name = 'Hospitalizations',
        marker=dict(color='orange')
    )

    trace2 = go.Scatter(
        x = filtered_df_recov.index,
        y = filtered_df_recov['deces'],
        mode = 'lines',
        name = 'Deaths',
        marker=dict(color='red')
    )

    trace3 = go.Scatter(
        x = filtered_df_death.index,
        y = filtered_df_death['reanimation'],
        mode = 'lines',
        name = 'Reanimations',
        marker=dict(color='purple')
    )

    traces = [trace1, trace2, trace3]


    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'showgrid': False, 'fixedrange':True},
            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
            hovermode='closest'
        )
    }

"""
#Confirmed graph

@app.callback(Output('country_graph_conf', 'figure'),
              [Input('country-picker', 'value')])
def update_figure(selected_region):

    filtered_df_conf = covid[covid['maille_nom'] == selected_region]
    filtered_df_conf['date'] =pd.to_datetime(filtered_df_conf.date)
    filtered_df_conf = filtered_df_conf.groupby(['date']).sum().sort_values(ascending=True, by='date')


    trace_con = go.Bar(
        x = filtered_df_conf.index,
        y = filtered_df_conf['hospitalises'],
        name = 'Confirmed',
        marker=dict(color='orange')
    )


    traces = [trace_con]


    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'showgrid': False, 'fixedrange':True},
            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
            hovermode='closest',
        )
    }

#End

#Recovered graph

@app.callback(Output('country_graph_recov', 'figure'),
              [Input('country-picker', 'value')])
def update_figure(selected_region):

    filtered_df_recov = covid[covid['maille_nom'] == selected_region]
    filtered_df_recov['date'] =pd.to_datetime(filtered_df_recov.date)
    filtered_df_recov = filtered_df_recov.groupby(['date']).sum().sort_values(ascending=True, by='date')


    trace_rec = go.Bar(
        x = filtered_df_recov.index,
        y = filtered_df_recov['nouvelles_hospitalisations'],
        name = 'Confirmed',
        marker=dict(color='orange')
    )


    traces = [trace_rec]


    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'showgrid': False, 'fixedrange':True},
            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
            hovermode='closest'
        )
    }

#End

#Deaths graph

@app.callback(Output('country_graph_deat', 'figure'),
              [Input('country-picker', 'value')])
def update_figure(selected_region):

    filtered_df_death = covid[covid['maille_nom'] == selected_region]
    filtered_df_death['date'] =pd.to_datetime(filtered_df_death.date)
    filtered_df_death = filtered_df_death.groupby(['date']).sum().sort_values(ascending=True, by='date')


    trace_deat = go.Bar(
    x = filtered_df_death.index,
    y = filtered_df_death['reanimation'],
    name = 'Deaths',
    marker=dict(color='purple')
)


    traces = [trace_deat]


    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'showgrid': False, 'fixedrange':True},
            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
            hovermode='closest'
        )
    }

#End

#EHPAD Graph
@app.callback(Output('country_graph_ehpad', 'figure'),
              [Input('country-picker', 'value')])
def update_figure(selected_region):

    filtered_df_new_rea = covid[covid['maille_nom'] == selected_region]
    filtered_df_new_rea['date'] =pd.to_datetime(filtered_df_new_rea.date)
    filtered_df_new_rea = filtered_df_new_rea.groupby(['date']).sum().sort_values(ascending=True, by='date')


    trace_new_rea = go.Bar(
        x = filtered_df_new_rea.index,
        y = filtered_df_new_rea['nouvelles_reanimations'],
        name = 'New_Reanimation',
        marker=dict(color='purple')
    )


    traces = [trace_new_rea]


    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'showgrid': False, 'fixedrange':True},
            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
            hovermode='closest'
        )
    }

#End

#EHPAD Deaths Graph
@app.callback(Output('country_graph_ehpad_deaths', 'figure'),
              [Input('country-picker', 'value')])
def update_figure(selected_region):

    filtered_df_deces = covid[covid['maille_nom'] == selected_region]
    filtered_df_deces['date'] =pd.to_datetime(filtered_df_deces.date)
    filtered_df_deces = filtered_df_deces.groupby(['date']).sum().sort_values(ascending=True, by='date')


    trace_gueris = go.Bar(
        x = filtered_df_deces.index,
        y = filtered_df_deces['deces'],
        name = 'deces',
        marker=dict(color='red')
    )


    traces = [trace_gueris]


    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'showgrid': False, 'fixedrange':True},
            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
            hovermode='closest'
        )
    }

#End



@app.callback(
    Output("country_conf_text", "children"),
    [Input('country-picker', 'value')],
)
def update_conf_text(selected_region):
    filtered_df_conf = dfr[dfr['maille_nom'] == selected_region]
    filtered_df_conf['date'] =pd.to_datetime(filtered_df_conf.date)
    filtered_df_conf = filtered_df_conf.groupby(['date']).sum().sort_values(ascending=True, by='date')

    num_count_conf = filtered_df_conf['hospitalises'].max()
    num_count_conf = int(num_count_conf)
    return (f"{num_count_conf:,}")

@app.callback(
    Output("country_reco_text", "children"),
    [Input('country-picker', 'value')],
)
def update_conf_text(selected_region):

    filtered_df_recov = dfr[dfr['maille_nom'] == selected_region]
    filtered_df_recov['date'] =pd.to_datetime(filtered_df_recov.date)
    filtered_df_recov = filtered_df_recov.groupby(['date']).sum().sort_values(ascending=True, by='date')

    num_count_reco = filtered_df_recov['deces'].max()
    num_count_reco = int(num_count_reco)
    return (f"{num_count_reco:,}")

@app.callback(
    Output("country_deat_text", "children"),
    [Input('country-picker', 'value')],
)
def update_conf_text(selected_region):

    filtered_df_death = dfr[dfr['maille_nom'] == selected_region]
    filtered_df_death['date'] =pd.to_datetime(filtered_df_death.date)
    filtered_df_death = filtered_df_death.groupby(['date']).sum().sort_values(ascending=True, by='date')

    num_count_deat = filtered_df_death['reanimation'].max()
    num_count_deat = int(num_count_deat)
    return (f"{num_count_deat:,}")

"""
@app.callback(
    Output("country_deat_text", "children"),
    [Input('country-picker', 'value')],
)
def update_conf_text(selected_region):

    filtered_ehpad_conf = dfr[dfr['maille_nom'] == selected_region]
    filtered_ehpad_conf['date'] =pd.to_datetime(filtered_ehpad_conf.date)
    filtered_ehpad_conf = filtered_ehpad_conf.groupby(['date']).sum().sort_values(ascending=True, by='date')

    num_count_ehpad = filtered_ehpad_conf['cas_ehpad'].max()
    num_count_ehpad = int(num_count_ehpad)
    return (f"{num_count_ehpad:,}")

@app.callback(
    Output("country_deat_text", "children"),
    [Input('country-picker', 'value')],
)
def update_conf_text(selected_region):

    filtered_ehpad_death = dfr[dfr['maille_nom'] == selected_region]
    filtered_ehpad_death['date'] =pd.to_datetime(filtered_ehpad_death.date)
    filtered_ehpad_death = filtered_ehpad_death.groupby(['date']).sum().sort_values(ascending=True, by='date')

    num_count_ehpad_death = filtered_ehpad_death['deces_ehpad'].max()
    num_count_ehpad_death = int(num_count_ehpad_death)
    return (f"{num_count_ehpad_death:,}")
"""

layout_france = html.Div([html.Br(),france], style={"text-align":"center", 'width': '100%', 'background-color': '#DCDCDC', "background-size": "cover", "background-position": "center"})
