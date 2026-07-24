import streamlit as st
import os


def run_ui():

    # Page style
    st.set_page_config(
        page_title="NexusCart AI Pro",
        page_icon="🛒",
        layout="wide"
    )


    # Header

    logo = "assets/logo.png"


    col1, col2 = st.columns([1,5])


    with col1:

        if os.path.exists(logo):

            st.image(
                logo,
                width=120
            )

        else:

            st.write("🛒")


    with col2:

        st.markdown(
            """
            # NexusCart AI Pro

            ### AI Powered Retail Intelligence Platform
            """
        )

        st.caption(
            "Enterprise Sales Analytics | AI Prediction | Customer Intelligence"
        )


    st.divider()


    # KPI Demo Cards

    a,b,c,d = st.columns(4)


    with a:
        st.metric(
            "💰 Revenue",
            "₹25,00,000",
            "+12%"
        )


    with b:
        st.metric(
            "📦 Orders",
            "5,240",
            "+8%"
        )


    with c:
        st.metric(
            "👥 Customers",
            "1,850",
            "+15%"
        )


    with d:
        st.metric(
            "🤖 AI Score",
            "94%",
            "Excellent"
        )


    st.divider()


    st.subheader(
        "🧠 AI Business Insight"
    )


    st.success(
        """
        🏆 Electronics is the top performing category.

        📈 Sales growth is increasing.

        🎯 Recommendation:
        Increase inventory for high-demand products.
        """
    )


    st.subheader(
        "📊 Dashboard Preview"
    )


    st.info(
        """
        Your existing AI dashboard will be connected here.
        """
    )



if __name__ == "__main__":

    run_ui()