import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np

import datetime

import pandas_datareader as web

import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import pyinvestingsnippets 


end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=5 * 365)
end_date_frmt = end_date.strftime("%Y-%m-%d")
start_date_frmt = start_date.strftime("%Y-%m-%d")

def tracking_error(r_a, r_b):
    """
    Returns the Tracking Error between the two return series
    """
    return np.sqrt(((r_a - r_b)**2).sum())


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig

def gbm(n_years = 10, n_scenarios=1000, mu=0.07, sigma=0.15, steps_per_year=12, s_0=100.0, prices=True):
    """
    Evolution of Geometric Brownian Motion trajectories, such as for Stock Prices through Monte Carlo
    :param n_years:  The number of years to generate data for
    :param n_paths: The number of scenarios/trajectories
    :param mu: Annualized Drift, e.g. Market Return
    :param sigma: Annualized Volatility
    :param steps_per_year: granularity of the simulation
    :param s_0: initial value
    :return: a numpy array of n_paths columns and n_years*steps_per_year rows
    """
    # Derive per-step Model Parameters from User Specifications
    dt = 1/steps_per_year
    n_steps = int(n_years*steps_per_year) + 1
    # the standard way ...
    # rets_plus_1 = np.random.normal(loc=mu*dt+1, scale=sigma*np.sqrt(dt), size=(n_steps, n_scenarios))
    # without discretization error ...
    rets_plus_1 = np.random.normal(loc=(1+mu)**dt, scale=(sigma*np.sqrt(dt)), size=(n_steps, n_scenarios))
    rets_plus_1[0] = 1
    ret_val = s_0*pd.DataFrame(rets_plus_1).cumprod() if prices else rets_plus_1-1
    return ret_val

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

controls = dbc.Row(
    [
        html.P('Tickers', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown_tickers',
            options=[{'label': i, 'value': i} for i in ['MSFT', 'FB']],
            value=[],  # default value
            multi=True
        ),
        html.P('Benchmark', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown_benchmark',
            options=[{'label': i, 'value': i} for i in ['SPY', '^GSPC']],
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
    ]
)

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
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

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content])

asset_prices = []
benchmark_price = None

@app.callback(Output('memory', 'data'),
              [Input('submit_button', 'n_clicks')],
              [State('dropdown_tickers', 'value'),
                State('dropdown_benchmark', 'value'),
                State('radio_years', 'value'),
                State('radio_rolling_window', 'value')
              ])
def collect_params(n_clicks, dropdown_tickers_value, dropdown_benchmark_value, radio_years_value, radio_rolling_window_value):
    if not n_clicks:
        raise PreventUpdate
    
    from dateutil.relativedelta import relativedelta
    yrs_ago = datetime.datetime.now() - relativedelta(days=radio_years_value*252)

    global asset_prices
    asset_prices = []
    for i, asset in enumerate(dropdown_tickers_value):
        # prices = web.DataReader(asset, data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']
        prices = gbm(10, 1, steps_per_year=252).iloc[:, 0] # gets the fist column of dataframe as series
        prices.index = pd.bdate_range(end=datetime.datetime.now(), periods=prices.shape[0]) # generates a time index
        
        prices.name = asset
        prices = prices.loc[yrs_ago.strftime("%Y-%m-%d"):]
        asset_prices.append({'ticker': asset, 'price': prices, 'color': px.colors.qualitative.Alphabet[i]})

    global benchmark_price
    benchmark_price = None
    bench_price = web.DataReader(dropdown_benchmark_value, data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']
    bench_price.name = dropdown_benchmark_value
    bench_price = bench_price.loc[yrs_ago.strftime("%Y-%m-%d"):]
    benchmark_price = {'ticker': dropdown_benchmark_value, 'price': bench_price, 'color': px.colors.qualitative.Alphabet[-1]}

    return {
        'dropdown_tickers_value': dropdown_tickers_value,
        'dropdown_benchmark_value': dropdown_benchmark_value,
        'radio_years_value': radio_years_value,
        'radio_rolling_window_value': radio_rolling_window_value,
        'downloaded': True
    }

@app.callback(
    Output('graph_wi', 'figure'),
    Input('memory', 'data'))
def update_wi(data):
    if data is None:
        raise PreventUpdate

    wi_figures = []

    fig_bench = benchmark_price['price'].prices.returns.wealth_index.plotly()
    fig_bench.update_traces(line_color=benchmark_price['color'], line_width=1)
    wi_figures.append(fig_bench)

    for asset in asset_prices:
        fig_wi_asset = asset['price'].prices.returns.wealth_index.plotly()
        fig_wi_asset.update_traces(line_color=asset['color'], line_width=1)
        wi_figures.append(fig_wi_asset)

    fig_wi = go.Figure(data=sum((fig.data for fig in wi_figures), ()))

    fig_wi.update_layout(
        title="Performance on 1$",
        legend_title="Symbol",
    )

    return fig_wi


@app.callback(
    Output('graph_dd', 'figure'),
    Input('memory', 'data'))
def update_dd(data):
    if data is None:
        raise PreventUpdate

    dd_figures = []

    fig_bench = benchmark_price['price'].prices.returns.wealth_index.drawdown.plotly()
    fig_bench.update_traces(line_color=benchmark_price['color'], line_width=1)
    dd_figures.append(fig_bench)

    for asset in asset_prices:
        fig1 = asset['price'].prices.returns.wealth_index.drawdown.plotly()
        fig1.update_traces(line_color=asset['color'], line_width=1)
        dd_figures.append(fig1)

    fig_dd = go.Figure(data=sum((fig.data for fig in dd_figures), ()))
    fig_dd.layout.yaxis.tickformat = '.1%'

    fig_dd.update_layout(
        title="Drawdown",
        legend_title="Symbol",
    )

    return fig_dd


@app.callback(
    Output('graph_arets', 'figure'),
    Input('memory', 'data'))
def update_arets(data):
    if data is None:
        raise PreventUpdate

    ann_rets = benchmark_price['price'].prices.returns.wealth_index.annual_returns.data
    for asset in asset_prices:
        ann_rets = pd.concat([ann_rets, asset['price'].prices.returns.wealth_index.annual_returns.data], axis=1)
    ann_rets = ann_rets.dropna(how='all')

    ann_rets_fig = px.bar(ann_rets, barmode="group")
    ann_rets_fig.layout.yaxis.tickformat = ',.1%'

    ann_rets_fig.update_layout(
        title="Annual Returns",
        legend_title="Symbol",
    )

    return ann_rets_fig

@app.callback(
    Output('graph_rolling_rets', 'figure'),
    Input('memory', 'data'))
def update_graph_rolling_rets(data):
    if data is None:
        raise PreventUpdate

    rolling_rets_figures = []

    fig_bench_r = pyinvestingsnippets.RollingReturns(benchmark_price['price'].prices.returns.data, rolling_window=data['radio_rolling_window_value']).plotly()
    fig_bench_r.update_traces(line_color=benchmark_price['color'], line_width=1)
    rolling_rets_figures.append(fig_bench_r)

    for asset in asset_prices:
        fig1_r = pyinvestingsnippets.RollingReturns(asset['price'].prices.returns.data, rolling_window=data['radio_rolling_window_value']).plotly()
        fig1_r.update_traces(line_color=asset['color'], line_width=1)
        rolling_rets_figures.append(fig1_r)

    fig = go.Figure(data=sum((fig.data for fig in rolling_rets_figures), ()))
    fig.layout.yaxis.tickformat = ',.1%'

    fig.update_layout(
        title="Rolling Returns",
        legend_title="Symbol",
    )

    return fig

@app.callback(
    Output('graph_rolling_vol', 'figure'),
    Input('memory', 'data'))
def update_graph_rolling_vol(data):
    if data is None:
        raise PreventUpdate

    rolling_vol_figures = []

    fig_bench_v = pyinvestingsnippets.RollingVolatility(benchmark_price['price'].prices.returns.data, rolling_window=data['radio_rolling_window_value'], window=252).plotly()
    fig_bench_v.update_traces(line_color=benchmark_price['color'], line_width=1)
    rolling_vol_figures.append(fig_bench_v)

    for asset in asset_prices:
        fig1_v = pyinvestingsnippets.RollingVolatility(asset['price'].prices.returns.data, rolling_window=data['radio_rolling_window_value'], window=252).plotly()
        fig1_v.update_traces(line_color=asset['color'], line_width=1)
        rolling_vol_figures.append(fig1_v)

    fig = go.Figure(data=sum((fig.data for fig in rolling_vol_figures), ()))
    fig.layout.yaxis.tickformat = ',.1%'

    fig.update_layout(
        title="Rolling Volatility",
        legend_title="Symbol",
    )

    return fig


@app.callback(
    Output('graph_risk_reward', 'figure'),
    Input('memory', 'data'))
def update_graph_risk_reward(data):
    if data is None:
        raise PreventUpdate

    all_values = pd.DataFrame()
    for asset in asset_prices:
        ann_vol = asset['price'].prices.returns.volatility_annualized(252)
        ann_ret = asset['price'].prices.returns.annualized(ppy=252)
        all_values = pd.concat([all_values, pd.DataFrame({'Name': asset['ticker'], 'Risk': ann_vol, 'Return': ann_ret, 'Color': asset['color']}, index=[asset['ticker']])], axis=0)

    fig = px.scatter(all_values, x='Risk', y='Return', hover_data=['Name'], color="Name")
    fig.update_traces(marker_size=10)
    fig.layout.yaxis.tickformat = '.1%'
    fig.layout.xaxis.tickformat = '.1%'
    fig.update_layout(
        title="Risk/Reward",
        xaxis_title="Risk",
        yaxis_title="Reward",
        legend_title="Symbol",
    )
    return fig


@app.callback(
    Output('graph_stats', 'figure'),
    Input('memory', 'data'))
def update_graph_stats(data):
    if data is None:
        raise PreventUpdate


    all_stats = [{'name': "Stat\Symbol", 'vals': ['Total Return', 'CAGR', 'Max DrawDown', 'Min DrawDown Duration', 'Max DrawDown Duration']}]
    for asset in asset_prices:
        asset_values = []
        asset_values.append(f"{asset['price'].prices.returns.wealth_index.total_return*100:.2}%")
        asset_values.append(f"{asset['price'].prices.returns.wealth_index.cagr*100:.2}%")
        asset_values.append(f"{asset['price'].prices.returns.wealth_index.drawdown.max_drawdown*100:.2}%")
        asset_values.append(f"{asset['price'].prices.returns.wealth_index.drawdown.durations.mean()}")
        asset_values.append(f"{asset['price'].prices.returns.wealth_index.drawdown.durations.max()}")
        all_stats.append({'name':asset['ticker'], 'vals': asset_values})
    

    asset_values = []
    asset_values.append(f"{benchmark_price['price'].prices.returns.wealth_index.total_return*100:.2}%")
    asset_values.append(f"{benchmark_price['price'].prices.returns.wealth_index.cagr*100:.2}%")
    asset_values.append(f"{benchmark_price['price'].prices.returns.wealth_index.drawdown.max_drawdown*100:.2}%")
    asset_values.append(f"{benchmark_price['price'].prices.returns.wealth_index.drawdown.durations.mean()}")
    asset_values.append(f"{benchmark_price['price'].prices.returns.wealth_index.drawdown.durations.max()}")
    all_stats.append({'name': benchmark_price['ticker'], 'vals': asset_values})

    fig = go.Figure(data=[go.Table(
        header=dict(values=[i['name'] for i in all_stats],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[i['vals'] for i in all_stats],
                fill_color='lavender',
                align='left'))
    ])
    fig.update_layout(
        title="Stats",
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)