"""Main module for the site class"""
#! /usr/bin/env python

# Python imports
import sys
import os

# Module imports
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Local imports
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
import visnet1d

class Site:
    """Site class that handles the dash web app"""

    def __init__(self, function, boundaries, input_dict_list=None, **kwargs):
        """ Initialises a site to visualise a vasculature network.

        Args:
            function (object) : A function that takes a set of kwarg arguments and produces an
                output.
            boundaries (dict) : A dictionary of each location's start and end.
                Expected as a dictionary with:
                    "location name" : [start, end]
                for each location / edge.
            input_dict_list (list, optional) : A list of dictionaries where each dictionary has the fields:
                name (str) : Name of variable to be displayed to site.
                id (str) : Name to be passed to the function (also used as ID).
                value (object) : Default value to be displayed to site.
                type (str) : Type of the value.
                If None, doesn't display any inputs. Defaults to None.
        kwargs:
            plot (function, optional) : The function to plot the graph.
                Defaults to visnet1d.site._plot_x().
            xlab (str, optional) : The label for the x-axis. Defaults to "Value".
            ylab (str, optional) : The label for the y-ayis. Defaults to "Value".
            title (str, optional) : The title of the plot. Defaults to "signal".
        """

        # Sets pandas plotting backend
        pd.options.plotting.backend = "plotly"

        # Loads keyword arguments
        self.plot = kwargs.get('plot', None)
        self.xlab = kwargs.get('xlab', "Value")
        self.ylab = kwargs.get('ylab', "Time (s)")
        self.title = kwargs.get('title', "Signal")

        # Defines static methods/attributes
        self.app = Dash(__name__)
        self.input_dict_list = input_dict_list
        self.function = function
        self.boundaries = boundaries

        # Sets up a dummpy input which will be hidden.
        if input_dict_list is None:
            input_dict_list = [{"name" : "", "id": "foo", "value" : '', "type" : "hidden"}]

        # Defines dynamic methods/attributes
        self.function_kwargs = get_kwargs(input_dict_list)
        self.loc_slider_vals = dict()
        self.loc_percentages = dict()
        self.loc_keys = []

        locs = list(boundaries.keys())
        loc_dd_id = "loc-dropdown"
        loc_radio_id = "radio-locs"
        selected_locs = [locs[0]]

        self.app.layout = html.Div([
            html.Div([
                html.H1("Inputs"),
                html.Div([
                    "Location: ",
                    dcc.Dropdown(locs, locs[0], id=loc_dd_id, multi=True),
                ]),
                visnet1d.layout.inputs_from_dict_list(
                    input_dict_list, style={'padding':10, 'flex':1},
                ),
            ], style={'padding':10, 'width': '20vw'}),
            html.Div([
                html.H1("VisNet1D", style = {'textAlign': 'center'}),
                html.Div([
                    html.Label('X position'),
                    dcc.Slider(
                        min=0,
                        max=1,
                        value=0,
                        vertical=False,
                        id="slider-x",
                    ),
                    html.Div(id="slider-x-label"),
                    dcc.Dropdown(
                        selected_locs, 
                        selected_locs[0], 
                        id=loc_radio_id, 
                    ),
                ]),
                html.Div([
                    dcc.Graph(id='graph-x', config={"editable" : True}),
                ]),
            ], style={'padding':10, 'width': '80vw'}),
        ], style={'display': 'flex', 'flex-direction': 'col'})

        inputs = [Input(item["id"], 'value') for item in input_dict_list]
        input_kwarg_keys = [item["id"] for item in input_dict_list]

        ### Callback functions ###
        @self.app.callback(
            Output('slider-x', 'min'),
            Output('slider-x', 'max'),
            Output('slider-x', 'value'),
            Input(loc_radio_id, 'value'),
        )
        def _set_slider_range(loc_key):
            """Gets the slider range along with the selected slider value"""
            v_start, v_end = get_relative_x(*boundaries[loc_key])
            try:
                v_selected = self.loc_slider_vals[loc_key]
            except KeyError:
                v_selected = (v_end - v_start) / 2
            return v_start, v_end, v_selected

        @self.app.callback(
            Output('slider-x-label', 'children'),
            Input('slider-x', 'value'),
            Input(loc_radio_id, 'value'),
            Input(loc_dd_id, 'value'),
        )
        def _update_slider(x_pos, selected_loc_key, loc_keys):
            """Display the percentage along the location"""
            v_start, v_end = get_relative_x(*boundaries[selected_loc_key])
            self.loc_percentages[selected_loc_key] = (x_pos - v_start) / (v_end - v_start) * 100
            if not isinstance(loc_keys, list):
                loc_keys = [loc_keys]
            rtn_str = [f"{key} = {self.loc_percentages[key]:.0f}%" for key in loc_keys]
            return ", ".join(rtn_str)

        @self.app.callback(
            Output(loc_radio_id, "options"),
            Output(loc_radio_id, "value"),
            Input(loc_dd_id, "value"),
        )
        def _update_radio_options(loc_options):
            """Updates the list of selected locations"""
            if not isinstance(loc_options, list):
                loc_options = [loc_options]
            return loc_options, loc_options[-1]

        @self.app.callback(
            Output('graph-x', 'figure'),
            Input('slider-x', 'value'),
            Input(loc_radio_id, 'value'),
            Input(loc_dd_id, 'value'),
            *inputs,
        )
        def _get_figure_x(x, selected_loc_key, loc_keys, *input_kwarg_values): # pylint: disable=invalid-name
            """Plots the figure with up to date values"""

            # Updates internal variables
            self.update_kwargs(input_kwarg_keys, input_kwarg_values)
            self.x = x
            self.loc_slider_vals[selected_loc_key] = x
            if isinstance(loc_keys, list):
                self.loc_keys = loc_keys
            else:
                self.loc_keys = [loc_keys]

            if self.plot is None:
                return self._plot()
            return self.plot(self)

    def update_kwargs(self, keys, values):
        """Updates the function kwargs dictionary

        Also updates internal property `self.function_kwargs`.

        Args:
            keys (list) : A list of function key word arguments.
            values (list) : A list of associated values.
                Expected to be in the same order as keys.

        Returns:
            function_kwargs (dict) : A dictionary of kwarg pairs.
        """

        function_kwargs = {}
        for i, key in enumerate(keys):
            function_kwargs[key] = values[i]

        self.function_kwargs = function_kwargs

        return function_kwargs

    def run(self, **kwargs):
        """Runs the server

        Key word arguments are directly passed to self.app.run_server()
        """
        return self.app.run_server(**kwargs)

    def _plot(self):
        """ Plots the graph

        Returns:
            fig (plotly figure) : Figure to displayed to the site.
        """

        data = dict()
        for i, key in enumerate(self.loc_keys):
            # pylint: disable=invalid-name
            y, x = self.function(self.loc_slider_vals[key], **self.function_kwargs)
            if i == 0:
                data[self.xlab] = x
            data[key] = y
        df = pd.DataFrame(data)
        fig = df.plot(
                x=self.xlab, 
                y=self.loc_keys, 
                title=self.title, 
                kind='line',
                labels=dict(value=self.ylab, variable="Location"),
                )

        return fig

def get_kwargs(input_dict_list):
    """Gets a dict of kwarg from a list of dictionaries

    Args:
        input_dict_list (list) : A list of dictionaries with the format "id" : "value".

    Returns:
        kwarg_dict (dict) : A dictionary of kwarg pairs.
    """

    kwarg_dict = {}
    for item in input_dict_list:
        key, value = item["id"], item["value"]
        kwarg_dict[key] = value

    return kwarg_dict

def get_relative_x(start, end):
    """Gets the relative distance between a start and an end"""
    return 0, end - start

def get_static_function(output_mat, t, axis=0):
    """Used for static inputs

    Args:
        output_mat (numpy array) : This is the output of some pre-run function.
            The use cases would be explore this output at various locations with
            the need to continually evaluate a function.
        t (numpy array) : The time axis to return which is used for plotting.
        axis (int, optional) : If axis is 0, returns output_mat[x, :].
            Else returns output_mat[:, x].
            Defaults to 0.

    """
    def fn(x, **kwargs):
        if axis == 0:
            return output_mat[int(x), :], t
        return output_mat[:, int(x)], t
    return fn
