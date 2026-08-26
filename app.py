import streamlit as st
import pandas as pd


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Shopping Growth Agent",
    page_icon="🛍️",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------

st.title("🛍️ AI Shopping Growth Agent")

st.write(
    "Analyze shopping data and generate actionable growth recommendations."
)


# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("data.csv")


# -----------------------------
# Calculate Metrics
# -----------------------------

df["Conversion Rate (%)"] = (
    df["Orders"] / df["Views"] * 100
).round(2)

df["Revenue"] = df["Price"] * df["Orders"]


# -----------------------------
# Sales Overview
# -----------------------------

st.subheader("📊 Sales Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Products",
        len(df)
    )

with col2:
    st.metric(
        "Total Views",
        f"{df['Views'].sum():,}"
    )

with col3:
    st.metric(
        "Total Orders",
        f"{df['Orders'].sum():,}"
    )

with col4:

    total_revenue = df["Revenue"].sum()

    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )


# -----------------------------
# Product Performance
# -----------------------------

st.subheader("🛒 Product Performance")

st.dataframe(
    df[
        [
            "Product",
            "Category",
            "Price",
            "Views",
            "Orders",
            "Rating"
        ]
    ],
    width="stretch",
    hide_index=True
)


# -----------------------------
# Conversion Analysis
# -----------------------------

st.subheader("📈 Conversion Analysis")

st.dataframe(
    df[
        [
            "Product",
            "Views",
            "Orders",
            "Conversion Rate (%)"
        ]
    ],
    width="stretch",
    hide_index=True
)


# -----------------------------
# Products Needing Attention
# -----------------------------

st.subheader("⚠️ Products Needing Attention")

attention = df[
    df["Conversion Rate (%)"] < 3
]

if len(attention) > 0:

    st.dataframe(
        attention[
            [
                "Product",
                "Views",
                "Orders",
                "Conversion Rate (%)"
            ]
        ],
        width="stretch",
        hide_index=True
    )

else:

    st.success(
        "All products have a healthy conversion rate!"
    )


# =====================================================
# GROWTH AGENT
# =====================================================

st.subheader("🤖 AI Growth Recommendations")


# -----------------------------
# Recommendation Engine
# -----------------------------

def generate_recommendation(row):

    conversion = row["Conversion Rate (%)"]
    views = row["Views"]
    rating = row["Rating"]

    # High traffic + low conversion
    if views >= 3500 and conversion < 3:

        return (
            "🎯 Improve Conversion",

            "High customer interest but low conversion. "
            "Improve the product page, offer a limited-time "
            "discount, or add stronger product benefits."
        )

    # High conversion
    elif conversion >= 4:

        return (
            "🚀 Scale Product",

            "Strong conversion performance. "
            "Increase visibility through promotions and "
            "consider cross-selling with related products."
        )

    # Low rating
    elif rating < 4:

        return (
            "⭐ Improve Product",

            "Customer rating is relatively low. "
            "Investigate customer feedback and improve "
            "product quality or product information."
        )

    # Medium performance
    else:

        return (
            "📢 Promote",

            "Product has growth potential. "
            "Test targeted marketing campaigns and "
            "monitor conversion."
        )


# -----------------------------
# Priority Engine
# -----------------------------

def get_priority(row):

    conversion = row["Conversion Rate (%)"]
    views = row["Views"]
    rating = row["Rating"]

    # Highest priority
    if views >= 3500 and conversion < 3:

        return "🔴 High"

    # Medium priority because of rating
    elif rating < 4:

        return "🟠 Medium"

    # Strong products need less attention
    elif conversion >= 4:

        return "🟢 Low"

    # Normal products
    else:

        return "🟡 Medium"


# -----------------------------
# Agent Reason
# -----------------------------

def get_agent_reason(row):

    conversion = row["Conversion Rate (%)"]
    views = row["Views"]
    rating = row["Rating"]

    # High traffic + low conversion
    if views >= 3500 and conversion < 3:

        return (
            "High traffic but low conversion indicates "
            "strong customer interest with missed purchase "
            "opportunities."
        )

    # Low rating
    elif rating < 4:

        return (
            "Lower customer rating may be reducing "
            "buyer confidence."
        )

    # Strong conversion
    elif conversion >= 4:

        return (
            "Strong conversion indicates the product is "
            "performing well and can be scaled."
        )

    # Normal performance
    else:

        return (
            "Moderate performance suggests the product "
            "can benefit from targeted promotion."
        )


# -----------------------------
# Expected Impact
# -----------------------------

def get_expected_impact(row):

    conversion = row["Conversion Rate (%)"]
    views = row["Views"]
    rating = row["Rating"]

    if views >= 3500 and conversion < 3:

        return (
            "Potential increase in orders by improving "
            "purchase conversion."
        )

    elif conversion >= 4:

        return (
            "Potential revenue growth by increasing "
            "product visibility."
        )

    elif rating < 4:

        return (
            "Potential improvement in customer trust "
            "and conversion."
        )

    else:

        return (
            "Potential increase in product visibility "
            "and sales."
        )


# -----------------------------
# Generate Agent Decisions
# -----------------------------

recommendations = []


for _, row in df.iterrows():

    action, recommendation = generate_recommendation(row)

    priority = get_priority(row)

    reason = get_agent_reason(row)

    impact = get_expected_impact(row)

    recommendations.append(
        {
            "Product": row["Product"],
            "Priority": priority,
            "Action": action,
            "Why": reason,
            "Recommendation": recommendation,
            "Expected Impact": impact
        }
    )


# -----------------------------
# Recommendation DataFrame
# -----------------------------

recommendation_df = pd.DataFrame(
    recommendations
)


st.dataframe(
    recommendation_df,
    width="stretch",
    hide_index=True
)


# =====================================================
# TOP GROWTH OPPORTUNITY
# =====================================================

st.subheader("💡 Top Growth Opportunity")


# Find product with lowest conversion

top_opportunity = df.loc[
    df["Conversion Rate (%)"].idxmin()
]


product_name = top_opportunity["Product"]

conversion_rate = top_opportunity[
    "Conversion Rate (%)"
]

views = top_opportunity["Views"]

orders = top_opportunity["Orders"]


st.info(
    f"**{product_name}** has the lowest conversion rate "
    f"at **{conversion_rate}%** despite receiving "
    f"**{views:,} views** and generating "
    f"**{orders:,} orders**. "
    f"This makes it a strong candidate for a targeted "
    f"growth campaign."
)


# =====================================================
# AGENT SUMMARY
# =====================================================

st.subheader("🧠 Growth Agent Summary")


high_priority = len(
    recommendation_df[
        recommendation_df["Priority"] == "🔴 High"
    ]
)

medium_priority = len(
    recommendation_df[
        recommendation_df["Priority"].isin(
            ["🟠 Medium", "🟡 Medium"]
        )
    ]
)

low_priority = len(
    recommendation_df[
        recommendation_df["Priority"] == "🟢 Low"
    ]
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "🔴 High Priority",
        high_priority
    )


with col2:

    st.metric(
        "🟡 Medium Priority",
        medium_priority
    )


with col3:

    st.metric(
        "🟢 Low Priority",
        low_priority
    )


st.write(
    "The growth agent analyzes product traffic, conversion "
    "rate, and customer ratings to prioritize products and "
    "suggest suitable growth actions."
)


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "AI Shopping Growth Agent | "
    "Intelligent commerce analytics prototype"
)