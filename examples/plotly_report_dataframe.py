import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.long_callback import DiskcacheLongCallbackManager
from utils import gbm
from _plotly_dash_board_template import content, configure_sidebar

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np

import datetime
import diskcache

import pandas_datareader as web

import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
import pyinvestingsnippets 

ASSET_TICKERS = ['Asset1', 'Asset2', 'Asset3', 'Asset4']
BENCHMARK_TICKERS = ['Bench1', 'Bench2']

def tracking_error(r_a, r_b):
    """
    Returns the Tracking Error between the two return series
    """
    return np.sqrt(((r_a - r_b)**2).sum())

def information_ratio(returns, benchmark_returns, periods=252):
    """It measures a trader's ability to generate excess returns relative to a benchmark."""
    return_difference = returns.annualized(periods) - benchmark_returns.annualized(periods)
    volatility = (returns - benchmark_returns).std() * (periods ** 0.5)
    information_ratio = return_difference.mean() / volatility
    return information_ratio

def modigliani_ratio(returns, benchmark_returns, rf, periods=252):
    """The Modigliani ratio (M2) measures the returns of the portfolio,
    adjusted for the risk of the portfolio relative to that of some benchmark."""
    sharpe_ratio = returns.sharpe(rf, periods)
    benchmark_volatility = benchmark_returns.volatility_annualized(periods)
    m2_ratio = (sharpe_ratio * benchmark_volatility) + rf
    return m2_ratio

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], long_callback_manager=long_callback_manager)
app.layout = html.Div([configure_sidebar(ASSET_TICKERS, BENCHMARK_TICKERS), content])

@app.long_callback(Output('memory', 'data'),
              [Input('submit_button', 'n_clicks')],
              [State('dropdown_tickers', 'value'),
                State('dropdown_benchmark', 'value'),
                State('radio_years', 'value'),
                State('radio_rolling_window', 'value')
              ],
              running=[
                (Output("submit_button", "disabled"), True, False),
                (Output("cancel_button_id", "disabled"), False, True),
                (
                    Output("progress_bar", "style"),
                    {"visibility": "visible"},
                    {"visibility": "hidden"},
                ),
              ],
              cancel=[Input("cancel_button_id", "n_clicks")],
              progress=[Output("progress_bar", "value"), Output("progress_bar", "max")],
              prevent_initial_call=True,
              )
def collect_params(set_progress, n_clicks, dropdown_tickers_value, dropdown_benchmark_value, radio_years_value, radio_rolling_window_value):
    if not n_clicks:
        return {}
    
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=radio_years_value*365)
    end_date_frmt = end_date.strftime("%Y-%m-%d")
    start_date_frmt = start_date.strftime("%Y-%m-%d")

    set_progress(("1", "3"))
    # prices = web.DataReader(dropdown_tickers_value + [dropdown_benchmark_value], data_source='yahoo', start=start_date_frmt, end=end_date_frmt)['Adj Close']
    prices = gbm(10, len(dropdown_tickers_value + [dropdown_benchmark_value]), steps_per_year=252)
    prices.columns = dropdown_tickers_value + [dropdown_benchmark_value]
    
    set_progress(("2", "3"))
    prices = prices.loc[start_date.strftime("%Y-%m-%d"):]
    
    set_progress(("3", "3"))

    return {
        'dropdown_tickers_value': dropdown_tickers_value,
        'dropdown_benchmark_value': dropdown_benchmark_value,
        'years': radio_years_value,
        'rolling_window_value': radio_rolling_window_value,
        'risk_free_rate': 0.03,
        'prices': prices.to_json(orient='split'),
    }


@app.callback(
    Output('graph_wi', 'figure'),
    Input('memory', 'data'))
def update_wi(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')

    try:
        wi_figure = prices.returns.wealth_index.plotly()
    except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
        wi_figure = prices.returns.wealth_index.plotly()
    
    wi_figure.update_layout(
        title="Performance on 1$",
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return wi_figure


@app.callback(
    Output('graph_dd', 'figure'),
    Input('memory', 'data'))
def update_dd(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')

    try:
        fig_dd = prices.returns.wealth_index.drawdown.plotly()
    except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
        fig_dd = prices.returns.wealth_index.drawdown.plotly()

    fig_dd.layout.yaxis.tickformat = '.1%'
    fig_dd.update_layout(
        title="Drawdown",
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return fig_dd


@app.callback(
    Output('graph_arets', 'figure'),
    Input('memory', 'data'))
def update_arets(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')

    try:
        ann_rets_fig = px.bar(prices.annual_returns.data, barmode="group")
    except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
        ann_rets_fig = px.bar(prices.annual_returns.data, barmode="group")
    ann_rets_fig.layout.yaxis.tickformat = ',.1%'

    ann_rets_fig.update_layout(
        title="Annual Returns",
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return ann_rets_fig


@app.callback(
    Output('graph_rolling_rets', 'figure'),
    Input('memory', 'data'))
def update_graph_rolling_rets(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')
    
    try:
        fig_rr = pyinvestingsnippets.RollingReturns(prices.returns.data, rolling_window=data['rolling_window_value']).plotly()
    except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
        fig_rr = pyinvestingsnippets.RollingReturns(prices.returns.data, rolling_window=data['rolling_window_value']).plotly()

    fig_rr.layout.yaxis.tickformat = ',.1%'

    fig_rr.update_layout(
        title="Rolling Returns",
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return fig_rr

@app.callback(
    Output('graph_rolling_vol', 'figure'),
    Input('memory', 'data'))
def update_graph_rolling_vol(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')
    
    try:
        fig_rv = pyinvestingsnippets.RollingVolatility(prices.returns.data, rolling_window=data['rolling_window_value'], window=252).plotly()
    except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
        fig_rv = pyinvestingsnippets.RollingVolatility(prices.returns.data, rolling_window=data['rolling_window_value'], window=252).plotly()
    fig_rv.layout.yaxis.tickformat = ',.1%'

    fig_rv.update_layout(
        title="Rolling Volatility",
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return fig_rv


@app.callback(
    Output('graph_risk_reward', 'figure'),
    Input('memory', 'data'))
def update_graph_risk_reward(data):
    if data is None:
        raise PreventUpdate

    prices = pd.read_json(data["prices"], orient='split')

    all_values = pd.DataFrame()
    for asset_name in prices.columns:
        ann_vol = prices[asset_name].returns.volatility_annualized(252)
        ann_ret = prices[asset_name].returns.annualized(ppy=252)
        all_values = pd.concat([all_values, pd.DataFrame({
                'Name': asset_name, 'Risk': ann_vol, 'Return': ann_ret,
            },
            index=[asset_name])], axis=0)

    try:
        fig = px.scatter(all_values, x='Risk', y='Return', hover_data=['Name'], color="Name")
    except Exception:  # due to bug in plotly https://github.com/plotly/plotly.py/issues/3441
        fig = px.scatter(all_values, x='Risk', y='Return', hover_data=['Name'], color="Name")
    fig.update_traces(marker_size=10)
    fig.layout.yaxis.tickformat = '.1%'
    fig.layout.xaxis.tickformat = '.1%'
    fig.update_layout(
        title="Risk/Reward",
        xaxis_title="Risk",
        yaxis_title="Reward",
        legend_title="",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="right",
            x=1
        ),
    )
    return fig


@app.callback(
    Output('graph_stats', 'figure'),
    Input('memory', 'data'))
def update_graph_stats(data):
    if data is None:
        raise PreventUpdate
    
    prices = pd.read_json(data["prices"], orient='split')

    all_stats = [{'name': "Stat\Symbol", 'vals': ['Total Return', 'Return Annualized', 'CAGR', 'Volatility', 'Max DrawDown', 'Min DrawDown Duration', 'Max DrawDown Duration', 'Beta', 'Tracking Error', 'Sharpe Ratio', 'M2 Ratio', 'Information Ratio', 'SRRI']}]
    for asset_name in prices.columns:
        asset_values = []
        asset_values.append(f"{prices[asset_name].returns.wealth_index.total_return*100:.2f}%")
        asset_values.append(f"{prices[asset_name].returns.annualized(252)*100:.2f}%")
        asset_values.append(f"{prices[asset_name].returns.wealth_index.cagr*100:.2f}%")
        asset_values.append(f"{prices[asset_name].returns.volatility_annualized(252)*100:.2f}%")
        asset_values.append(f"{prices[asset_name].returns.wealth_index.drawdown.max_drawdown*100:.2f}%")
        asset_values.append(f"{prices[asset_name].returns.wealth_index.drawdown.durations.mean.days} days")
        asset_values.append(f"{prices[asset_name].returns.wealth_index.drawdown.durations.max.days} days")
        asset_values.append(f"{pyinvestingsnippets.BetaCovariance(prices.iloc[: , -1].returns.data, prices[asset_name].returns.data).beta:.2}")
        asset_values.append(f"{tracking_error(prices[asset_name].returns.data, prices.iloc[: , -1].returns.data):.4f}")
        asset_values.append(f"{prices[asset_name].returns.sharpe(data['risk_free_rate'], 252):.2f}")
        asset_values.append(f"{modigliani_ratio(prices[asset_name].returns, prices.iloc[: , -1].returns, data['risk_free_rate'], 252):.2f}")
        asset_values.append(f"{information_ratio(prices[asset_name].returns, prices.iloc[: , -1].returns, 252):.2f}")
        asset_values.append(f"{prices[asset_name].monthly_returns.srri.risk_class}") if prices[asset_name].monthly_returns.data.shape[0] >=60 else '-' 
        all_stats.append({'name':asset_name, 'vals': asset_values})

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