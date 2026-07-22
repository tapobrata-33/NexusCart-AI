import pandas as pd


def export_kpi(report):


    df = pd.DataFrame({

        "Metric":
        report.keys(),


        "Value":
        report.values()

    })


    df.to_csv(
        "NexusAI_KPI.csv",
        index=False
    )


    print(
        "Power BI KPI File Created"
    )