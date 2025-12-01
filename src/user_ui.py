import streamlit as st
from .consts import *
from .dataframe_analize import *
class Page:

    def __init__(self):
        self.title = "home"
        self.page_statement = st.session_state
        self.data = st.session_state
        self.__init_statics()
        self.__init_data()
        self.__init_page_statement()
    def __init_statics(self):
        self.show_logo()
        self.show_setting()

    def __init_data(self):
        if 'columns' not in self.data:
            self.data.columns = dict()
        if 'is_loaded' not in self.data:
            self.page_statement.is_loaded = 0
        if 'selected_dt' not in self.data:
            self.page_statement.selected_dt = None
        if 'mode_count' not in self.page_statement:
            self.page_statement.mode_count = 1
        if 'selected_column' not in self.page_statement:
            self.page_statement.selected_column = None
        if 'plot_created' not in self.page_statement:
            self.page_statement.plot_created = 0
        if 'results' not in self.data:
            self.data.results = 'No results'
        if 'data' not in self.data:
            self.data.data = None
        if 'df' not in self.data:
            self.data.df = None
        if 'plot_type' not in self.page_statement:
            self.page_statement.plot_type = 'hist'
        if 'multyselect' not in self.page_statement:
            self.page_statement.multyselect = []

    def __init_page_statement(self):
        self.conf_placeholder = st.empty()
        self.dataset_placeholder = st.container(border=False)
        self.panel_placeholder = st.container(border=bool(self.data.is_loaded))
        self.plot_placeholder = st.container(border=False)

    @staticmethod
    def __init_footer():
        with st.container():
            st.markdown("Created by :red[**Arthurius**] — 😺 [GitHub](https://github.com/arthuraswork)")
    def get_user_data(self, userdata: dict):
        if 'userdata' not in self.data:
            self.data.userdata = userdata

    def requester(self, query):
        try:

            result = request(self.data.df, query)
            self.data.df = result
        except Exception as e:
            st.error(f'Error: {e}')
    def dataframe_work(self):
        print(self.page_statement.multyselect)
        st.text(f"multyselected columns: {' * '.join(self.page_statement.multyselect)}")

        column_option = st.radio(
            "Select columns",
            self.data.columns, horizontal=True
                 )

        self.data.selected_dt = str(self.data.df[column_option].dtype)
        self.data.selected_column = column_option
        if self.data.selected_dt == "object":
            option = st.radio(
                "Select option",
                OPTIONS,
                horizontal=True,
            )
        else:
            option = st.radio(
                "Select option",
                OPTIONS + NUM_OPTIONS,
                horizontal=True,
            )

        user_input = st.text_input('input pandas query')

        with st.container(horizontal=True):
            if column_option:
                if st.button("Plot"):
                    if self.page_statement.plot_created:
                        self.page_statement.plot_created = 0

                    else:
                        self.page_statement.plot_created = 1

            if option and column_option:
                if st.button("Calculate"):
                    results = metrica(
                        option, self.data.df, self.page_statement.selected_column, self.page_statement.mode_count
                                      )
                    self.data.results = results

            if st.button("Request"):
                if user_input:
                    self.requester(user_input)
                    st.rerun()

            if st.button("Reset"):
                self.data.df = self.data.data
                st.rerun()

            if st.button("Multyselect"):
                if column_option not in self.page_statement.multyselect:
                    self.page_statement.multyselect.append(column_option)
                self.page_statement.multyselect.pop(self.page_statement.multyselect.index(column_option))
                st.rerun()
                
                


        st.write(self.data.results)

    def visualisation(self):
        if self.page_statement.selected_column and self.page_statement.plot_created:
            with self.plot_placeholder:

                if self.page_statement.plot_type == "corr":
                    st.write(corr(self.data.df))

                if self.data.selected_dt != "object":
                    if self.page_statement.plot_type == "hist":
                        st.bar_chart(self.data.df[self.page_statement.selected_column])
                    elif self.page_statement.plot_type == "area":
                        st.area_chart(self.data.df[self.page_statement.selected_column])
                    elif self.page_statement.plot_type == "plot":
                        st.line_chart(self.data.df[self.page_statement.selected_column])      
    
                else:
                    value_counts = self.data.df[self.page_statement.selected_column].value_counts().head(10)
                    st.bar_chart(value_counts)
        else:
            with self.plot_placeholder:
                st.write(f'{self.page_statement.selected_column} -> {self.page_statement.selected_dt}')


    def show_df(self):
        with self.dataset_placeholder:
            st.write(self.data.df)

    def show_setting(self):
        with st.expander("Settings"):
            self.page_statement.mode_count = st.slider('Mode count', min_value=1, max_value=10, step=1)
            option_map = {
                'hist': ":material/grouped_bar_chart:",
                'area': ":material/show_chart:",
                'plot': ":material/line_axis:",
                'corr': ":material/border_all:"
            }
            self.page_statement.plot_type = st.pills(
                "Plot type",
                options=option_map.keys(),
                format_func=lambda option: option_map[option],
                selection_mode="single",
            )




    def upload_dataset(self):
        with self.dataset_placeholder.container():
            df = st.file_uploader(
            label="Load dataset",
            type="csv",
            help=f"max size: {MAX_FILE_SIZE}",
            key="dataset_uploader"
        )
            if df is not None:
                if df.size > MAX_FILE_SIZE:
                    st.error("File too big")
                else:
                    data = read_df(df)
                    if isinstance(data, pd.DataFrame):
                        self.data.columns = data.columns.tolist()
                        self.data.df = data
                        self.data.data = data
                        self.page_statement.is_loaded = 1
                        self.dataset_placeholder.empty()
                        st.rerun()

                    else:
                        st.error("Dataset is empty or not exist")

    @staticmethod
    def show_logo():
        st.header("EasyDA")

    def page(self):
        if self.page_statement.is_loaded == 0:
            self.upload_dataset()
        if self.page_statement.is_loaded == 1:
            self.show_df()
            with self.panel_placeholder:
                self.dataframe_work()
                self.visualisation()
        self.__init_footer()




