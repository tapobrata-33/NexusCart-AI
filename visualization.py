import matplotlib.pyplot as plt


def category_sales_chart(df):


    sales = df.groupby(
        "Product Category"
    )["Total Amount"].sum()



    plt.figure(figsize=(8,5))


    sales.plot(
        kind="bar"
    )


    plt.title(
        "Revenue By Category"
    )


    plt.xlabel(
        "Category"
    )


    plt.ylabel(
        "Revenue"
    )


    plt.tight_layout()


    plt.savefig(
        "category_sales.png"
    )


    plt.show()