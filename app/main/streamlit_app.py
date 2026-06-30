import os

import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


load_dotenv()


st.set_page_config(
    page_title="TravelPulse Analytics",
    page_icon="📊",
    layout="wide"
)


# -------------------------
# LOAD DATA FROM MYSQL
# -------------------------
@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    df = pd.read_sql("SELECT * FROM bookings", conn)
    conn.close()
    return df


df = load_data()


# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("TravelPulse Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Overview",
        "Booking Trends",
        "Customer Behaviour",
        "Data Explorer",
        "AI Predictions"
    ]
)

st.success("Connected to MySQL successfully!")


# -------------------------
# COMMON VALUES
# -------------------------
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

total_bookings = len(df)
cancellation_rate = round(df["is_canceled"].mean() * 100, 2)
avg_adr = round(df["adr"].mean(), 2)
avg_lead_time = int(round(df["lead_time"].mean(), 0))


# -------------------------
# OVERVIEW PAGE
# -------------------------
if page == "Overview":
    st.title("Booking Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Bookings", f"{total_bookings:,}")
    col2.metric("Cancellation Rate", f"{cancellation_rate}%")
    col3.metric("Average ADR", f"£{avg_adr}")
    col4.metric("Average Lead Time", f"{avg_lead_time} days")

    st.divider()

    chart_col1, chart_col2 = st.columns(2)

    hotel_df = df["hotel"].value_counts().reset_index()
    hotel_df.columns = ["hotel", "bookings"]

    fig_hotel = px.pie(
        hotel_df,
        names="hotel",
        values="bookings",
        hole=0.5,
        title="Hotel Type Split"
    )

    chart_col1.plotly_chart(fig_hotel, use_container_width=True)

    country_df = df["country"].value_counts().head(10).reset_index()
    country_df.columns = ["country", "bookings"]

    fig_country = px.bar(
        country_df,
        x="bookings",
        y="country",
        orientation="h",
        title="Top 10 Guest Countries"
    )

    fig_country.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Bookings",
        yaxis_title="Country"
    )

    chart_col2.plotly_chart(fig_country, use_container_width=True)

    monthly_df = df.groupby("arrival_month").size().reset_index(name="bookings")

    monthly_df["arrival_month"] = pd.Categorical(
        monthly_df["arrival_month"],
        categories=month_order,
        ordered=True
    )

    monthly_df = monthly_df.sort_values("arrival_month")

    fig_monthly = px.line(
        monthly_df,
        x="arrival_month",
        y="bookings",
        markers=True,
        title="Monthly Booking Volume"
    )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Bookings"
    )

    st.plotly_chart(fig_monthly, use_container_width=True)


# -------------------------
# BOOKING TRENDS PAGE
# -------------------------
elif page == "Booking Trends":
    st.title("Booking Trends")

    monthly_hotel = df.groupby(
        ["arrival_month", "hotel"]
    ).size().reset_index(name="bookings")

    monthly_hotel["arrival_month"] = pd.Categorical(
        monthly_hotel["arrival_month"],
        categories=month_order,
        ordered=True
    )

    monthly_hotel = monthly_hotel.sort_values("arrival_month")

    fig1 = px.bar(
        monthly_hotel,
        x="arrival_month",
        y="bookings",
        color="hotel",
        barmode="group",
        title="Monthly Bookings by Hotel Type"
    )

    fig1.update_layout(
        xaxis_title="Month",
        yaxis_title="Bookings"
    )

    st.plotly_chart(fig1, use_container_width=True)

    adr_month = df.groupby(
        ["arrival_month", "hotel"]
    )["adr"].mean().reset_index()

    adr_month["arrival_month"] = pd.Categorical(
        adr_month["arrival_month"],
        categories=month_order,
        ordered=True
    )

    adr_month = adr_month.sort_values("arrival_month")

    fig2 = px.line(
        adr_month,
        x="arrival_month",
        y="adr",
        color="hotel",
        markers=True,
        title="Average Daily Rate by Month"
    )

    fig2.update_layout(
        xaxis_title="Month",
        yaxis_title="Average Daily Rate (£)"
    )

    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(
        df,
        x="lead_time",
        nbins=40,
        title="Lead Time Distribution"
    )

    fig3.update_layout(
        xaxis_title="Days Before Arrival",
        yaxis_title="Number of Bookings"
    )

    st.plotly_chart(fig3, use_container_width=True)

    cancel_month = df.groupby("arrival_month")["is_canceled"].mean().reset_index()
    cancel_month["cancellation_rate"] = cancel_month["is_canceled"] * 100

    cancel_month["arrival_month"] = pd.Categorical(
        cancel_month["arrival_month"],
        categories=month_order,
        ordered=True
    )

    cancel_month = cancel_month.sort_values("arrival_month")

    fig4 = px.line(
        cancel_month,
        x="arrival_month",
        y="cancellation_rate",
        markers=True,
        title="Cancellation Rate by Month"
    )

    fig4.update_layout(
        xaxis_title="Month",
        yaxis_title="Cancellation Rate (%)"
    )

    st.plotly_chart(fig4, use_container_width=True)


# -------------------------
# CUSTOMER BEHAVIOUR PAGE
# -------------------------
elif page == "Customer Behaviour":
    st.title("Customer Behaviour")

    col1, col2 = st.columns(2)

    market_df = df["market_segment"].value_counts().reset_index()
    market_df.columns = ["market_segment", "bookings"]

    fig_market = px.bar(
        market_df,
        x="market_segment",
        y="bookings",
        title="Bookings by Market Segment"
    )

    fig_market.update_layout(
        xaxis_title="Market Segment",
        yaxis_title="Bookings"
    )

    col1.plotly_chart(fig_market, use_container_width=True)

    deposit_df = df["deposit_type"].value_counts().reset_index()
    deposit_df.columns = ["deposit_type", "bookings"]

    fig_deposit = px.pie(
        deposit_df,
        names="deposit_type",
        values="bookings",
        hole=0.5,
        title="Deposit Type Distribution"
    )

    col2.plotly_chart(fig_deposit, use_container_width=True)

    customer_df = df["customer_type"].value_counts().reset_index()
    customer_df.columns = ["customer_type", "bookings"]

    fig_customer = px.bar(
        customer_df,
        x="customer_type",
        y="bookings",
        title="Bookings by Customer Type"
    )

    fig_customer.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Bookings"
    )

    st.plotly_chart(fig_customer, use_container_width=True)

    status_df = df["reservation_status"].value_counts().reset_index()
    status_df.columns = ["reservation_status", "bookings"]

    fig_status = px.pie(
        status_df,
        names="reservation_status",
        values="bookings",
        hole=0.5,
        title="Reservation Status Distribution"
    )

    st.plotly_chart(fig_status, use_container_width=True)


# -------------------------
# DATA EXPLORER PAGE
# -------------------------
elif page == "Data Explorer":
    st.title("Data Explorer")

    hotel_filter = st.multiselect(
        "Filter by Hotel Type",
        options=sorted(df["hotel"].unique()),
        default=list(sorted(df["hotel"].unique()))
    )

    year_filter = st.multiselect(
        "Filter by Arrival Year",
        options=sorted(df["arrival_year"].unique()),
        default=list(sorted(df["arrival_year"].unique()))
    )

    month_filter = st.multiselect(
        "Filter by Arrival Month",
        options=month_order,
        default=month_order
    )

    search_text = st.text_input("Search by country, market segment, or reservation status")

    filtered_df = df[
        (df["hotel"].isin(hotel_filter)) &
        (df["arrival_year"].isin(year_filter)) &
        (df["arrival_month"].isin(month_filter))
    ]

    if search_text:
        search_text = search_text.lower()
        filtered_df = filtered_df[
            filtered_df["country"].astype(str).str.lower().str.contains(search_text) |
            filtered_df["market_segment"].astype(str).str.lower().str.contains(search_text) |
            filtered_df["reservation_status"].astype(str).str.lower().str.contains(search_text)
        ]

    st.write(f"Showing {len(filtered_df):,} records")

    visible_columns = [
        "id",
        "hotel",
        "is_canceled",
        "lead_time",
        "arrival_year",
        "arrival_month",
        "country",
        "market_segment",
        "adr",
        "deposit_type",
        "customer_type",
        "reservation_status"
    ]

    st.dataframe(
        filtered_df[visible_columns],
        use_container_width=True
    )

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered CSV",
        data=csv,
        file_name="travelpulse_filtered_data.csv",
        mime="text/csv"
    )


# -------------------------
# AI PREDICTIONS PAGE
# -------------------------
elif page == "AI Predictions":
    st.title("AI Booking Cancellation Prediction")

    features = [
        "lead_time",
        "total_guests",
        "adr",
        "stays_weekend",
        "stays_weekday",
        "hotel",
        "deposit_type",
        "customer_type"
    ]

    model_df = df[features + ["is_canceled"]].copy()

    X = model_df[features].copy()
    y = model_df["is_canceled"]

    encoders = {}

    for col in ["hotel", "deposit_type", "customer_type"]:
        encoder = LabelEncoder()
        X[col] = encoder.fit_transform(X[col])
        encoders[col] = encoder

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100

    st.info(f"Random Forest Model Accuracy: {accuracy:.2f}%")

    st.subheader("Enter Booking Details")

    col1, col2 = st.columns(2)

    with col1:
        lead_time = st.slider("Lead Time (days)", 0, 700, 100)
        total_guests = st.number_input("Total Guests", min_value=1, max_value=10, value=2)
        adr = st.number_input("Average Daily Rate (£)", min_value=0.0, max_value=1000.0, value=100.0)
        stays_weekend = st.number_input("Weekend Nights", min_value=0, max_value=20, value=1)

    with col2:
        stays_weekday = st.number_input("Weekday Nights", min_value=0, max_value=50, value=2)
        hotel = st.selectbox("Hotel Type", sorted(df["hotel"].unique()))
        deposit_type = st.selectbox("Deposit Type", sorted(df["deposit_type"].unique()))
        customer_type = st.selectbox("Customer Type", sorted(df["customer_type"].unique()))

    if st.button("Predict Cancellation Risk"):
        input_data = pd.DataFrame({
            "lead_time": [lead_time],
            "total_guests": [total_guests],
            "adr": [adr],
            "stays_weekend": [stays_weekend],
            "stays_weekday": [stays_weekday],
            "hotel": [hotel],
            "deposit_type": [deposit_type],
            "customer_type": [customer_type]
        })

        for col in ["hotel", "deposit_type", "customer_type"]:
            input_data[col] = encoders[col].transform(input_data[col])

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100

        st.subheader("Prediction Result")

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=probability,
                title={"text": "Cancellation Probability (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "red" if probability >= 70 else "orange" if probability >= 40 else "green"},
                    "steps": [
                        {"range": [0, 40], "color": "lightgreen"},
                        {"range": [40, 70], "color": "khaki"},
                        {"range": [70, 100], "color": "lightcoral"}
                    ]
                }
            )
        )

        st.plotly_chart(gauge, use_container_width=True)

        st.metric(
            "Cancellation Probability",
            f"{probability:.2f}%"
        )

        if prediction == 1:
            st.error("Prediction: Likely to cancel")
        else:
            st.success("Prediction: Unlikely to cancel")

    st.divider()

    st.subheader("Feature Importance")

    importance_df = pd.DataFrame({
        "Feature": features,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    fig_importance = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Random Forest Feature Importance"
    )

    fig_importance.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig_importance, use_container_width=True)