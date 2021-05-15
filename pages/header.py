import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

LOGO = "https://www.formasup-npc.org/wp-content/uploads/2018/05/ILIS_UnivLille2018.jpg"

navbar = dbc.Navbar(
    [
        html.A(
            # Alignement vertical de l'image et de l'acceuil
            dbc.Row(
                [   #logo
                    dbc.Col(html.Img(src=LOGO, height="40px")),
                    #Navlink Acceuil
                    dbc.NavLink("Worldwide", href="/covidworld",style={'color':'white'}),
                    #Navlink Worldwide
                    dbc.NavLink("France", href="/covidfrance",style={'color':'white'}),
                    #Navlink France
                    dbc.NavLink("SEAIRD modelisation", href="/modelisation",style={'color':'white'})
                ],
                align="cesnter",
                no_gutters=True,
            ),
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="dark",
    dark=True,
)
