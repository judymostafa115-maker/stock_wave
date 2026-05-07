import streamlit as st
import yfinance as yf
import plotly.express as px

st.title("📈 Stock Market Analysis System")

st.write("Enter a stock symbol to view stock data and price trends.")

# Input
symbol = st.text_input("Enter Stock Symbol", "AAPL")

# Period Selection
period = st.selectbox(
    "Choose Period",
    ["7d", "1mo", "3mo", "6mo", "1y"]
)

# Search Button
if st.button("Search"):

    try:
        # Fetch Data
        stock = yf.Ticker(symbol)

        data = stock.history(period=period)

        info = stock.info

        # Check if data exists
        if data.empty:
            st.error("Invalid stock symbol or no data found.")

        else:

            # Company Name
            company_name = info.get("longName", symbol.upper())

            st.subheader(f"Company Name: {company_name}")

            # Prices
            current_price = data["Close"].iloc[-1]
            high_price = data["High"].max()
            low_price = data["Low"].min()
            volume = data["Volume"].sum()

            # Metrics
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Current Price", f"${current_price:.2f}")
            col2.metric("High Price", f"${high_price:.2f}")
            col3.metric("Low Price", f"${low_price:.2f}")
            col4.metric("Volume", f"{volume:,}")

            st.markdown("---")

            # Historical Data Table
            st.subheader("Historical Stock Data")

            st.dataframe(data)

            st.markdown("---")

            # Line Chart
            st.subheader("Line Chart")

            line_fig = px.line(
                data,
                x=data.index,
                y="Close",
                title=f"{company_name} Closing Price Trend"
            )

            st.plotly_chart(line_fig)

            st.markdown("---")

            # Bar Chart
            st.subheader("Bar Chart")

            bar_fig = px.bar(
                data,
                x=data.index,
                y="Volume",
                title=f"{company_name} Trading Volume"
            )

            st.plotly_chart(bar_fig)

    except:
        st.error("Something went wrong. Please check the stock symbol.")