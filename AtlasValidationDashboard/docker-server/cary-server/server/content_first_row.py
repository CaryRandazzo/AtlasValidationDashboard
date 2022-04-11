############################
# Import modules and files #
############################
import dash_bootstrap_components as dbc
import dash_html_components as html

from styles import *


################################
# Create content for first row #
################################
content_first_row = dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_1', children=['Card Title 1'], className='card-title',
                                style=CARD_TEXT_STYLE),
                        html.P(id='card_text_1', children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                )
            ]
        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H4(id='card_title_2',children=['Card Title 2'], className='card-title', style=CARD_TEXT_STYLE),
                        html.P(id='card_text_2',children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_3',children=['Card Title 3'], className='card-title', style=CARD_TEXT_STYLE),
                        html.P(id='card_text_3',children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]

        ),
        md=3
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H4(id='card_title_4',children=['Card Title 4'], className='card-title', style=CARD_TEXT_STYLE),
                        html.P(id='card_text_4',children=['Sample text.'], style=CARD_TEXT_STYLE),
                    ]
                ),
            ]
        ),
        md=3
    )
])