import numpy as np
import pandas as pd
import os
import pathlib

import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff

import dash
from dash.dependencies import Input, Output, State

from dash import dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

rand_state = 1000


# numeric columns
def numeric_columns(df):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64', 'datetime64[ns]']
    df_numeric = df.select_dtypes(include=numerics)
    return df_numeric.columns.tolist()


# object columns
def object_columns(df):
    objects = ['object']
    df_object = df.select_dtypes(include=objects)
    return df_object.columns.tolist()


# change column data type to categorical
def cat_features(df, ls):
    for l in ls:
        df[l] = df[l].astype(str)
    return df


# change column data type to float
def num_features(df, ls):
    for l in ls:
        df[l] = df[l].astype(float)
    return df


def number_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    if num > 10000:
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def dict_merge(x, y):
    z = x.copy()  # start with keys and values of x
    z.update(y)  # modifies z with keys and values of y
    return z


app_path = str(pathlib.Path().parent.resolve())

energy = pd.read_csv(os.path.join(app_path, 'energy.csv'))

logo_name = 'Loisaida-Center-Logo-Final-simple.png'

i1 = 'Source EUI (kBtu/ft²)'
i2 = 'Site EUI (kBtu/ft²)'
i3 = 'Fuel Oil Use Total Intensity (kBtu/ft2)'
i4 = 'Natural Gas Use Intensity (kBtu/ft2)'
i5 = 'Diesel #2 Use Intensity (kBtu/ft2)'
i6 = 'District Chilled Water Use Intensity (kBtu/ft2)'
i7 = 'District Steam Use Intensity (kBtu/ft2)'
i8 = 'Green Power - Onsite and Offsite Intensity (kBtu/ft2)'
i9 = 'Electricity Use - Grid Purchase and Generated from Onsite Renewable Systems Intensity (kBtu/ft2)'

in9 = 'Electricity Use Intensity (kBtu/ft2)'

t1 = 'Source Energy Use (kBtu)'
t2 = 'Site Energy Use (kBtu)'
t3 = 'Fuel Oil Use Total (kBtu)'
t4 = 'Natural Gas Use (kBtu)'
t5 = 'Diesel #2 Use (kBtu)'
t6 = 'District Chilled Water Use (kBtu)'
t7 = 'District Steam Use (kBtu)'
t8 = 'Green Power - Onsite and Offsite (kBtu)'
t9 = 'Electricity Use - Grid Purchase and Generated from Onsite Renewable Systems (kBtu)'

tn9 = 'Electricity Use (kBtu)'

e1 = 'Total GHG Emissions Intensity (kgCO2e/ft²)'
e2 = 'Indirect GHG Emissions Intensity (kgCO2e/ft²)'
e3 = 'Direct GHG Emissions Intensity (kgCO2e/ft²)'
e4 = 'Avoided Emissions - Onsite and Offsite Green Power Intensity (Metric Tons CO2e/ft2)'

en4 = 'Avoided Emissions Intensity (Metric Tons CO2e/ft2)'

s1 = 'Total GHG Emissions (Metric Tons CO2e)'
s2 = 'Indirect GHG Emissions (Metric Tons CO2e)'
s3 = 'Direct GHG Emissions (Metric Tons CO2e)'
s4 = 'Avoided Emissions - Onsite and Offsite Green Power (Metric Tons CO2e)'

sn4 = 'Avoided Emissions Intensity (Metric Tons CO2e/ft2)'

emission_dict_intensity = {e1: 'Total GHG Emissions',
                           e2: 'Indirect GHG Emissions',
                           e3: 'Direct GHG Emissions',
                           e4: 'Avoided Emissions'
                           }

emission_dict = {s1: 'Total GHG Emissions',
                 s2: 'Indirect GHG Emissions',
                 s3: 'Direct GHG Emissions',
                 s4: 'Avoided Emissions'
                 }

use_dict = {t1: 'Source Energy',
            t2: 'Site Energy',
            t3: 'Fuel Oil',
            t4: 'Natural Gas',
            t5: "Diesel #2",
            t6: 'Chilled Water',
            t7: 'District Steam',
            t8: 'Green Power',
            t9: 'Electricity'}

use_dict_intensity = {i1: 'Source Energy',
                      i2: 'Site Energy',
                      i3: 'Fuel Oil',
                      i4: 'Natural Gas',
                      i5: "Diesel #2",
                      i6: 'Chilled Water',
                      i7: 'District Steam',
                      i8: 'Green Power',
                      i9: 'Electricity'}

l_head = ['Property Id',
          'Property Name',
          'bbl',
          'Address 1',
          'City',
          'Postcode',
          'Primary Property Type - Self Selected',
          'Borough',
          'Council District',
          'Census Tract',
          'isLowrise',
          'Latitude',
          'Longitude',
          'Year Built',
          'Community Board',
          'NTA']

energy[l_head] = energy[l_head].fillna(0)

df_total = energy.groupby(l_head).sum().reset_index()
df_total['Year Ending'] = 2015
df_mean = energy.groupby(l_head).mean().reset_index()
df_mean['Year Ending'] = 2014

df_energy = pd.concat([energy, df_total, df_mean], ignore_index=True)
df_energy['Community Board'] = df_energy['Community Board'].round().astype(int).astype(str)
df_energy['Census Tract'] = df_energy['Community Board'].astype(int).astype(str)
df_energy['ENERGY STAR Score'].fillna(0, inplace=True)
df_sample = df_energy.sample(frac=0.1, random_state=rand_state)

Cat_list = ['Council District',
            'isLowrise',
            'Community Board',
            'NTA',
            'Borough']
df_use = df_energy[['Property Id', 'Property Name',
                    'Year Ending', 'Latitude', 'Longitude',
                    i1, i2, i3, i4, i5, i6, i7, i8, i9,
                    t1, t2, t3, t4, t5, t6, t7, t8, t9] + Cat_list]
df_use = df_use[~df_use[i1].isna()]

df_emission = df_energy[['Property Id', 'Property Name',
                         'Year Ending', 'Latitude', 'Longitude',
                         e1, e2, e3, e4,
                         s1, s2, s3, s4] + Cat_list]
df_emission = df_emission[~df_emission[s1].isna()]

df_total = df_energy[['Property Id', 'Property Name',
                      'Year Ending',
                      t1, t2, t3, t4, t5, t6, t7, t8, t9,
                      s1, s2, s3, s4] + Cat_list]

df_avg = df_energy[['Property Id', 'Property Name',
                    'Year Ending',
                    i1, i2, i3, i4, i5, i6, i7, i8, i9,
                    e1, e2, e3, e4] + Cat_list]

df_recent = df_energy.sort_values(by='Year Ending', ascending=False).groupby('Property Id').first()

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
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

TAB_STYLE = {
    #     'width': 'inherit',
    #     'border': 'none',
    #     'boxShadow': 'inset 0px -1px 0px 0px lightgrey',
    #     'background': 'white',
    #     'paddingTop': 0,
    #     'paddingBottom': 0,
    #     'height': '42px',
}

LABEL_STYLE = {
    "color": "#000080",
    'font-size': 20,
    'font-weight': 'bold'
}

SELECTED_STYLE = {
    #     'width': 'inherit',
    #     'boxShadow': 'none',
    #     'borderLeft': 'none',
    #     'borderRight': 'none',
    #     'borderTop': 'none',
    #     'borderBottom': '2px #004A96 solid',
    #     'background': 'white',
    #     'paddingTop': 0,
    #     'paddingBottom': 0,
    #     'height': '42px',
}

HR_STYLE = {
    'overflow': 'visible',
    'padding': 0,
    'border': 'none',
    'border-top': 'medium double #333',
    'color': '#333',
    'text-align': 'center',
}

GRAPH_STYLE = {
    "align": "center",
    "justify": "center",
    'horrizontal-align': 'center',
    'height': '300'
}

HEADER_STYLE = {
    'textAlign': 'center',
    'color': '#1E3163',
    "margin-top": "25px",
    'font-weight': 'bold',
}

CONTENT_HEADER_STYLE = {
    #     'background':'#277BC0',
    'text-align': 'left',
    #     'color':'white',
    'font-weight': 'bold',

}

KPICARD_STYLE = {

}

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


def drawrangeslider(id):
    return html.Div(
        style={'color': 'Green', 'font-size': 26},
        children=dcc.RangeSlider(min=2014, max=2020, step=1,
                                 value=[2020], id=id,
                                 marks={
                                     2016: {'label': '2016'},
                                     2017: {'label': '2017'},
                                     2018: {'label': '2018'},
                                     2019: {'label': '2019'},
                                     2020: {'label': '2020'},
                                     2015: {'label': 'Total'},
                                     2014: {'label': 'Mean'}}
                                 )
    )


def drawfigure(id):
    return dcc.Graph(id=id,
                     style=GRAPH_STYLE)


def drawradio(id):
    return html.Div(
        style={'color': '#1E3163', 'font-size': 16},
        children=dcc.RadioItems(
            id=id,
            options=[{
                'label': v,
                'value': v
            } for v in Cat_list],
            value='Community Board',
            labelStyle={'display': 'block'}
        )
    )


# Card
def drawcard(id):
    return html.Div([
        html.H6("", id=id)
    ], style={'textAlign': 'center', 'color': 'blue'})


# Text field
def drawtext(id):
    return html.Div([
        html.H6("", id=id)
    ], style={'textAlign': 'center', 'color': 'dark'})


def drawtable(id):
    l = [i1, i2, i3, i4, i5, i6, i7, i8, i9,
         t1, t2, t3, t4, t5, t6, t7, t8, t9, e1, e2, e3, e4, s1, s2, s3, s4] + l_head
    return html.Div(
        dash.dash_table.DataTable(
            id=id,
            columns=[
                {"name": i, "id": i} for i in sorted(l)
            ],
            page_current=0,
            page_size=10,
            page_action='custom',

            filter_action='custom',
            filter_query='',

            sort_action='custom',
            sort_mode='multi',
            sort_by=[],
            style_table={'minWidth': '100%'},
            style_cell={
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'FFAE6D',
                'color': 'black',
                'whiteSpace': 'normal',
                'height': 'auto',
            }
        ),
        style={'height': 500, 'overflowY': 'scroll'},
        className='six columns',
    )


def drawdropdown(id):
    return dcc.Dropdown(df_energy['Community Board'].unique(), value='103',
                        id=id)


content_header_row = dbc.Row([
    dbc.Col([
        html.Img(
            #             src='data:image/png;base64,{}'.format(logo_name),
            src='images/Loisaida-Center-Logo-Final-simple.png',
            # src='http://loisaida.org/wp-content/uploads/2014/09/Loisaida-Center-Logo-Final-simple.png',
            id="logo",
            style={
                "height": "120px",
                "width": "auto",
                "margin-bottom": "25px",
                "font-size": "30px"
            },
        )
    ],
        md=1
    ),
    dbc.Col([
        html.Br(),
        html.H2(
            'Manhattan Energy Usage and GHG Emission',
            id='title',
            style=HEADER_STYLE,
        ),
    ])

])

overview_first_row = dbc.Row([
    dbc.Col([
        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Year Range',
                            style={
                                'textAlign': 'center',
                                "margin-top": "50px",
                            }),
                ]),
                dbc.CardBody([
                    drawrangeslider(id='year'),
                ])
            ],
                className='mb-3')
        ]),

        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Categories',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),
                dbc.CardBody([
                    html.Div([
                        drawradio(id='categories'),
                    ])
                ])
            ],
                className='mb-3')
        ]),

        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Facts',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),
                dbc.CardBody([
                    html.Div([
                        html.P(id='PropertyName',
                               style={"padding": '0px'}
                               ),
                        html.P(id='addr',
                               style={"padding": '0px'}),
                        html.P(id='lon',
                               style={"padding": '0px'}),
                        html.P(id='lat',
                               style={"padding": '0px'}),
                        html.P(id='score',
                               style={"padding": '0px'}),
                        html.P(id='source',
                               style={"padding": '0px'}),
                        html.P(id='site',
                               style={"padding": '0px'}),
                        html.P(id='ghg',
                               style={"padding": '0px'}),
                        html.P(id='source_intensity',
                               style={"padding": '0px'}),
                        html.P(id='site_intensity',
                               style={"padding": '0px'}),
                        html.P(id='ghg_intensity',
                               style={"padding": '0px'})
                    ])
                ])
            ],
                className='mb-3')
        ]),

    ], md=3),

    dbc.Col([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader([
                            html.H6(
                                "",
                                id='t_property'
                            ),
                            html.H6(
                                "",
                                id='y_property'
                            ),
                        ]),
                        dbc.CardBody(
                            [
                                html.H6(
                                    "",
                                    id='c_property',
                                    className="card-title",
                                ),
                            ])
                    ],
                    className='mb-3',
                    color="#607EAA", inverse=True
                )
            ]),

            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader([
                            html.H6(
                                id='t_usage'
                            ),
                            html.H6(
                                "",
                                id='y_usage'
                            ),
                        ]),
                        dbc.CardBody(
                            [
                                html.H6(
                                    "",
                                    id='c_usage',
                                    className="card-title",
                                ),
                            ])
                    ],
                    className='mb-3',
                    color="#607EAA", inverse=True
                )
            ]),

            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader([
                            html.H6(
                                id='t_emission'
                            ),

                            html.H6(
                                "",
                                id='y_emission'
                            )
                        ]),

                        dbc.CardBody(
                            [
                                html.H6(
                                    "",
                                    id='c_emission',
                                    className="card-title",
                                ),
                            ])
                    ],
                    className='mb-3',
                    color="#607EAA", inverse=True
                )
            ]),
        ]),

        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Energy Usage and Emission Map for Manhattan',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),

                dbc.CardBody([
                    html.Div([
                        drawfigure(id='energymap'),
                    ]),
                ])
            ],
                className='mb-3 mx-3',
                style={}
            )
        ])
    ], md=9)

])

overview_second_row = dbc.Row([
    dbc.Card([
        dbc.CardHeader([
            html.H6(
                "",
                id='plots_usage',
                style={'text-align': 'center'}
            ),
        ]),

        dbc.CardBody([

            dbc.Row([
                # bar - total usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='bar_total_usage')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - total usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_total_usage')
                        ])
                    ])
                ], md=4,
                    className="g-0"),
            ]),

            dbc.Row([
                # bar - average usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='bar_total_usage_intensity')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - average usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_total_usage_intensity')
                        ])
                    ])
                ], md=4,
                    className="g-0")
            ]),

            dbc.Row([
                # bar - total usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_totaltrend_usage')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - total usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='bar_totaltrend_usage')
                        ])
                    ])
                ], md=4,
                    className="g-0"),
            ]),

            dbc.Row([
                # bar - average usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_totaltrend_usage_intensity')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - average usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='bar_totaltrend_usage_intensity')
                        ])
                    ])
                ], md=4,
                    className="g-0")
            ]),

            dbc.Row([
                # bar - total usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_totaltrend_usage_by_cat')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - total usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_totaltrend_usage_by_cat')
                        ])
                    ])
                ], md=4,
                    className="g-0"),
            ]),

            dbc.Row([
                # bar - average usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_totaltrend_usage_intensity_by_cat')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - average usage
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_totaltrend_usage_intensity_by_cat')
                        ])
                    ])
                ], md=4,
                    className="g-0")
            ]),

        ])
    ])
], className='mb-3')

overview_third_row = dbc.Row([
    dbc.Card([
        dbc.CardHeader([
            html.H6(
                "",
                id='plots_emission',
                style={'text-align': 'center'}
            ),
        ]),
        dbc.CardBody([
            dbc.Row([
                # bar - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='bar_total_emission')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_total_emission')
                        ])
                    ])
                ], md=4,
                    className="g-0"),
            ]),

            dbc.Row([
                # bar - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='bar_total_emission_intensity')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_total_emission_intensity')
                        ])
                    ])
                ], md=4,
                    className="g-0")
            ]),

            dbc.Row([
                # bar - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_totaltrend_emission')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='bar_totaltrend_emission')
                        ])
                    ])
                ], md=4,
                    className="g-0"),
            ]),

            dbc.Row([
                # bar - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_totaltrend_emission_intensity')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='bar_totaltrend_emission_intensity')
                        ])
                    ])
                ], md=4,
                    className="g-0")
            ]),

            dbc.Row([
                # bar - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_totaltrend_emission_by_cat')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_totaltrend_emission_by_cat')
                        ])
                    ])
                ], md=4,
                    className="g-0"),
            ]),

            dbc.Row([
                # bar - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_totaltrend_emission_intensity_by_cat')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_totaltrend_emission_intensity_by_cat')
                        ])
                    ])
                ], md=4,
                    className="g-0")
            ]),

        ])
    ])
], className='mb-3')

usage_first_row = dbc.Row([

    dbc.Col([
        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Year Range',
                            style={
                                'textAlign': 'center',
                                "margin-top": "50px",
                            }),
                ]),
                dbc.CardBody([
                    drawrangeslider(id='year_use'),
                ])
            ],
                className='mb-3')
        ]),

        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Categories',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),
                dbc.CardBody([
                    html.Div([
                        drawradio(id='categories_use'),
                    ]),

                    dbc.Card([
                        dbc.CardBody([
                            html.Br(),
                            html.Div(id='categories_dropdown_use',
                                     children=[drawdropdown(id='categories_value_use')]
                                     ),
                        ])
                    ]),
                ])
            ],
                className='mb-3')
        ]),

        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Facts',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),

                dbc.CardBody([
                    html.Div([
                        html.P(id='propname_use',
                               style={"padding": '0px'}),
                        html.P(id='addr_use',
                               style={"padding": '0px'}),
                        html.P(id='lon_use',
                               style={"padding": '0px'}),
                        html.P(id='lat_use',
                               style={"padding": '0px'}),
                        html.P(id='score_use',
                               style={"padding": '0px'}),
                        html.P(id='source_use',
                               style={"padding": '0px'}),
                        html.P(id='site_use',
                               style={"padding": '0px'}),
                        html.P(id='oil_use',
                               style={"padding": '0px'}),
                        html.P(id='gas_use',
                               style={"padding": '0px'}),
                        html.P(id='diesel_use',
                               style={"padding": '0px'}),
                        html.P(id='chilledwater_use',
                               style={"padding": '0px'}),
                        html.P(id='stream_use',
                               style={"padding": '0px'}),
                        html.P(id='greenpower_use',
                               style={"padding": '0px'}),
                        html.P(id='electricity_use',
                               style={"padding": '0px'})
                    ])
                ])
            ])
        ],
            className='mb-3'),
    ], md=3),  # end of control col

    dbc.Col([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader([
                            html.H6(
                                "",
                                id='t_property_use'
                            ),
                            html.H6(
                                "",
                                id='y_property_use'
                            ),
                        ]),
                        dbc.CardBody(
                            [
                                html.H6(
                                    "",
                                    id='c_property_use',
                                    className="card-title",
                                ),
                            ])
                    ],
                    className='mb-3',
                    color="success", inverse=True
                )
            ]),

            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader([
                            html.H6(
                                id='t_total_use'
                            ),
                            html.H6(
                                "",
                                id='y_total_use'
                            ),
                        ]),
                        dbc.CardBody(
                            [
                                html.H6(
                                    "",
                                    id='c_total_use',
                                    className="card-title",
                                ),
                            ])
                    ],
                    className='mb-3',
                    color="success", inverse=True
                )
            ]),

            dbc.Col([
                dbc.Row([
                    dbc.Card(
                        [
                            dbc.CardHeader([
                                html.H6(
                                    id='t_avg_use'
                                ),

                                html.H6(
                                    "",
                                    id='y_avg_use'
                                )
                            ]),

                            dbc.CardBody(
                                [
                                    html.H6(
                                        "",
                                        id='c_avg_use',
                                        className="card-title",
                                    ),
                                ])
                        ],
                        className='mb-3',
                        color="success", inverse=True
                    )
                ]),
            ]),
        ]),

        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Energy Usage Map for Manhattan',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),

                dbc.CardBody([
                    html.Div([
                        drawfigure(id='usemap'),
                    ]),
                ])
            ],
                className='mb-3 mx-3',
                style={}
            )

        ])
    ], md=9)
])

usage_second_row = dbc.Row([
    dbc.Card([
        dbc.CardHeader([
            html.H4(
                "",
                id='plots_use',
                style={'text-align': 'center'}
            ),
        ]),
        dbc.CardBody([
            dbc.Row([
                # bar - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_yeartrend_total_use')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_yeartrend_total_use')
                        ])
                    ])
                ], md=4,
                    className="g-0"),
            ]),

            dbc.Row([
                # bar - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_yeartrend_mean_use')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_yeartrend_mean_use')
                        ])
                    ])
                ], md=4,
                    className="g-0")
            ]),
        ])
    ])
], className='mb-3')

emission_first_row = dbc.Row([

    dbc.Col([
        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Year Range',
                            style={
                                'textAlign': 'center',
                                "margin-top": "50px",
                            }),
                ]),
                dbc.CardBody([
                    drawrangeslider(id='year_emission'),
                ])
            ],
                className='mb-3')
        ]),

        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Categories',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),
                dbc.CardBody([
                    html.Div([
                        drawradio(id='categories_emission'),
                    ]),

                    dbc.Card([
                        dbc.CardBody([
                            html.Br(),
                            html.Div(id='categories_dropdown_emission',
                                     children=[drawdropdown(id='categories_value_emission')]
                                     ),
                        ])
                    ]),
                ])
            ],
                className='mb-3')
        ]),

        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Facts',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),

                dbc.CardBody([
                    html.Div([
                        html.P(id='propname_emission',
                               style={"padding": '0px'}),
                        html.P(id='addr_emission',
                               style={"padding": '0px'}),
                        html.P(id='lon_emission',
                               style={"padding": '0px'}),
                        html.P(id='lat_emission',
                               style={"padding": '0px'}),
                        html.P(id='score_emission',
                               style={"padding": '0px'}),
                        html.P(id='total_emission',
                               style={"padding": '0px'}),
                        html.P(id='indirect_emission',
                               style={"padding": '0px'}),
                        html.P(id='direct_emission',
                               style={"padding": '0px'}),
                        html.P(id='avoided_emission',
                               style={"padding": '0px'})
                    ])
                ])
            ])
        ],
            className='mb-3'),
    ], md=3),  # end of control col

    dbc.Col([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader([
                            html.H6(
                                "",
                                id='t_property_emission'
                            ),
                            html.H6(
                                "",
                                id='y_property_emission'
                            ),
                        ]),
                        dbc.CardBody(
                            [
                                html.H6(
                                    "",
                                    id='c_property_emission',
                                    className="card-title",
                                ),
                            ])
                    ],
                    className='mb-3',
                    color="warning", inverse=True
                )
            ]),

            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader([
                            html.H6(
                                id='t_total_emission'
                            ),
                            html.H6(
                                "",
                                id='y_total_emission'
                            ),
                        ]),
                        dbc.CardBody(
                            [
                                html.H6(
                                    "",
                                    id='c_total_emission',
                                    className="card-title",
                                ),
                            ])
                    ],
                    className='mb-3',
                    color="warning", inverse=True
                )
            ]),

            dbc.Col([
                dbc.Row([
                    dbc.Card(
                        [
                            dbc.CardHeader([
                                html.H6(
                                    id='t_avg_emission'
                                ),

                                html.H6(
                                    "",
                                    id='y_avg_emission'
                                )
                            ]),

                            dbc.CardBody(
                                [
                                    html.H6(
                                        "",
                                        id='c_avg_emission',
                                        className="card-title",
                                    ),
                                ])
                        ],
                        className='mb-3',
                        color="warning", inverse=True
                    )
                ]),
            ]),
        ]),

        dbc.Row([

            dbc.Card([
                dbc.CardHeader([
                    html.H6('Greenhouse Emission Map for Manhattan',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),

                dbc.CardBody([
                    html.Div([
                        drawfigure(id='emissionmap'),
                    ]),
                ])
            ],
                className='mb-3 mx-3',
                style={}
            )

        ])
    ], md=9)
])

emission_second_row = dbc.Row([
    dbc.Card([
        dbc.CardHeader([
            html.H2(
                "",
                id='plots_emission1',
                style={'text-align': 'center'}
            ),
        ]),
        dbc.CardBody([
            dbc.Row([
                # bar - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_yeartrend_total_emission')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - total emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_yeartrend_total_emission')
                        ])
                    ])
                ], md=4,
                    className="g-0"),
            ]),

            dbc.Row([
                # bar - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='line_yeartrend_mean_emission')
                        ])
                    ])
                ], md=8,
                    className="g-0"),

                # sunburst - average emission
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            drawfigure(id='sunburst_yeartrend_mean_emission')
                        ])
                    ])
                ], md=4,
                    className="g-0")
            ]),
        ])
    ])
], className='mb-3')

table_first_row = dbc.Row([
    dbc.Col([
        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Year Range',
                            style={
                                'textAlign': 'center',
                                "margin-top": "50px",
                            }),
                ]),
                dbc.CardBody([
                    drawrangeslider(id='year_table'),
                ])
            ],
                className='mb-3 mx-3')
        ]),

        dbc.Row([
            dbc.Card([
                dbc.CardHeader([
                    html.H6('Categories',
                            style={
                                'textAlign': 'center',
                                "margin-top": "15px",
                            }),
                ]),
                dbc.CardBody([
                    html.Div([
                        drawradio(id='categories_table'),
                    ]),

                    dbc.Card([
                        dbc.CardBody([
                            html.Br(),
                            html.Div(id='categories_dropdown_table',
                                     children=[drawdropdown(id='categories_value_table')]
                                     ),
                        ])
                    ]),
                ])
            ],
                className='mb-3 mx-3')
        ]),

    ], md=3),  # end of control col

    dbc.Col([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4('Manhattan Energy Usage and Green Gas Emission', id='table_title',
                                style={'textAlign': 'center'}),
                        html.Br()
                    ]),
                    dbc.CardBody([
                        drawtable(id='table-paging-with-graph')
                    ])
                ])
            ])
        ])
    ], md=9, align="center"),  # end of card and heatmap col
])

card_overview = dbc.Card([
    dbc.CardHeader([
        html.H4('OVERVIEW')
    ], className="card-header card-header-warning",
        style=CONTENT_HEADER_STYLE),
    dbc.CardBody([
        overview_first_row,
        overview_second_row,
        overview_third_row
    ])
], className='mb-3, mx-5',
    color='white',
    style={'background-color': '#EEF1FF'})

card_usage = dbc.Card([
    dbc.CardHeader([
        html.H4('ENERGY USAGE')
    ], style=CONTENT_HEADER_STYLE),
    dbc.CardBody([
        usage_first_row,
        usage_second_row
    ])
], className='mb-3, mx-5',
    color='white')

card_emission = dbc.Card([
    dbc.CardHeader([
        html.H4('GREENHOUSE GAS EMISSION')
    ], style=CONTENT_HEADER_STYLE),
    dbc.CardBody([
        emission_first_row,
        emission_second_row
    ])
], className='mb-3, mx-5',
    color='white')

card_table = dbc.Card([
    dbc.CardHeader([
        html.H4('TABLES')
    ], style=CONTENT_HEADER_STYLE),
    dbc.CardBody([
        table_first_row
    ])
], className='mb-3, mx-5',
    color='white')

content = html.Div([
    content_header_row,
    card_overview,
    card_usage,
    card_emission,
    card_table
],
    style={"background-color": "#81CACF"}
)

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.MATERIA],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, ''initial-scale=1'}])

# app.config.suppress_callback_exceptions = True
app.title = 'Manhattan Energy Usage and Emission Analysis'

app.layout = html.Div([content])


@app.callback(
    Output('PropertyName', 'children'),
    Output('addr', 'children'),
    Output('lon', 'children'),
    Output('lat', 'children'),
    Output('score', 'children'),
    Output('source', 'children'),
    Output('site', 'children'),
    Output('ghg', 'children'),
    Output('source_intensity', 'children'),
    Output('site_intensity', 'children'),
    Output('ghg_intensity', 'children'),
    [Input('year', 'value'),
     Input('energymap', 'hoverData')])
def upgrade_card(years, hoverData):
    df = df_energy[df_energy['Year Ending'].isin(years)]
    if hoverData is None:
        propname = ''
        addr = ''
        lon = ''
        lat = ''
        score = ''
        source = ''
        site = ''
        ghg = ''
        source_intensity = ''
        site_intensity = ''
        ghg_intensity = ''
    else:
        map_data = hoverData['points'][0]['customdata']
        propId = map_data[0]
        df_map = df[df['Property Id'] == propId]
        propname = df_map['Property Name']
        addr = df_map['Address 1']
        lon = number_format(df_map['Longitude'].iloc[0])
        lat = number_format(df_map['Latitude'].iloc[0])
        score = number_format(df_map['ENERGY STAR Score'].iloc[0])
        source = number_format(df_map[t1].iloc[0])
        site = number_format(df_map[t2].iloc[0])
        ghg = number_format(df_map[s1].iloc[0])
        source_intensity = number_format(df_map[i1].iloc[0])
        site_intensity = number_format(df_map[i2].iloc[0])
        ghg_intensity = number_format(df_map[e1].iloc[0])
    return ['Property Name: ' + propname,
            'Address: ' + addr,
            'Longitude: ' + lon,
            'Latitude: ' + lat,
            'Energy Star Score: ' + score,
            'Source Energy Used (kbTu): ' + source,
            'Site Energy Used (kbTu): ' + site,
            'Green House Gas Emission (Metric Tons CO2e): ' + ghg,
            'Source Energy Intensity (kbTu/ft2): ' + source_intensity,
            'Site Energy Intensity (kbTu/ft2): ' + site_intensity,
            'Green House Gas Emission Intensity (kgCO2e/ft2): ' + ghg_intensity]


@app.callback(
    Output('c_property', 'children'),
    Output('y_property', 'children'),
    Output('t_property', 'children'),
    Output('c_usage', 'children'),
    Output('y_usage', 'children'),
    Output('t_usage', 'children'),
    Output('c_emission', 'children'),
    Output('y_emission', 'children'),
    Output('t_emission', 'children'),
    [Input('year', 'value'),
     Input('categories', 'value')])
def update_cards(years, category):
    df = df_energy[df_energy['Year Ending'].isin(years)]

    year = years[0]
    YearLabel = 'For ' + str(year)
    if year == 2014:
        YearLabel = 'For 2016 - 2020 (Average)'
    elif year == 2015:
        YearLabel = 'For 2016 - 2020 (Total)'
    card1 = str(len(df['Property Id'].unique()))
    text1 = 'Total Properties'

    card2 = number_format(df[t1].sum().round(4))
    text2 = 'Total Source Energy Used (kBtu)'

    card3 = number_format(df[s1].sum().round(4))
    text3 = 'Total GHG Emission (Metric Tons CO2e)'

    return [card1, YearLabel, text1, card2, YearLabel, text2, card3, YearLabel, text3]


@app.callback(
    Output('energymap', 'figure'),
    [Input('year', 'value'),
     Input('categories', 'value')])
def update_map(years, category):
    df = df_energy[df_energy['Year Ending'].isin(years)]
    lat = df[df['Community Board'] == '103']['Latitude'].iloc[0]
    lon = df[df['Community Board'] == '103']['Longitude'].iloc[0]
    fig1 = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        color=category,
        opacity=0.6,
        #         width=600,
        height=700,
        hover_name='Property Id',
        hover_data=['Property Name',
                    'ENERGY STAR Score',
                    'Site EUI (kBtu/ft²)',
                    'Source EUI (kBtu/ft²)',
                    'Total GHG Emissions Intensity (kgCO2e/ft²)'],
        size='ENERGY STAR Score',
        size_max=15,
        custom_data=['Property Id'])

    fig1.update_layout(
        mapbox=dict(
            bearing=0,
            center=dict(
                lat=40.72111,
                lon=-73.98586
            ),
            pitch=0,
            zoom=14))
    fig1.update_layout(mapbox_style="open-street-map")
    fig1.update_layout(showlegend=False)

    return fig1


@app.callback(
    Output('bar_total_usage', 'figure'),
    Output('sunburst_total_usage', 'figure'),
    Output('bar_total_usage_intensity', 'figure'),
    Output('sunburst_total_usage_intensity', 'figure'),

    Output('line_totaltrend_usage', 'figure'),
    Output('bar_totaltrend_usage', 'figure'),
    Output('line_totaltrend_usage_intensity', 'figure'),
    Output('bar_totaltrend_usage_intensity', 'figure'),

    Output('line_totaltrend_usage_by_cat', 'figure'),
    Output('sunburst_totaltrend_usage_by_cat', 'figure'),
    Output('line_totaltrend_usage_intensity_by_cat', 'figure'),
    Output('sunburst_totaltrend_usage_intensity_by_cat', 'figure'),

    Output('bar_total_emission', 'figure'),
    Output('sunburst_total_emission', 'figure'),
    Output('bar_total_emission_intensity', 'figure'),
    Output('sunburst_total_emission_intensity', 'figure'),

    Output('line_totaltrend_emission', 'figure'),
    Output('bar_totaltrend_emission', 'figure'),
    Output('line_totaltrend_emission_intensity', 'figure'),
    Output('bar_totaltrend_emission_intensity', 'figure'),

    Output('line_totaltrend_emission_by_cat', 'figure'),
    Output('sunburst_totaltrend_emission_by_cat', 'figure'),
    Output('line_totaltrend_emission_intensity_by_cat', 'figure'),
    Output('sunburst_totaltrend_emission_intensity_by_cat', 'figure'),

    Output('plots_usage', 'children'),
    Output('plots_emission', 'children'),
    [Input('year', 'value'),
     Input('categories', 'value')])
def update_bar(years, category):
    year = years[0]
    YearLabel = 'for ' + str(year)
    if year == 2014:
        YearLabel = 'for 2016 - 2020 (mean)'
    elif year == 2015:
        YearLabel = 'for 2016 - 2020 (total)'

    h_usage = 'Energy Usage ' + YearLabel
    h_emission = 'Green House Gas Emission ' + YearLabel

    df1 = df_total[df_total['Year Ending'].isin(years)][['Property Id', category, t1, s1]]
    df1 = df1.groupby(category).sum().reset_index()

    fig_totalusage1 = px.bar(df1, y=t1, x=category, color=category,
                             text=t1, height=400,
                             color_discrete_sequence=px.colors.sequential.BuGn_r,
                             title="Total Energy Usage " + YearLabel)
    #     fig1.update_layout(showlegend=False)
    fig_totalusage1.update_xaxes(tickangle=45,
                                 tickmode='array'
                                 )
    fig_totalusage1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig_totalusage1.update_layout(xaxis_showticklabels=False)
    fig_totalusage1.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})

    fig_totalusage2 = px.pie(df1, values=t1, names=category, height=400,
                             color_discrete_sequence=px.colors.sequential.BuGn_r)
    fig_totalusage2.update_layout(showlegend=False)

    fig_totalemission1 = px.bar(df1, y=s1, x=category, color=category,
                                text=s1, height=400,
                                color_discrete_sequence=px.colors.sequential.Oranges_r,
                                title="Total Greenhouse Gas Emission " + YearLabel)
    #     fig3.update_layout(showlegend=False)
    fig_totalemission1.update_xaxes(tickangle=45,
                                    tickmode='array'
                                    )
    fig_totalemission1.update_layout(xaxis_showticklabels=False)
    fig_totalemission1.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    fig_totalemission1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig_totalemission2 = px.pie(df1, values=s1, names=category, height=400,
                                color_discrete_sequence=px.colors.sequential.Oranges_r)
    fig_totalemission2.update_layout(showlegend=False)

    df2 = df_avg[df_avg['Year Ending'].isin(years)][['Property Id', category, i1, e1]]
    df2 = df2.groupby(category).mean().reset_index()

    fig_avgusage1 = px.bar(df2, y=i1, x=category, color=category,
                           text=i1, height=400,
                           color_discrete_sequence=px.colors.sequential.BuGn_r,
                           title="Property Average Energy Usage " + YearLabel)
    #     fig1.update_layout(showlegend=False)
    fig_avgusage1.update_xaxes(tickangle=45,
                               tickmode='array'
                               )
    fig_avgusage1.update_layout(xaxis_showticklabels=False)
    fig_avgusage1.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    fig_avgusage1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig_avgusage2 = px.pie(df2, values=i1, names=category, height=400,
                           color_discrete_sequence=px.colors.sequential.BuGn_r)
    fig_avgusage2.update_layout(showlegend=False)

    fig_avgemission1 = px.bar(df2, y=e1, x=category, color=category,
                              text=e1, height=400,
                              color_discrete_sequence=px.colors.sequential.Oranges_r,
                              title="Property Average Greenhouse Gas Emission " + YearLabel)
    #     fig3.update_layout(showlegend=False)
    fig_avgemission1.update_xaxes(tickangle=45,
                                  tickmode='array'
                                  )
    fig_avgemission1.update_layout(xaxis_showticklabels=False)
    fig_avgemission1.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
    fig_avgemission1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig_avgemission2 = px.pie(df2, values=e1, names=category, height=400,
                              color_discrete_sequence=px.colors.sequential.Oranges_r)
    fig_avgemission2.update_layout(showlegend=False)

    df_trend1 = df_total[df_total['Year Ending'].isin([2016, 2017, 2018, 2019, 2020])]
    df_trend2 = df_avg[df_avg['Year Ending'].isin([2016, 2017, 2018, 2019, 2020])]
    df_trend_total1 = df_trend1.groupby('Year Ending').sum().reset_index()
    fig_totaltrendusage1 = px.line(df_trend_total1, x='Year Ending', y=t1, markers=True,
                                   title='Total Energy Usage Trend for 2016 - 2020', height=400, )
    fig_totaltrendusage1.update_xaxes(tickmode='array',
                                      tickvals=[2016, 2017, 2018, 2019, 2020],
                                      #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                                      )
    fig_totaltrendusage1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_totaltrendusage1.update_traces(line_color='green', line_width=3)

    df_trend_total1['Year Ending'] = df_trend_total1['Year Ending'].round().astype(int).astype(str)
    fig_totaltrendusage2 = px.bar(df_trend_total1, y=t1, height=400,
                                  x='Year Ending',
                                  color='Year Ending',
                                  color_discrete_sequence=px.colors.sequential.BuGn_r,
                                  text=t1)
    #     fig3.update_layout(showlegend=False)
    fig_totaltrendusage2.update_xaxes(tickangle=45,
                                      tickmode='array'
                                      )

    fig_totaltrendemission1 = px.line(df_trend_total1, x='Year Ending', y=s1, markers=True,
                                      title='Total Greenhouse Gas Emission Trend for 2016 - 2020', height=400, )
    fig_totaltrendemission1.update_xaxes(tickmode='array',
                                         #                  tickvals = [2016, 2017, 2018, 2019, 2020],
                                         #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                                         )
    fig_totaltrendemission1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_totaltrendemission1.update_traces(line_color='orange', line_width=3)

    fig_totaltrendemission2 = px.bar(df_trend_total1, y=s1, x='Year Ending',
                                     color='Year Ending',
                                     color_discrete_sequence=px.colors.sequential.Oranges_r,
                                     text=s1, height=400)
    #     fig3.update_layout(showlegend=False)
    fig_totaltrendemission2.update_xaxes(tickangle=45,
                                         tickmode='array'
                                         )
    fig_totaltrendemission2.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    df_trend_total2 = df_trend1.groupby([category, 'Year Ending']).sum().reset_index()
    fig_totaltrendusage3 = px.line(df_trend_total2, x='Year Ending', y=t1,
                                   color=category, markers=True, height=400,
                                   color_discrete_sequence=px.colors.sequential.Viridis_r,
                                   title='Total Energy Usage Trend by ' + category + ' for 2016 - 2020')
    fig_totaltrendusage3.update_xaxes(tickmode='array',
                                      tickvals=[2016, 2017, 2018, 2019, 2020],
                                      #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                                      )
    fig_totaltrendusage3.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_totaltrendusage3.update_traces(line_width=2)

    fig_totaltrendusage4 = px.sunburst(df_trend_total2, path=['Year Ending', category], values=t1,
                                       color=t1, color_continuous_scale=px.colors.sequential.BuGn_r, height=400)
    fig_totaltrendusage4.update_layout(showlegend=False)
    fig_totaltrendusage4.update_layout(coloraxis_colorbar_title='Source Energy Use <br> (kBtu)',
                                       coloraxis_colorbar_tickfont_size=8)

    fig_totaltrendemission3 = px.line(df_trend_total2, x='Year Ending', y=s1,
                                      color=category, markers=True, height=400,
                                      color_discrete_sequence=px.colors.sequential.Sunsetdark_r,
                                      title='Total Greenhouse Gas Emission Trend by ' + category + ' for 2016 - 2020')
    fig_totaltrendemission3.update_xaxes(tickmode='array',
                                         tickvals=[2016, 2017, 2018, 2019, 2020],
                                         #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                                         )
    fig_totaltrendemission3.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_totaltrendemission3.update_traces(line_width=2)

    fig_totaltrendemission4 = px.sunburst(df_trend_total2, path=['Year Ending', category], values=s1,
                                          color=s1, color_continuous_scale=px.colors.sequential.Oranges_r, height=400, )
    fig_totaltrendemission4.update_layout(showlegend=False)
    fig_totaltrendemission4.update_layout(coloraxis_colorbar_title='Total GHG Emissions <br> (Metric Tons CO2e)',
                                          coloraxis_colorbar_tickfont_size=8)

    df_trend1 = df_total[df_total['Year Ending'].isin([2016, 2017, 2018, 2019, 2020])]
    df_trend2 = df_avg[df_avg['Year Ending'].isin([2016, 2017, 2018, 2019, 2020])]

    df_trend_avg1 = df_trend2.groupby('Year Ending').mean().reset_index()
    df_trend_avg1['Year Ending'] = df_trend_avg1['Year Ending'].round().astype(int).astype(str)
    fig_avgtrendusage1 = px.line(df_trend_avg1, x='Year Ending', y=i1, markers=True, height=400,
                                 title='Property Average Energy Usage Trend for 2016 - 2020')
    #     fig_avgtrendusage1.update_xaxes(tickmode = 'array',
    #                  tickvals = [2016, 2017, 2018, 2019, 2020],
    #                  ticktext= [2016, 2017, 2018, 2019, 2020]
    #                      )
    fig_avgtrendusage1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_avgtrendusage1.update_traces(line_color='green', line_width=3)

    fig_avgtrendusage2 = px.bar(df_trend_avg1, y=i1, x='Year Ending',
                                color='Year Ending',
                                color_discrete_sequence=px.colors.sequential.BuGn_r,
                                text=i1, height=400)
    #     fig3.update_layout(showlegend=False)
    fig_avgtrendusage2.update_xaxes(tickangle=45,
                                    tickmode='array'
                                    )

    fig_avgtrendemission1 = px.line(df_trend_avg1, x='Year Ending', y=e1, markers=True, height=400,
                                    title='Property Average Greenhouse Gas Emission Trend for 2016 - 2020')
    fig_avgtrendemission1.update_xaxes(tickmode='array',
                                       #                  tickvals = [2016, 2017, 2018, 2019, 2020],
                                       #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                                       )
    fig_avgtrendemission1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_avgtrendemission1.update_traces(line_color='orange', line_width=3)

    fig_avgtrendemission2 = px.bar(df_trend_avg1, y=e1, x='Year Ending',
                                   color='Year Ending',
                                   color_discrete_sequence=px.colors.sequential.Oranges_r,
                                   text=e1, height=400)
    #     fig3.update_layout(showlegend=False)
    fig_avgtrendemission2.update_xaxes(tickangle=45,
                                       tickmode='array'
                                       )

    df_trend_avg2 = df_trend2.groupby([category, 'Year Ending']).mean().reset_index()
    fig_avgtrendusage3 = px.line(df_trend_avg2, x='Year Ending', y=i1, color=category, markers=True,
                                 color_discrete_sequence=px.colors.sequential.Viridis_r, height=400,
                                 title='Property Average Energy Use Intensity Trend by ' + category + ' for 2016 - 2020')
    fig_avgtrendusage3.update_xaxes(tickmode='array',
                                    tickvals=[2016, 2017, 2018, 2019, 2020],
                                    #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                                    )
    fig_avgtrendusage3.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_avgtrendusage3.update_traces(line_width=2)

    fig_avgtrendusage4 = px.sunburst(df_trend_avg2, path=['Year Ending', category], values=i1,
                                     color=i1, color_continuous_scale=px.colors.sequential.BuGn_r, height=400, )
    fig_avgtrendusage4.update_layout(showlegend=False)
    fig_avgtrendusage4.update_layout(coloraxis_colorbar_title='Source EUI <br> (kBtu/ft²)',
                                     coloraxis_colorbar_tickfont_size=8)

    fig_avgtrendemission3 = px.line(df_trend_avg2, x='Year Ending', y=e1,
                                    color=category, markers=True, height=400,
                                    color_discrete_sequence=px.colors.sequential.Sunsetdark_r,
                                    title='Property Average GHG Emission Intensity Trend by ' + category + ' for 2016 - 2020')
    fig_avgtrendemission3.update_xaxes(tickmode='array',
                                       tickvals=[2016, 2017, 2018, 2019, 2020],
                                       #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                                       )
    fig_avgtrendemission3.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig_avgtrendemission3.update_traces(line_width=3)

    fig_avgtrendemission4 = px.sunburst(df_trend_avg2, path=['Year Ending', category], values=e1,
                                        color=e1, color_continuous_scale=px.colors.sequential.Oranges_r, height=400, )
    fig_avgtrendemission4.update_layout(showlegend=False)
    fig_avgtrendemission4.update_layout(coloraxis_colorbar_title='Total GHG <br> Emissions Intensity <br> (kgCO2e/ft²)',
                                        coloraxis_colorbar_tickfont_size=8)

    return [fig_totalusage1, fig_totalusage2, fig_avgusage1, fig_avgusage2,
            fig_totaltrendusage1, fig_totaltrendusage2, fig_avgtrendusage1, fig_avgtrendusage2,
            fig_totaltrendusage3, fig_totaltrendusage4, fig_avgtrendusage3, fig_avgtrendusage4,
            fig_totalemission1, fig_totalemission2, fig_avgemission1, fig_avgemission2,
            fig_totaltrendemission1, fig_totaltrendemission2, fig_avgtrendemission1, fig_avgtrendemission2,
            fig_totaltrendemission3, fig_totaltrendemission4, fig_avgtrendemission3, fig_avgtrendemission4,
            h_usage, h_emission]


#######################################
####    Energy Usage Tab #############
#######################################


@app.callback(
    Output('categories_dropdown_use', 'children'),
    [Input('categories_use', 'value')])
def update_dropdown_category(category):
    value = df_energy[category].unique()[0]
    if category == 'Community Board':
        value = '103'
    elif category == 'Borough':
        value = 'MANHATTAN'
    return dcc.Dropdown(df_energy[category].unique(), value=value,
                        id='categories_value_use')


@app.callback(
    Output('t_property_use', 'children'),
    Output('y_property_use', 'children'),
    Output('c_property_use', 'children'),
    Output('t_total_use', 'children'),
    Output('y_total_use', 'children'),
    Output('c_total_use', 'children'),
    Output('t_avg_use', 'children'),
    Output('y_avg_use', 'children'),
    Output('c_avg_use', 'children'),
    [Input('year_use', 'value'),
     Input('categories_use', 'value'),
     Input('categories_value_use', 'value')])
def update_cards(years, category, cat_value):
    df = df_use[df_use['Year Ending'].isin(years)]
    df = df[df[category] == cat_value]

    year = years[0]
    YearLabel = 'for ' + str(year)
    if year == 2014:
        YearLabel = 'for 2016 - 2020 (mean)'
    elif year == 2015:
        YearLabel = 'for 2016 - 2020 (total)'

    t_property_use = 'Total Properties'
    y_use = YearLabel + ' (' + category + ' : ' + str(cat_value) + ')'
    c_property_use = number_format(df[t1].count())

    t_total_use = 'Total Energy Usage' + ' (kBtu)'
    c_total_use = number_format(round(df[t1].sum(), 4))

    t_avg_use = 'Average Energy Usage' + ' (kBtu/ft2)'
    c_avg_use = number_format(round(df[i1].mean(), 4))

    return [t_property_use, y_use, c_property_use,
            t_total_use, y_use, c_total_use,
            t_avg_use, y_use, c_avg_use]


@app.callback(
    Output('usemap', 'figure'),
    [Input('year_use', 'value'),
     Input('categories_use', 'value'),
     Input('categories_value_use', 'value')])
def update_map(years, category, cat_value):
    df = df_use[df_use['Year Ending'].isin(years)]
    df = df[df[category] == cat_value]
    lat = df['Latitude'].iloc[0]
    lon = df['Longitude'].iloc[0]
    df['dummy_column_for_size'] = 1.

    fig1 = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        color=t1,
        opacity=0.6,
        #         width=1000,
        height=1000,
        hover_name='Property Id',
        hover_data=['Property Name', t1, t2, i1, i2],
        size='dummy_column_for_size',
        size_max=15,
        custom_data=['Property Id'])

    fig1.update_layout(
        mapbox=dict(
            bearing=0,
            center=dict(
                lat=lat,
                lon=lon,
            ),
            pitch=0,
            zoom=15))
    fig1.update_layout(mapbox_style="open-street-map")
    fig1.update_layout(showlegend=False)
    fig1.update_layout(
        title={
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig1


@app.callback(
    Output('line_yeartrend_total_use', 'figure'),
    Output('sunburst_yeartrend_total_use', 'figure'),
    Output('line_yeartrend_mean_use', 'figure'),
    Output('sunburst_yeartrend_mean_use', 'figure'),
    [Input('year_use', 'value'),
     Input('categories_use', 'value'),
     Input('categories_value_use', 'value')])
def update_bar(years, category, cat_value):
    year = years[0]
    YearLabel = 'for ' + str(year)
    if year == 2014:
        YearLabel = 'for 2016 - 2020 (mean)'
    elif year == 2015:
        YearLabel = 'for 2016 - 2020 (total)'

    df_trend = df_use[df_use[category] == cat_value]
    df_trend = df_trend[df_trend['Year Ending'].isin([2016, 2017, 2018, 2019, 2020])]

    df_trend1 = df_trend.groupby('Year Ending').sum().reset_index()
    df_trend1 = pd.melt(df_trend1, id_vars=['Year Ending'],
                        value_vars=[t1, t2, t3, t4, t5, t6, t7, t8, t9],
                        var_name='Source Type',
                        value_name='Value (kBtu)')
    df_trend1['Value (kBtu)'] = np.where(df_trend1['Value (kBtu)'] == 0,
                                         0.00001,
                                         df_trend1['Value (kBtu)'])
    fig1 = px.line(df_trend1, x='Year Ending', y='Value (kBtu)', markers=True,
                   color='Source Type', height=400,
                   title='Total Energy Usage Trend <br> for 2016 - 2020 for ' + category + ' : ' + str(cat_value),
                   color_discrete_sequence=px.colors.sequential.Viridis_r)
    fig1.update_xaxes(tickmode='array',
                      tickvals=[2016, 2017, 2018, 2019, 2020],
                      #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                      )
    fig1.update_layout(coloraxis_colorbar_title='Source Energy Use <br> (kBtu)',
                       coloraxis_colorbar_tickfont_size=8)
    fig1.for_each_trace(lambda t: t.update(name=use_dict[t.name],
                                           legendgroup=use_dict[t.name],
                                           hovertemplate=t.hovertemplate.replace(t.name, use_dict[t.name])
                                           )
                        )
    fig1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig2 = px.sunburst(df_trend1, path=['Year Ending', 'Source Type'], values='Value (kBtu)', color='Value (kBtu)',
                       color_continuous_scale=px.colors.sequential.BuGn_r, height=400, )
    fig2.update_layout(coloraxis_colorbar_title='Source Energy Use <br> (kBtu)',
                       coloraxis_colorbar_tickfont_size=8)
    fig2.update_layout(showlegend=False)

    df_trend2 = df_trend.groupby('Year Ending').mean().reset_index()
    df_trend2 = pd.melt(df_trend2, id_vars=['Year Ending'],
                        value_vars=[i1, i2, i3, i4, i5, i6, i7, i8, i9],
                        var_name='Source Type',
                        value_name='Value (kBtu/ft2)')

    df_trend2['Value (kBtu/ft2)'] = np.where(df_trend2['Value (kBtu/ft2)'] == 0,
                                             0.00001,
                                             df_trend2['Value (kBtu/ft2)'])

    fig3 = px.line(df_trend2, x='Year Ending', y='Value (kBtu/ft2)', markers=True,
                   color='Source Type', height=400,
                   title='Property Average Energy Use Intensity Trend <br> for 2016 - 2020 for ' + category + ' : ' + str(
                       cat_value),
                   color_discrete_sequence=px.colors.sequential.Viridis_r)
    fig3.update_xaxes(tickmode='array',
                      tickvals=[2016, 2017, 2018, 2019, 2020],
                      #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                      )
    fig3.for_each_trace(lambda t: t.update(name=use_dict_intensity[t.name],
                                           legendgroup=use_dict_intensity[t.name],
                                           hovertemplate=t.hovertemplate.replace(t.name, use_dict_intensity[t.name])
                                           )
                        )
    fig3.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig4 = px.sunburst(df_trend2, path=['Year Ending', 'Source Type'], values='Value (kBtu/ft2)',
                       color='Value (kBtu/ft2)',
                       color_continuous_scale=px.colors.sequential.BuGn_r, height=400, )
    fig4.update_layout(coloraxis_colorbar_title='Source Energy <br> Use Intensity <br> (kBtu)',
                       coloraxis_colorbar_tickfont_size=8)
    fig4.update_layout(showlegend=False)

    return [fig1, fig2, fig3, fig4]


@app.callback(
    Output('propname_use', 'children'),
    Output('addr_use', 'children'),
    Output('lon_use', 'children'),
    Output('lat_use', 'children'),
    Output('score_use', 'children'),
    Output('source_use', 'children'),
    Output('site_use', 'children'),
    Output('oil_use', 'children'),
    Output('gas_use', 'children'),
    Output('diesel_use', 'children'),
    Output('chilledwater_use', 'children'),
    Output('stream_use', 'children'),
    Output('greenpower_use', 'children'),
    Output('electricity_use', 'children'),
    [Input('year', 'value'),
     Input('usemap', 'hoverData')])
def upgrade_card(years, hoverData):
    df = df_energy[df_energy['Year Ending'].isin(years)]
    if hoverData is None:
        propname_use = ''
        addr_use = ''
        lon_use = ''
        lat_use = ''
        score_use = ''
        source_use = ''
        site_use = ''
        oil_use = ''
        gas_use = ''
        diesel_use = ''
        chilledwater_use = ''
        stream_use = ''
        greenpower_use = ''
        electricity_use = ''
    else:
        map_data = hoverData['points'][0]['customdata']
        propId = map_data[0]
        df_map = df[df['Property Id'] == propId]
        propname_use = df_map['Property Name']
        addr_use = df_map['Address 1']
        lon_use = number_format(df_map['Longitude'].iloc[0])
        lat_use = number_format(df_map['Latitude'].iloc[0])
        score_use = number_format(df_map['ENERGY STAR Score'].iloc[0])
        source_use = number_format(df_map[t1].iloc[0]) + ' KBTU (' + number_format(df_map[i1].iloc[0]) + ' KBTU/FT2)'
        site_use = number_format(df_map[t2].iloc[0]) + ' KBTU (' + number_format(df_map[i2].iloc[0]) + ' KBTU/FT2)'
        oil_use = number_format(df_map[t3].iloc[0]) + ' KBTU (' + number_format(df_map[i3].iloc[0]) + ' KBTU/FT2)'
        gas_use = number_format(df_map[t4].iloc[0]) + ' KBTU (' + number_format(df_map[i4].iloc[0]) + ' KBTU/FT2)'
        diesel_use = number_format(df_map[t5].iloc[0]) + ' KBTU (' + number_format(df_map[i5].iloc[0]) + ' KBTU/FT2)'
        chilledwater_use = number_format(df_map[t6].iloc[0]) + ' KBTU (' + number_format(
            df_map[i6].iloc[0]) + ' KBTU/FT2)'
        stream_use = number_format(df_map[t7].iloc[0]) + ' KBTU (' + number_format(df_map[i7].iloc[0]) + ' KBTU/FT2)'
        greenpower_use = number_format(df_map[t8].iloc[0]) + ' KBTU (' + number_format(
            df_map[i8].iloc[0]) + ' KBTU/FT2)'
        electricity_use = number_format(df_map[t9].iloc[0]) + ' KBTU (' + number_format(
            df_map[i9].iloc[0]) + ' KBTU/FT2)'

    return ['Property Name: ' + propname_use,
            'Address: ' + addr_use,
            'Longitude: ' + lon_use,
            'Latitude: ' + lat_use,
            'Energy Star Score: ' + score_use,
            use_dict[t1] + ": " + source_use,
            use_dict[t2] + ": " + site_use,
            use_dict[t3] + ": " + oil_use,
            use_dict[t4] + ": " + gas_use,
            use_dict[t5] + ": " + diesel_use,
            use_dict[t6] + ": " + chilledwater_use,
            use_dict[t7] + ": " + stream_use,
            use_dict[t8] + ": " + greenpower_use,
            use_dict[t9] + ": " + electricity_use]


#################################
##### Greenhouse Gas Emission
#################################


@app.callback(
    Output('categories_dropdown_emission', 'children'),
    [Input('categories_emission', 'value')])
def update_dropdown_category(category):
    value = df_energy[category].unique()[0]
    if category == 'Community Board':
        value = '103'
    elif category == 'Borough':
        value = 'MANHATTAN'
    return dcc.Dropdown(df_energy[category].unique(), value=value,
                        id='categories_value_emission')


@app.callback(
    Output('t_property_emission', 'children'),
    Output('y_property_emission', 'children'),
    Output('c_property_emission', 'children'),
    Output('t_total_emission', 'children'),
    Output('y_total_emission', 'children'),
    Output('c_total_emission', 'children'),
    Output('t_avg_emission', 'children'),
    Output('y_avg_emission', 'children'),
    Output('c_avg_emission', 'children'),
    [Input('year_emission', 'value'),
     Input('categories_emission', 'value'),
     Input('categories_value_emission', 'value')])
def update_cards(years, category, cat_value):
    df = df_emission[df_emission['Year Ending'].isin(years)]
    df = df[df[category] == cat_value]

    year = years[0]
    YearLabel = 'for ' + str(year)
    if year == 2014:
        YearLabel = 'for 2016 - 2020 (mean)'
    elif year == 2015:
        YearLabel = 'for 2016 - 2020 (total)'

    t_property_emission = 'Total Properties'
    y_emission = YearLabel + ' (' + category + ' : ' + str(cat_value) + ')'
    c_property_emission = number_format(df[s1].count())

    t_total_emission = 'Total GHG Emission' + ' (Metric Tons CO2e)'
    c_total_emission = number_format(round(df[s1].sum(), 4))

    t_avg_emission = 'Total GHG Emission' + ' (kgCO2e/ft²)'
    c_avg_emission = number_format(round(df[e1].mean(), 4))

    return [t_property_emission, y_emission, c_property_emission,
            t_total_emission, y_emission, c_total_emission,
            t_avg_emission, y_emission, c_avg_emission]


@app.callback(
    Output('emissionmap', 'figure'),
    [Input('year_emission', 'value'),
     Input('categories_emission', 'value'),
     Input('categories_value_emission', 'value')])
def update_map(years, category, cat_value):
    df = df_emission[df_emission['Year Ending'].isin(years)]
    df = df[df[category] == cat_value]
    lat = df['Latitude'].iloc[0]
    lon = df['Longitude'].iloc[0]
    df['dummy_column_for_size'] = 1.

    fig1 = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        color=s1,
        opacity=0.6,
        #         width=1000,
        height=900,
        hover_name='Property Id',
        hover_data=['Property Name', s1, s2, s3, s4, e1, e2, e3, e4],
        size='dummy_column_for_size',
        size_max=15,
        custom_data=['Property Id'])

    fig1.update_layout(
        mapbox=dict(
            bearing=0,
            center=dict(
                lat=lat,
                lon=lon,
            ),
            pitch=0,
            zoom=15))
    fig1.update_layout(mapbox_style="open-street-map")
    fig1.update_layout(showlegend=False)
    fig1.update_layout(coloraxis_colorbar_title='Total GHG Emission <br> (Metric Tons CO2e)',
                       coloraxis_colorbar_tickfont_size=8)
    fig1.update_layout(
        title={
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig1


@app.callback(
    Output('line_yeartrend_total_emission', 'figure'),
    Output('sunburst_yeartrend_total_emission', 'figure'),
    Output('line_yeartrend_mean_emission', 'figure'),
    Output('sunburst_yeartrend_mean_emission', 'figure'),
    [Input('year_emission', 'value'),
     Input('categories_emission', 'value'),
     Input('categories_value_emission', 'value')])
def update_bar(years, category, cat_value):
    year = years[0]
    YearLabel = 'for ' + str(year)
    if year == 2014:
        YearLabel = 'for 2016 - 2020 (mean)'
    elif year == 2015:
        YearLabel = 'for 2016 - 2020 (total)'

    df_trend = df_emission[df_emission[category] == cat_value]
    df_trend = df_trend[df_trend['Year Ending'].isin([2016, 2017, 2018, 2019, 2020])]

    df_trend1 = df_trend.groupby('Year Ending').sum().reset_index()
    df_trend1 = pd.melt(df_trend1, id_vars=['Year Ending'],
                        value_vars=[s1, s2, s3, s4],
                        var_name='Source Type',
                        value_name='Value (Metric Tons CO2e)')
    df_trend1['Value (Metric Tons CO2e)'] = np.where(df_trend1['Value (Metric Tons CO2e)'] == 0,
                                                     0.00001,
                                                     df_trend1['Value (Metric Tons CO2e)'])
    fig1 = px.line(df_trend1, x='Year Ending', y='Value (Metric Tons CO2e)', markers=True,
                   color='Source Type', height=400,
                   title='Total Greenhouse Gas Emission Trend <br> for 2016 - 2020 for ' + str(cat_value),
                   color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
    fig1.update_xaxes(tickmode='array',
                      tickvals=[2016, 2017, 2018, 2019, 2020],
                      #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                      )
    fig1.for_each_trace(lambda t: t.update(name=emission_dict[t.name],
                                           legendgroup=emission_dict[t.name],
                                           hovertemplate=t.hovertemplate.replace(t.name, emission_dict[t.name])
                                           )
                        )
    fig1.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig2 = px.sunburst(df_trend1, path=['Year Ending', 'Source Type'], values='Value (Metric Tons CO2e)',
                       color='Value (Metric Tons CO2e)',
                       color_continuous_scale=px.colors.sequential.Oranges_r, height=400, )
    fig2.update_layout(coloraxis_colorbar_title='Total GHG Emission <br> (Metric Tons CO2e)',
                       coloraxis_colorbar_tickfont_size=8)
    fig2.update_layout(showlegend=False)

    df_trend2 = df_trend.groupby('Year Ending').mean().reset_index()
    df_trend2 = pd.melt(df_trend2, id_vars=['Year Ending'],
                        value_vars=[e1, e2, e3, e4],
                        var_name='Source Type',
                        value_name='Value (kgCO2e/ft²)')

    df_trend2['Value (kBtu/ft2)'] = np.where(df_trend2['Value (kgCO2e/ft²)'] == 0,
                                             0.00001,
                                             df_trend2['Value (kgCO2e/ft²)'])

    fig3 = px.line(df_trend2, x='Year Ending', y='Value (kgCO2e/ft²)', markers=True,
                   color='Source Type', height=400,
                   title='Property Average Energy emission Intensity Trend <br> for 2016 - 2020 for ' + category + ' : ' + str(
                       cat_value),
                   color_discrete_sequence=px.colors.sequential.Sunsetdark_r)
    fig3.update_xaxes(tickmode='array',
                      tickvals=[2016, 2017, 2018, 2019, 2020],
                      #                  ticktext= [2016, 2017, 2018, 2019, 2020]
                      )
    fig3.for_each_trace(lambda t: t.update(name=emission_dict_intensity[t.name],
                                           legendgroup=emission_dict_intensity[t.name],
                                           hovertemplate=t.hovertemplate.replace(t.name,
                                                                                 emission_dict_intensity[t.name])
                                           )
                        )
    fig3.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig4 = px.sunburst(df_trend2, path=['Year Ending', 'Source Type'], values='Value (kgCO2e/ft²)',
                       color='Value (kgCO2e/ft²)',
                       color_continuous_scale=px.colors.sequential.Oranges_r, height=400, )
    fig4.update_layout(coloraxis_colorbar_title='Total GHG <br> Emission Intensity <br> (kgCO2e/ft²)',
                       coloraxis_colorbar_tickfont_size=8)
    fig4.update_layout(showlegend=False)

    return [fig1, fig2, fig3, fig4]


@app.callback(
    Output('propname_emission', 'children'),
    Output('addr_emission', 'children'),
    Output('lon_emission', 'children'),
    Output('lat_emission', 'children'),
    Output('score_emission', 'children'),
    Output('total_emission', 'children'),
    Output('indirect_emission', 'children'),
    Output('direct_emission', 'children'),
    Output('avoided_emission', 'children'),
    [Input('year_emission', 'value'),
     Input('emissionmap', 'hoverData')])
def upgrade_card(years, hoverData):
    df = df_energy[df_energy['Year Ending'].isin(years)]
    if hoverData is None:
        propname_emission = ''
        addr_emission = ''
        lon_emission = ''
        lat_emission = ''
        score_emission = ''
        total_emission = ''
        indirect_emission = ''
        direct_emission = ''
        avoided_emission = ''
    else:
        map_data = hoverData['points'][0]['customdata']
        propId = map_data[0]
        df_map = df[df['Property Id'] == propId]
        propname_emission = df_map['Property Name']
        addr_emission = df_map['Address 1']
        lon_emission = number_format(df_map['Longitude'].iloc[0])
        lat_emission = number_format(df_map['Latitude'].iloc[0])
        score_emission = number_format(df_map['ENERGY STAR Score'].iloc[0])
        total_emission = number_format(df_map[s1].iloc[0]) + ' Metric Tons CO2e (' + number_format(
            df_map[e1].iloc[0]) + ' kgCO2e/ft²)'
        indirect_emission = number_format(df_map[s2].iloc[0]) + ' Metric Tons CO2e (' + number_format(
            df_map[e2].iloc[0]) + ' kgCO2e/ft²)'
        direct_emission = number_format(df_map[s3].iloc[0]) + ' Metric Tons CO2e (' + number_format(
            df_map[e3].iloc[0]) + ' kgCO2e/ft²)'
        avoided_emission = number_format(df_map[s4].iloc[0]) + ' Metric Tons CO2e (' + number_format(
            df_map[e4].iloc[0]) + ' kgCO2e/ft²)'

    return ['Property Name: ' + propname_emission,
            'Address: ' + addr_emission,
            'Longitude: ' + lon_emission,
            'Latitude: ' + lat_emission,
            'Energy Star Score: ' + score_emission,
            emission_dict[s1] + ": " + total_emission,
            emission_dict[s2] + ": " + indirect_emission,
            emission_dict[s3] + ": " + direct_emission,
            emission_dict[s4] + ": " + avoided_emission]


#########################################
#### Table ##############
#########################################

@app.callback(
    Output('categories_dropdown_table', 'children'),
    [Input('categories_table', 'value')])
def update_dropdown_category(category):
    value = df_energy[category].unique()[0]
    if category == 'Community Board':
        value = '103'
    elif category == 'Borough':
        value = 'MANHATTAN'
    return dcc.Dropdown(df_energy[category].unique(), value=value,
                        id='categories_value_table')


@app.callback(
    Output('table_title', 'children'),
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('table-paging-with-graph', "sort_by"),
     Input('table-paging-with-graph', "filter_query"),
     Input('year_table', 'value'),
     Input('categories_table', 'value'),
     Input('categories_value_table', 'value')]
)
def update_table(page_current, page_size, sort_by, filter,
                 years, category, cat_value):
    year = years[0]
    YearLabel = ' for ' + str(year)
    if year == 2014:
        YearLabel = ' for 2016 - 2020 (mean)'
    elif year == 2015:
        YearLabel = ' for 2016 - 2020 (total)'

    table_title = 'Manhattan Energy Usage and Green Gas Emission' + YearLabel + ' (' + category + ': ' + str(
        cat_value) + ')'

    df = df_energy[df_energy['Year Ending'].isin(years)][[i1, i2, i3, i4, i5, i6, i7, i8, i9,
                                                          t1, t2, t3, t4, t5, t6, t7, t8, t9,
                                                          e1, e2, e3, e4, s1, s2, s3, s4] + l_head]
    df = df[df[category] == cat_value]

    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    return [table_title,
            dff.iloc[
            page_current * page_size: (page_current + 1) * page_size
            ].to_dict('records')]


if __name__ == '__main__':
    app.run_server(debug=False,
                   host="0.0.0.0",
                   port=8080)
