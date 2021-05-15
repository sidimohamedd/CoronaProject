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
 

#World data
dw = pd.read_csv("https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv", sep= ",")
dw[["Confirmed", "Recovered", "Deaths"]].astype(int)
#Sum world data
dw_new = dw[dw.groupby('Country').Date.transform('max') == dw['Date']]
dw_new['Date'] = pd.to_datetime(dw_new['Date'],format='%Y-%m-%d')


df_overall_temp =  dw_new.groupby(['Country'])['Confirmed','Recovered','Deaths'].sum().sort_values(ascending=False, by=['Confirmed'])[:10]
df_overall_temp = df_overall_temp.reset_index()


conf_top = pd.DataFrame(df_overall_temp)

df_confirmed_chart = pd.DataFrame(dw.groupby(['Date']).sum()['Confirmed']).sort_values(ascending=True, by=['Confirmed'])
df_recovered_chart = pd.DataFrame(dw.groupby(['Date']).sum()['Recovered']).sort_values(ascending=True, by=['Recovered'])
df_death_chart = pd.DataFrame(dw.groupby(['Date']).sum()['Deaths']).sort_values(ascending=True, by=['Deaths'])



def update_conf_text():

    num_conf = dw_new['Confirmed'].sum()
    return (f"{num_conf:,}")

def update_reco_text():

    num_reco = dw_new['Recovered'].sum()
    return (f"{num_reco:,}")

def update_deat_text():

    num_deat = dw_new['Deaths'].sum()
    return (f"{num_deat:,}")

def update_mortrate_text():

    num_deat = dw_new['Deaths'].sum()
    num_conf = dw_new['Confirmed'].sum()
    return str(((num_deat/num_conf)*100).round(1)) + "%"

def update_recorate_text():

    num_reco = dw_new['Recovered'].sum()
    num_conf = dw_new['Confirmed'].sum()
    return str(((num_reco/num_conf)*100).round(1)) + "%"

def update_active_text():

    num_acti = dw_new['Confirmed'].sum() - dw_new['Deaths'].sum() - dw_new['Recovered'].sum()
    return (f"{num_acti:,}")




world = html.Div([
                    html.Div(
                                [
                                    html.Div([ 
                                        html.H6('Last update : ' + str(dw_new.Date.max()),
                                        style={'text-align': 'center', "margin-bottom": "0px", "width":"100%", 'font-size': '20px', 'font-weight': 'bold','color': 'rgb(49, 69, 106)'}
                                                )
                                            ],className='one-third column',id='title1'),

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H3(
                                                        "COVID-19 Dashboard", style={'text-align': 'center', "margin-bottom": "0px", "width":"100%", 'font-size': '45px', 'font-weight': 'bold','color': 'rgb(49, 69, 106)'},
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
                                                href="https://www.who.int/health-topics/coronavirus#tab=tab_1",
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
                                [
                                    html.Div(
                                        [
                                            html.H5(
                                                "Worldwide Cases", style={'margin-top': '40px',
                                                                            'font-size': '25px',
                                                                            'font-weight': '700',
                                                                            'text-align': 'center',
                                                                            'color': 'rgb(49, 69, 106)',
                                                                            'margin-bottom': '30px'}
                                            ),
                                        ]
                                    )
                                ],
                                className="full columns",
                            ),
           
                    html.Div(
                                [html.Div(
                                    [html.P("Confirmed"), html.H1(id="conf_text", children=update_conf_text(), style={'font-weight': '700'})],
                                        id="infected",
                                        className="mini_container",
                                        style={
                                            'background-color': 'orange',
                                            'color': 'white',
                                            'font-size': '26px',
                                            'text-align': 'center',
                                            'flex': '1'
                                            }
                                         ),
                                html.Div(
                                        [html.P("Recovered"), html.H1(id="reco_text", children=update_reco_text(), style={'font-weight': '700'})],
                                        id="recoveries",
                                        className="mini_container",
                                        style={
                                            'background-color': 'rgb(76, 199, 112)',
                                            'color': 'white',
                                            'font-size': '26px',
                                            'text-align': 'center',
                                            'flex': '1'
                                            }
                                        ),
                                html.Div(
                                        [html.P("Deaths"), html.H1(id="deat_text", children=update_deat_text(), style={'font-weight': '700'})],
                                        id="deaths",
                                        className="mini_container",
                                        style={
                                            'background-color': 'rgb(204, 75, 75)',
                                            'color': 'white',
                                            'font-size': '26px',
                                            'text-align': 'center',
                                            'flex': '1'
                                            }
                                        )
                                ],
                                id="one-info-container",
                                className=" row container-display",
                                style = {'text-align': 'center', "columnCount":3}
                            ),
                

                    html.Div(
                                [
                                html.Div(
                                    [html.P("Mortality Rate"), html.H1(id="avg_conf_text", children=update_mortrate_text(), style={'font-weight': '700'})],
                                        id="mortality-rate",
                                        className="mini_container",
                                        style={
                                            'background-color': 'white',
                                            'color': 'rgba(49,69,106,1)',
                                            'font-size': '26px',
                                            'text-align': 'center',
                                            'flex': '1'
                                            }
                                         ),
                                html.Div(
                                        [html.P("Recovery Rate"), html.H1(id="avg_reco_text", children=update_recorate_text(), style={'font-weight': '700'})],
                                        id="recovery-rate",
                                        className="mini_container",
                                        style={
                                            'background-color': 'white',
                                            'color': 'rgba(49,69,106,1)',
                                            'font-size': '26px',
                                            'text-align': 'center',
                                            'flex': '1'
                                            }
                                        ),
                                html.Div(
                                        [html.P("Active Cases"), html.H1(id="active_cases_text", children=update_active_text(), style={'font-weight': '700'})],
                                        id="active-cases",
                                        className="mini_container",
                                        style={
                                            'background-color': 'white',
                                            'color': 'rgba(49,69,106,1)',
                                            'font-size': '26px',
                                            'text-align': 'center',
                                            'flex': '1'
                                            }
                                        )
                                ],
                                id="two-info-container",
                                className=" row container-display",
                                style = {'text-align': 'center', "columnCount":3}
                            ),


                    html.Div(
                                [
                                    html.H5(
                                        "Cumulative Cases (Worldwide)", style={'margin-top': '20px',
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
                                [dcc.Graph(
                                    id='scatter4',
                                    figure={
                                        'data': [
                                            go.Scatter(
                                                    x = df_confirmed_chart.index,
                                                    y = df_confirmed_chart['Confirmed'],
                                                    mode = 'lines+markers',
                                                    name = 'Confirmed',
                                                    marker=dict(color='blue')
                                                ),
                                            go.Scatter(
                                                    x = df_recovered_chart.index,
                                                    y = df_recovered_chart['Recovered'],
                                                    mode = 'lines+markers',
                                                    name = 'Recovered',
                                                    marker=dict(color='green')
                                                ),
                                            go.Scatter(
                                                    x = df_death_chart.index,
                                                    y = df_death_chart['Deaths'],
                                                    mode = 'lines+markers',
                                                    name = 'Deaths',
                                                    marker=dict(color='red')
                                                )
                                        ],
                                        'layout': go.Layout(
                                            # title = 'Overall Cases (Worldwide)',
                                            xaxis={'showgrid': False, 'fixedrange':True},
                                            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
                                            hovermode='closest'
                                        )
                                    }
                                )],
                                id="overallGraphContainer",
                                className="pretty_container",
                                style={
                                    'background-color': '#1E88E5',
                                    'padding': '5px',
                                    'text-align': 'center',
                                    'columnCount':1
                                    }
                            ),

        html.Div(
                    [
                    html.Div(
                                [

                                    html.Div(
                                        [
                                            html.H5(
                                                "Most Affected Countries", style={'margin-top': '20px',
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
                                                [dcc.Graph(
                                                    id='scatter3',
                                                    figure={
                                                        'data': [
                                                            go.Bar(
                                                                    x = conf_top['Country'],
                                                                    y = conf_top['Confirmed'],
                                                                    name = 'Confirmed',
                                                                    marker=dict(color='#1E88E5')
                                                                ),
                                                            go.Bar(
                                                                    x = conf_top['Country'],
                                                                    y = conf_top['Recovered'],
                                                                    name='Recovered',
                                                                    marker=dict(color='#43A047')
                                                                ),
                                                            go.Bar(
                                                                    x = conf_top['Country'],
                                                                    y = conf_top['Deaths'],
                                                                    name='Deaths',
                                                                    marker=dict(color='#E53935')
                                                                )
                                                        ],
                                                        'layout': go.Layout(
                                                            # title = 'Countries Most Affected by the Corona Virus',
                                                            xaxis={'showgrid': False, 'fixedrange':True},
                                                            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
                                                            hovermode='closest'
                                                        )
                                                    }
                                                )],
                                                id="countGraphContainer",
                                                className="pretty_container",
                                                style={
                                                    'background-color': '#1E88E5',
                                                    'padding': '5px',
                                                    }
                                            ),

                                ],
                                className="six columns",
                            ),

            html.Div(
                        [

                            html.Div(
                                [
                                    html.H5(
                                        "Recovery Comparison for the most affected", style={'margin-top': '20px',
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
                                        [dcc.Graph(
                                            id='scatter10',
                                            figure={
                                                'data': [
                                                    go.Scatter(
                                                            x=conf_top['Confirmed'],
                                                            y=conf_top['Country'],
                                                            marker=dict(color="blue", size=12),
                                                            mode="markers",
                                                            name="Confirmed",
                                                        ),
                                                    go.Scatter(
                                                            x=conf_top['Recovered'],
                                                            y=conf_top['Country'],
                                                            marker=dict(color="green", size=12),
                                                            mode="markers",
                                                            name="Recovered",
                                                        )
                                                ],
                                                'layout': go.Layout(
                                                    # title = 'Countries Most Affected by the Corona Virus',
                                                    xaxis={'fixedrange':True},
                                                    yaxis={'fixedrange':True},
                                                    hovermode='closest'
                                                )
                                            }
                                        )],
                                        id="compGraphContainer",
                                        className="pretty_container",
                                        style={
                                            'background-color': '#1E88E5',
                                            'padding': '5px',
                                            }
                                    ),

                        ],
                        className="six columns",
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
                                                "Confirmed Cases (Worldwide)", style={'margin-top': '20px',
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
                                                [dcc.Graph(
                                                    id='scatter11',
                                                    figure={
                                                        'data': [
                                                            go.Bar(
                                                                    x = df_confirmed_chart.index,
                                                                    y = df_confirmed_chart['Confirmed'],
                                                                    name = 'Confirmed',
                                                                    marker=dict(color='#1E88E5')
                                                                )

                                                        ],
                                                        'layout': go.Layout(
                                                            # title = 'Countries Most Affected by the Corona Virus',
                                                            xaxis={'showgrid': False, 'fixedrange':True},
                                                            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
                                                            hovermode='closest'
                                                        )
                                                    }
                                                )],
                                                id="confworldGraphContainer",
                                                className="pretty_container",
                                                style={
                                                    'background-color': '#1E88E5',
                                                    'padding': '5px',
                                                    }
                                            ),

                                ],
                                className="six columns",
                            ),

                    html.Div(
                                [

                                    html.Div(
                                        [
                                            html.H5(
                                                "Recovered Cases (Worldwide)", style={'margin-top': '20px',
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
                                                [dcc.Graph(
                                                    id='scatter12',
                                                    figure={
                                                        'data': [
                                                            go.Bar(
                                                                    x = df_recovered_chart.index,
                                                                    y = df_recovered_chart['Recovered'],
                                                                    name = 'Recovered',
                                                                    marker=dict(color='#43A047')
                                                                )

                                                        ],
                                                        'layout': go.Layout(
                                                            # title = 'Countries Most Affected by the Corona Virus',
                                                            xaxis={'showgrid': False, 'fixedrange':True},
                                                            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
                                                            hovermode='closest'
                                                        )
                                                    }
                                                )],
                                                id="recovworldGraphContainer",
                                                className="pretty_container",
                                                style={
                                                    'background-color': '#1E88E5',
                                                    'padding': '5px',
                                                    }
                                            ),

                                ],
                                className="six columns",
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
                                                "Deaths (Worldwide)", style={'margin-top': '20px',
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
                                                [dcc.Graph(
                                                    id='scatter13',
                                                    figure={
                                                        'data': [
                                                            go.Bar(
                                                                    x = df_death_chart.index,
                                                                    y = df_death_chart['Deaths'],
                                                                    name = 'Deaths',
                                                                    marker=dict(color='#E53935')
                                                                )

                                                        ],
                                                        'layout': go.Layout(
                                                            # title = 'Countries Most Affected by the Corona Virus',
                                                            xaxis={'showgrid': False, 'fixedrange':True},
                                                            yaxis={'title': 'No. of People', 'showgrid': False, 'fixedrange':True},
                                                            hovermode='closest'
                                                        )
                                                    }
                                                )],
                                                id="deatworldGraphContainer",
                                                className="pretty_container",
                                                style={
                                                    'background-color': '#1E88E5',
                                                    'padding': '5px',
                                                    }
                                            ),

                                ],
                                className="six columns",
                            ),

                    html.Div([

                        html.Div(
                            [
                                html.H5(
                                    "Worldwide Count", style={'margin-top': '20px',
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
                        dash_table.DataTable(
                        data=dw_new.to_dict('records'),
                        columns=[{'id': c, 'name': c} for c in dw_new.columns[1:]],
                        fixed_rows={ 'headers': True, 'data': 0 },
                        filter_action="native",
                        sort_action="native",
                        style_cell={
                                'fontFamily': 'Open Sans',
                                'textAlign': 'center',
                                'height': '60px',
                                #'height': 'auto',
                            # all three widths are needed
                                'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                                'whiteSpace': 'normal'
                                    },
                                    style_table={
                                        'height': '459px',
                                        'overflowX': 'hidden',
                                        'borderRadius': '0px'
                                    },
                                    style_header={
                                        "left": "50%",
                                        "marginRight": "-50%",
                                        'backgroundColor': 'blue',
                                        'color':'white'
                                    }
                    ),
                        html.Div(id='datatable-interactivity-container')
                    ],
                    id="right-column",
                    className="six columns"
                    ),


            ],  className= "row",
                style={'text-align': 'center', "width":"100%", "margin-bottom": "0px", "columnCount":1},
        ),
        html.Div(
                [
                    html.Div(
                        [
                            html.A(
                                html.H5(
                                    "Data sources: COVID-19 dataset", style={'margin-top': '20px',
                                                                'font-size': '14px',
                                                                'text-align': 'center',
                                                                'color': 'rgb(49, 69, 106)',
                                                                'padding-top': '15px',
                                                                'margin-bottom': '20px'
                                                                }
                                ), href="https://github.com/datasets/covid-19",
                            ),

                                html.H5(
                                    "Authors: Kossivi KUGBE & Saïd MAALLEM & Sidi Mohamed SID'EL MOCTAR", style={'margin-top': '20px',
                                                                'font-size': '14px',
                                                                'text-align': 'center',
                                                                'color': 'rgb(49, 69, 106)',
                                                                'padding-top': '15px',
                                                                'margin-bottom': '20px'
                                                                }
                                ),
                            

                        ]),
                ]),

])

layout_world  = html.Div([html.Br(),world], style={"text-align":"center", 'width': '100%', 'background-color': '#DCDCDC', "background-size": "cover", "background-position": "center"})