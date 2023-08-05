import plotly.offline as py
import plotly.graph_objs as go
from plotly.io import to_html

import pandas as pd

class Presentation:

    def __init__(self, path_dir_statics:str, dark_mode:bool=True):
        self.__list_section = []
        self.__dark_mode = dark_mode
        self.__dir_statics = path_dir_statics

    def __get_layout(self):
        return go.Layout(autosize=True,
                   template='plotly_dark' if self.__dark_mode else None, #TODO(erfan): change it
                   )

    def add_h2(self, title:str):
        self.__list_section.append(f'<h2>{title}</h2>')
    
    def add_paragraph(self, paragraph:str):
        self.__list_section.append(f'<p>{paragraph}</p>')

    def add_scatter(self, x_data:list[float], y_data:list[float], title:str):
        # trace = go.Scatter(x=[1, 2, 3, 4], y=[10, 15, 13, 17])
        trace = go.Scatter(x=x_data, y=y_data)
        data = [trace]

        fig = go.Figure(data=data)
        self.__list_section.append(self.__fig_to_html_div(fig=fig,title=title))

    def add_fig(self, plotly_fig:go.Figure):
        self.__list_section.append(self.__fig_to_html_div(fig=plotly_fig))


    def __fig_to_html_div(self, fig:go.Figure,title:str) -> str:
        __layout = self.__get_layout()
        __layout.title=title
        fig.layout = __layout
        return to_html(fig, full_html=False, 
                                    #div_id='tt-aa-id',
                                    # include_plotlyjs=True
                                    include_plotlyjs='cdn'
                                    )

    def add_candlestick(self, df_price:pd.DataFrame, 
                                title:str,
                                col_name_date='date',
                                col_name_open='open',
                                col_name_high='high',
                                col_name_low='low',
                                col_name_close='close',
                                show_bottom_section=False
                                ):
        fig = go.Figure(data=[go.Candlestick(x=df_price[col_name_date],
                open=df_price[col_name_open],
                high=df_price[col_name_high],
                low=df_price[col_name_low],
                close=df_price[col_name_close])])

        if not show_bottom_section:
            fig.update_layout(xaxis_rangeslider_visible=False)


        self.__list_section.append(self.__fig_to_html_div(fig=fig,
                title=title))

    def add_table_zebra(self, df_table:pd.DataFrame, 
                        title:str,
                        headerColor:str = 'grey',
                        rowEvenColor:str = 'lightgrey',
                        rowOddColor:str = 'white'
                        ):

        __list_cols = df_table.columns.tolist()
        __list_cols = [f'<b>{col}</b>' for col in __list_cols]

        fig = go.Figure(data=[go.Table(
                                header=dict(
                                    values=__list_cols,
                                    line_color='darkslategray',
                                    fill_color=headerColor,
                                    # align=['left','center'],
                                    align=['center'],
                                    font=dict(color='white', size=12)
                                ),
                                cells=dict(
                                    values=df_table.values.T,
                                    line_color='darkslategray',
                                    # 2-D list of colors for alternating rows
                                    fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
                                    align = ['left', 'center'],
                                    font = dict(color = 'darkslategray', size = 11)
                                    ))
                            ],
                    

                        )
        self.__list_section.append(self.__fig_to_html_div(fig=fig, title=title))


    def get_html_str(self):
        __css_str = f'<link rel="stylesheet" href="{self.__dir_statics}/style.css">'
        return f'<html><head>{__css_str}</head><body class="{"body-dark" if self.__dark_mode else "body-light"}">{"<br/>".join(self.__list_section)}</body></html>'

    def save_html_file(self, path:str='presentation.html'):
        with open(path, "w") as text_file:
            text_file.write(self.get_html_str())
# # Create a line chart
# trace = go.Scatter(x=[1, 2, 3, 4], y=[10, 15, 13, 17])
# data = [trace]
# layout = go.Layout(title='Line Chart', 
#                    template='plotly_dark',
#                    annotations=[
#                         dict(
#                             templateitemname="draft watermark",
#                             text="erfan.ai",
#                         )
#                     ]
                   
#                    )
# fig = go.Figure(data=data, layout=layout)

# # Save the chart as an HTML file
# py.plot(fig, filename='line-chart.html', auto_open=False)


# plot_html = to_html(fig, full_html=False, div_id='tt-aa-id', include_plotlyjs=False)
# print(plot_html)