import pandas as pd
import numpy as np
from scipy.integrate import odeint
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import dash_daq as daq
from app import app

# Equation du modele SEAIRD
def deriv(y, t, N, alpha, beta, gamma1, gamma2, teta, delta, mu, eta):
    S, E, I, A, R, D = y
    dSdt = (-beta * S *(I + delta * A)/(S+E+I+A+R)) - eta *S + eta * N
    dEdt = (beta * S *(I + delta * A)/(S+E+I+A+R)) - (mu + eta) * E
    dIdt = alpha * mu * E - (gamma1 + teta + eta) * I
    dAdt = (1- alpha)* mu * E - (gamma2 + eta) * A
    dRdt = gamma1 * I + gamma2 * A - eta * R
    dDdt = teta * I
    return dSdt, dEdt, dIdt, dAdt, dRdt, dDdt






modelisation=html.Div([
    html.H3("SEAIRD COVID-19 modeling", style={'text-align': 'center', "margin-bottom": "0px", "width":"100%", 'font-size': '45px', 'font-weight': 'bold','color': 'rgb(49, 69, 106)'}),
    html.Div([
    html.H4("Setting of parameters :", style={'text-align': 'justify', "margin-bottom": "0px", "width":"100%", 'font-size': '20px', 'font-weight': 'bold','color': 'rgb(49, 69, 106)'})
    ],  style={'text-align': 'center', "width":"100%", "margin-bottom": "0px", "columnCount":1}),
    html.Div([
    html.P('Population size',style={"height": "auto", "margin-bottom": "0.5vw"}),
    dcc.Input(id='N',
        value='1000',
        type='number',
        style={"height": "auto", "width": 170, "margin-bottom": "2vw"}
    ),
    html.P('Infected individuals',style={"height": "auto", "margin-bottom": "0.5vw"}),
    dcc.Input(
        id='IA0',
        value='100',
        type='number',
        style={"height": "auto", "width": 170, "margin-bottom": "2vw"}
    ),
    html.P('Removed persones',style={"height": "auto", "margin-bottom": "0.5vw"}),
    dcc.Input(
        id='R0',
        value='0',
        type='number',
        style={"height": "auto", "width": 170, "margin-bottom": "2vw"}
    ),
    html.P('Dead people',style={"height": "auto", "margin-bottom": "0.5vw"}),
    dcc.Input(
        id='D0',
        value='0',
        type='number',
        style={"height": "auto", "width": 170, "margin-bottom": "2vw"}
    ),
    
    ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '0.5vw','width': '14%','background-color': '#DCDCDC'}),
    html.Div([
    daq.Slider(
        id='beta',
        min=0,
        max=1,
        dots=False,
        handleLabel={"showCurrentValue": True,"label": "Value"},
        step=0.01,
        value=0.5,
        size=280),
        html.P(id= "ebeta", style={"margin-bottom": "3vw",'margin-top': '0vw', "text-align":"left"}
    ),
    daq.Slider(
        id='alpha',
        min=0,
        max=1,
        dots=False,
        handleLabel={"showCurrentValue": True,"label": "Value"},
        step=0.01,
        value=0.83,
        size= 280),
        html.P("Proportion of symptomatic", style={"margin-bottom": "3vw",'margin-top': '0vw', "text-align":"left"}
    ),
    daq.Slider(
        id='mu',
        min=0,
        max=1,
        dots=False,
        handleLabel={"showCurrentValue": True,"label": "Value"},
        step=0.01,
        value=0.20,
        size= 280),
    html.P("Progression rate from exposed to infective", style={"margin-bottom": "3vw",'margin-top': '0vw', "text-align":"left"}),
    
    daq.Slider(
        id='delta',
        min=0,
        max=1,
        dots=False,
        handleLabel={"showCurrentValue": True,"label": "Value"},
        step=0.01,
        value=0.18,
        size= 280),
    html.P("Infective force asymptomatic / symptomatic", style={"margin-bottom": "3vw",'margin-top': '0vw', "text-align":"left"}),
    daq.Slider(
        id='gamma1',
        min=0,
        max=1,
        dots=False,
        handleLabel={"showCurrentValue": True,"label": "Value"},
        step=0.01,
        value=0.99,
        size= 280),
    html.P(id="egamma1", style={"margin-bottom": "3vw",'margin-top': '0vw', "text-align":"left"}),
    daq.Slider(
        id='gamma2',
        min=0,
        max=1,
        dots=False,
        handleLabel={"showCurrentValue": True,"label": "Value"},
        step=0.1,
        value=1,
        size= 280),
    html.P("Recovry probability of asymptomatic people", style={"margin-bottom": "3vw",'margin-top': '0vw', "text-align":"left"}),
    daq.Slider(
        id='teta',
        min=0,
        max=100,
        dots=False,
        handleLabel={"showCurrentValue": True,"label": "Value"},
        step=0.1,
        value=0.7,
        size= 280),
    html.P(id="eteta", style={"margin-bottom": "3vw",'margin-top': '0vw', "text-align":"left"}),
    daq.Slider(
        id='eta',
        min=0,
        max=30,
        dots=False,
        handleLabel={"showCurrentValue": True,"label": "Value"},
        step=0.1,
        value=11.2,
        size= 280),
        html.P("Birth and death rate (‰ / year)", style={"margin-bottom": "3vw",'margin-top': '0vw', "text-align":"left"})
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '1vw', 'margin-top': '3vw','width': '25%','background-color': '#DCDCDC'}),
    html.Div([
    html.Div([
    dcc.Graph(id='my_graph')],
    style= {'background-color': '#1E88E5', 'padding': '5px',}),
    html.Div([
    html.Label("Set max day on x axis"),
    dcc.Input(id='t',
        value='30',
        type='number',
        style={'margin-left': '1vw', 'margin-top': '0vw'}
    )
    ],style={'margin-left': '0.5vw', 'margin-top': '1vw','display': 'inline-block'}),
    html.Div([
    dcc.RadioItems(
        id='l',
        options=[
            {'label': 'Linear', 'value': 'linear', 'text-align': 'left'},
            {'label': 'logarithmic', 'value': 'logarithmic'}
        ],
        value='linear'
    )   
    ],style={'margin-left': '6vw', 'margin-top': '0vw','display': 'inline-block'})
    ],style={'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '0vw', 'margin-top': '3vw','hight': '120%','width': '55%','background-color': '#DCDCDC'})
])

layout_modelisation  = html.Div([html.Br(),modelisation], style={"text-align":"center", 'width': '100%', 'background-color': '#DCDCDC', "background-size": "cover", "background-position": "center"})

@app.callback(
    Output('my_graph','figure'),
    Output('ebeta','children'),
    Output('egamma1','children'),
    Output('eteta','children'),
    [Input('N','value'),
    Input('IA0','value'),
    Input('R0','value'),
    Input('D0','value'),
    Input('alpha','value'),
    Input('beta','value'),
    Input('gamma1','value'),
    Input('gamma2','value'),
    Input('teta','value'),
    Input('delta','value'),
    Input('mu','value'),
    Input('eta','value'),
    Input('t','value'),
    Input('l','value')
    ])
def update_graph(N,IA0,R0,D0, alpha,beta,gamma1,gamma2,teta,delta,mu,eta,t,l):
    N= int(N)
    IA0= int(IA0)
    R0= int(R0)
    D0= int(D0)
    #### calcule des effectifs initiaux
    E0 = IA0 / mu #### modif
    I0 = alpha * IA0 
    A0 = (1-alpha) * IA0
    S0 = N - D0 - R0 - IA0 - E0
    alpha= float(alpha)
    beta= float(beta)
    gamma1= float(gamma1)
    gamma2= float(gamma2)
    teta= float(teta)/100
    delta= float(delta)
    mu= float(mu)
    eta= float(eta)/(1000*365)
    t= int(t)
    #### parametters estimation
    ebeta="Probability of transmission (estimated : " +str(round(E0/S0,1))+")"
    egamma1="Recovry probability symptomatic (estimated : " +str(round(R0/I0,1))+")"
    eteta="Fatality rate (%) (estimated : " +str(round((D0/I0)*100,1))+")"
    # time
    t = np.linspace(0, t - 1, t)

    # Initial conditions vector
    y0 = S0, E0, I0, A0, R0, D0
    # Integrate the SEAIRD equations over the time.
    ret = odeint(deriv, y0, t, args=(N, alpha, beta, gamma1, gamma2, teta, delta, mu, eta))
    S, E, I, A, R, D = ret.T
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="Susceptible : " + str(round(S[-1])), x=t, y=S,line=dict(color='royalblue')))
    fig.add_trace(go.Scatter(name="Exposed : " + str(round(E[-1])), x=t, y=E,line=dict(color='yellow')))
    fig.add_trace(go.Scatter(name="Symptomatic : " + str(round(I[-1])), x=t, y=I,line=dict(color='orange')))
    fig.add_trace(go.Scatter(name="Asymptomatic : " + str(round(A[-1])), x=t, y=A,line=dict(color='gray')))
    fig.add_trace(go.Scatter(name="Removed : " + str(round(R[-1])), x=t, y=R,line=dict(color='green')))
    fig.add_trace(go.Scatter(name="Dead : " + str(round(D[-1])), x=t, y=D,line=dict(color='red')))
    fig.update_layout(
    title="Evolution of COVID-19 epidemy according to SEAIRD model",
    legend_title_text='n on day '+str(round(t[-1]+1))+' : ',
    xaxis_title="",
    yaxis_title="Number of people (n)",
    legend=dict(orientation="h")
    )
    if l == "logarithmic":
        fig.update_xaxes(type="log")
    return fig ,ebeta,egamma1,eteta




