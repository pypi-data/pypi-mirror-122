from dash import html
import dash_bootstrap_components as dbc

#style of navitem
padding = "5px"

#normal button for navbar
def normal(text, id, color = "secondary", size = None):
    return dbc.NavItem(
        children = [
            html.Div(style = {"width": padding}),
            dbc.Button(text, color = color, id = id, size = size),
            html.Div(style = {"width": padding})
        ],
        style = {"display": "flex"}
    )

#href button for navbar
def href(text, id, href = "/", color = "secondary", size = None):
    return dbc.NavItem(
        children = [
            html.Div(style = {"width": padding}),
            html.A(
                dbc.Button(text, color = color, id = id, size = size),
                href = href,
                target = "_blank"
            ),
            html.Div(style = {"width": padding})
        ],
        style = {"display": "flex"}
    )