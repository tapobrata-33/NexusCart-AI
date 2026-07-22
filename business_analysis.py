def business_report(df):


    total_revenue = df["Total Amount"].sum()


    total_orders = df["Transaction ID"].count()


    total_customers = df["Customer ID"].nunique()


    average_order = df["Total Amount"].mean()



    print("======================")

    print("NEXUS AI REPORT")

    print("======================")


    print(
        "Total Revenue:",
        total_revenue
    )


    print(
        "Total Orders:",
        total_orders
    )


    print(
        "Total Customers:",
        total_customers
    )


    print(
        "Average Order Value:",
        average_order
    )


    return {
        "Revenue":total_revenue,
        "Orders":total_orders,
        "Customers":total_customers,
        "Average Order":average_order
    }