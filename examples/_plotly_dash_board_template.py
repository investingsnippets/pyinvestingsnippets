import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objects as go

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig


# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '22%',
    'margin-right': '2%',
    'padding': '10px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

def controls(asset_tickers, bench_tickers):
    return dbc.Row(
        [
            html.P('Tickers', style={
                'textAlign': 'center'
            }),
            dcc.Dropdown(
                id='dropdown_tickers',
                options=[{'label': i, 'value': i} for i in asset_tickers],
                value=[],  # default value
                multi=True
            ),
            html.P('Benchmark', style={
                'textAlign': 'center'
            }),
            dcc.Dropdown(
                id='dropdown_benchmark',
                options=[{'label': i, 'value': i} for i in bench_tickers],
                value=[],  # default value
                multi=False
            ),
            html.Br(),
            html.P('Years', style={
                'textAlign': 'center'
            }),
            dbc.Card([dbc.RadioItems(
                id='radio_years',
                options=[{
                        'label': '1',
                        'value': 1
                    },
                    {
                        'label': '3',
                        'value': 3
                    },
                    {
                        'label': '5',
                        'value': 5
                    }
                ],
                value=5,
                style={
                    'margin': 'auto'
                }
            )]),
            html.Br(),
            html.P('Rolling Window (days)', style={
                'textAlign': 'center'
            }),
            dbc.Card([dbc.RadioItems(
                id='radio_rolling_window',
                options=[{
                        'label': '30',
                        'value': 30
                    },
                    {
                        'label': '90',
                        'value': 90
                    },
                    {
                        'label': '252',
                        'value': 252
                    }
                ],
                value=252,
                style={
                    'margin': 'auto'
                }
            )]),
            html.Br(),
            dbc.Button(
                id='submit_button',
                n_clicks=0,
                children='Apply',
                color='primary'
            ),
            html.Button("Cancel Running Job!", id="cancel_button_id", style={"display": "none"}),
        ]
    )

def configure_sidebar(asset_tickers, bench_tickers):
    return html.Div(
        [
            html.H2('Parameters', style=TEXT_STYLE),
            html.Hr(),
            controls(asset_tickers, bench_tickers),
            html.Div(
                [
                    html.Progress(id="progress_bar", style={"display": "none"}),
                ]
            ),
        ],
        style=SIDEBAR_STYLE,
    )

content_wealthindex = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_wi', figure = blank_fig()), md=12
        )
    ]
)

content_drawdown = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_dd', figure = blank_fig()), md=12,
        )
    ]
)

content_annual_rets = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_arets', figure = blank_fig()), md=12,
        )
    ]
)

content_rolling = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_rolling_rets', figure = blank_fig()), md=6
        ),
        dbc.Col(
            dcc.Graph(id='graph_rolling_vol', figure = blank_fig()), md=6
        )
    ]
)

content_risk_reward = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_risk_reward', figure = blank_fig()), md=12,
        )
    ]
)

content_stats = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_stats', figure = blank_fig()), md=12,
        )
    ]
)

content = html.Div(
    [
        dcc.Store(id='memory'),
        html.H2('Report', style=TEXT_STYLE),
        html.Hr(),
        content_wealthindex,
        content_drawdown,
        content_annual_rets,
        content_rolling,
        content_risk_reward,
        content_stats,
    ],
    style=CONTENT_STYLE
)
