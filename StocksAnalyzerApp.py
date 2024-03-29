import streamlit as st
from PIL import Image
import json
from streamlit_option_menu import option_menu
from StockDataAnalyzer import StockDatapipeline
from StockNewsAnalyzer import StockNews, StockTweets
from StockPredictionAnalyzer import LongShortTermMemory, XGBoostModel
#from streamlit_lottie import st_lottie
st.set_page_config(layout="wide", initial_sidebar_state='expanded',
                   page_title="Stocks Analyzer", page_icon="chart_with_upwards_trend")


class StockApp:
    def __init__(self):
        self.path = StockDatapipeline.get_current_dir()
        self.settings = StockDatapipeline.load_settings(self.path)
        self.css = self.settings['css_file']
        self.local_css(self.css)
        self.stock_list = self.settings['stock_list']
        # self.lottie = self.settings['lottie']

    @staticmethod
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def layout(self):
        # with st.sidebar:
        #     st_lottie(self.lottie, key='Hello')
        # st_lottie(self.lottie)
        stock = st.sidebar.selectbox(
            label='Select Stocks', options=self.stock_list)
    #    with st.container():
    #        st_lottie(self.lottie, key="hello")

        curr_price = StockDatapipeline(
            stock_ticker=stock).get_realtime_stock_price()
        curr_open = StockDatapipeline(
            stock_ticker=stock).get_current_stock_open_price()
        curr_vol = StockDatapipeline(stock_ticker=stock).get_stock_volume()

        b1, b2, b3 = st.columns(3)
        b1.metric("Stock Price", str(curr_price)+' USD')
        b2.metric("Open", str(curr_open)+' USD')
        b3.metric("Volume", str(curr_vol)+' USD')

        with st.container():
            selected = option_menu("Technical Analysis", ["", "RSI", 'MACD', '50D SMA', '100D SMA', '200D SMA'],
                                   menu_icon="cast", orientation="horizontal", default_index=0)

            if selected == "RSI":
                st.pyplot(fig=StockDatapipeline(stock_ticker=stock).plot_rsi())
            if selected == "MACD":
                st.pyplot(fig=StockDatapipeline(
                    stock_ticker=stock).plot_macd())
            if selected == "50D SMA":
                st.pyplot(fig=StockDatapipeline(
                    stock_ticker=stock).plot_50_days_sma())
            if selected == "100D SMA":
                st.pyplot(fig=StockDatapipeline(
                    stock_ticker=stock).plot_100_days_sma())
            if selected == "200D SMA":
                st.pyplot(fig=StockDatapipeline(
                    stock_ticker=stock).plot_200_days_sma())

        with st.sidebar:
            col1, col3 = st.columns(2)
            with col1:
                if st.button(label='Download Stock Data'):
                    StockDatapipeline(
                        stock_ticker=stock).download_stock_ticker_data()
                    st.write('## Stock Data Downloaded')

            with col3:
                if st.button(label="Download Stock Info",):
                    StockDatapipeline(
                        stock_ticker=stock).download_market_info()
                    st.write('## Market Info Downloaded')

        with st.container():
            st.markdown('### Stock Price Chart')
            st.pyplot(fig=StockDatapipeline(
                stock_ticker=stock).plot_trend())

        c1, c2 = st.columns((5, 5))
        with c1:
            st.markdown('### Two Side View')
            st.pyplot(fig=StockDatapipeline(
                stock_ticker=stock).plot_two_side_view())

        with c2:
            st.markdown('### Tweets Sentiment Overview')
            st.pyplot(fig=StockNews(
                stock_ticker=stock).plot_tweet_sentiment_donut_chart())

        with st.container():
            st.markdown('### Daily News Sentiments')
            st.pyplot(fig=StockNews(
                stock_ticker=stock).plot_daily_sentiment_barchart())
            # StockTweets(stock_ticker=stock).plot_tweet_sentiment_donut_chart()

        with st.container():
            st.markdown('### Daily News Affecting Price')
            st.pyplot(fig=StockNews(
                stock_ticker=stock).plot_sentiments_with_price())

        with st.container():
            st.markdown('### LSTM Predictions')
            st.pyplot(fig=LongShortTermMemory(
                stock_ticker=stock).plot_prediction())

        with st.container():
            st.markdown('### XGBoost Predictions')
            st.pyplot(fig=XGBoostModel(
                stock_ticker=stock).plot_xgboost_prediction())


if __name__ == "__main__":
    StockApp().layout()
