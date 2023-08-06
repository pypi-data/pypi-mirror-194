import plotly.offline as py
import plotly.graph_objs as go
from plotly.io import to_html

import pandas as pd

class Presentation:

    def __init__(self, path_dir_statics:str, dark_mode:bool=True):
        """init function of the Presentation

        Args:
            path_dir_statics (str): where is the location of web statics directory
            dark_mode (bool, optional): change report style to dark_mode . Defaults to True.
        """
        self.__list_section = []
        self.__dark_mode = dark_mode
        self.__dir_statics = path_dir_statics

    def __get_layout(self):
        return go.Layout(autosize=True,
                   template='plotly_dark' if self.__dark_mode else None, #TODO(erfan): change it
                   )

    def add_h2(self, title:str):
        """Add html h2 tag to the report

        Args:
            title (str): the text inside the h2 tag
        """
        self.__list_section.append(f'<h2>{title}</h2>')
    
    def add_paragraph(self, paragraph:str):
        """Add html p elem to the report

        Args:
            paragraph (str): text inside the p tag
        """
        self.__list_section.append(f'<p>{paragraph}</p>')

    def add_scatter(self, x_data:list[float], y_data:list[float], title:str):
        """Plot a scatter_plot and add that to the presentation flow

        Args:
            x_data (list[float]): list of float number as x
            y_data (list[float]): list of float number as y
            title (str): the chart title
        """
        # trace = go.Scatter(x=[1, 2, 3, 4], y=[10, 15, 13, 17])
        trace = go.Scatter(x=x_data, y=y_data)
        data = [trace]

        fig = go.Figure(data=data)
        self.__list_section.append(self.__fig_to_html_div(fig=fig,title=title))

    def add_fig(self, plotly_fig:go.Figure):
        """Add custom plotly fig to the report

        Args:
            plotly_fig (go.Figure): plotly fig, for example:
                __fig = go.Scatter(x=x_data, y=y_data)
                add_fig(plotly_fig=__fig)
        """
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
        """Add candlestick chart

        Args:
            df_price (pd.DataFrame): the price dataframe containing open, high, low and close price
            title (str): The chart title
            col_name_date (str, optional): Date column name, the type of date should be datetime . Defaults to 'date'.
            col_name_open (str, optional): The open price column name. Defaults to 'open'.
            col_name_high (str, optional): The high price column name. Defaults to 'high'.
            col_name_low (str, optional): The low price column name. Defaults to 'low'.
            col_name_close (str, optional): The close price column name. Defaults to 'close'.
            show_bottom_section (bool, optional): Show minimized chart under the main chart?. Defaults to False.
        """
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
        """Add zebra style tables

        Args:
            df_table (pd.DataFrame): Pandas dataframe that you want to plot
            title (str): The chart title
            headerColor (str, optional): the color could be hex as well. Defaults to 'grey'.
            rowEvenColor (str, optional): the color could be hex as well. Defaults to 'lightgrey'.
            rowOddColor (str, optional): the color could be hex as well. Defaults to 'white'.
        """

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


    def get_html_str(self) -> str:
        """Generate the string (HTML in string) of the  report 

        Returns:
            str: return the HTML in string
        """
        __css_str = f'<link rel="stylesheet" href="{self.__dir_statics}/style.css">'
        return f'<html><head>{__css_str}</head><body class="{"body-dark" if self.__dark_mode else "body-light"}">{"<br/>".join(self.__list_section)}</body></html>'

    def save_html_file(self, path:str='presentation.html'):
        """Save the report file in html in custom path.

        Args:
            path (str, optional): You should add full custom path like xxx/statics/presentation.html . Defaults to 'presentation.html'.
        """
        with open(path, "w") as text_file:
            text_file.write(self.get_html_str())
