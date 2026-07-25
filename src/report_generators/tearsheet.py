import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from reportlab.platypus import *

from reportlab.platypus import PageBreak

from reportlab.lib import colors

from reportlab.platypus import Image

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.units import inch

from reportlab.lib.pagesizes import A4

from reportlab.lib.enums import TA_CENTER

from reportlab.graphics.shapes import Drawing

from reportlab.graphics.charts.barcharts import VerticalBarChart

def generate_tearsheet(company_id):

    BASE_DIR = Path(__file__).resolve().parents[2]

    DB_PATH = BASE_DIR / "nifty100.db"

    OUTPUT_DIR = BASE_DIR / "output"

    REPORT_DIR = OUTPUT_DIR / "reports"
    CHART_DIR = REPORT_DIR / "charts"

    CHART_DIR.mkdir(
    parents=True,
    exist_ok=True
)

    REPORT_DIR.mkdir(
    exist_ok=True
)

    conn = sqlite3.connect(DB_PATH)


    company = pd.read_sql(f"""

    SELECT *

    FROM companies

    WHERE id='{company_id}'

    """,conn)

    print(company)

    ratios = pd.read_sql(f"""

    SELECT *

    FROM financial_ratios

    WHERE company_id='{company_id}'

    ORDER BY year

    """,conn)

    print(ratios.head())
    market = pd.read_sql(f"""
    SELECT *
    FROM market_cap
    WHERE company_id='{company_id}'
    ORDER BY year
    """, conn)

    latest_market = market.iloc[-1]

    pl = pd.read_sql(f"""

    SELECT *

    FROM profitandloss

    WHERE company_id='{company_id}'

    ORDER BY year

    """,conn)

    bs = pd.read_sql(f"""

    SELECT *

    FROM balancesheet

    WHERE company_id='{company_id}'

    ORDER BY year

    """,conn)
    print(bs.columns.tolist())
    print(bs.head())

    plt.figure(figsize=(5.2,3))

    plt.bar(
    pl["year"],
    pl["sales"],
    edgecolor="black"
)

    plt.ylabel("₹ Cr")

    plt.title("Revenue Trend")

    plt.xticks(rotation=35)

    plt.grid(axis="y",alpha=0.3)

    plt.tight_layout()

    plt.figure(figsize=(5,3))

    plt.bar(
    pl["year"],
    pl["net_profit"]
)

    plt.xticks(rotation=45)

    plt.ylabel("₹ Cr")

    plt.title("Net Profit Trend")

    plt.grid(axis="y",alpha=0.3)

    plt.tight_layout()

    plt.savefig(
    CHART_DIR / "profit.png"
)

    plt.close()

    plt.figure(figsize=(6,3))

    plt.plot(
    ratios["year"],
    ratios["return_on_equity_pct"],
    marker="o",
    linewidth=2.5,
    markersize=5,
    label="ROE"
)

    plt.plot(
    ratios["year"],
    ratios["return_on_capital_employed_pct"],
    marker="o",
    label="ROCE"
)

    plt.xticks(rotation=45)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
    CHART_DIR / "roe_roce.png"
)

    plt.close()

    cf = pd.read_sql(f"""

    SELECT *

    FROM cashflow

    WHERE company_id='{company_id}'

    ORDER BY year

    """,conn)

    pros = pd.read_csv(
    OUTPUT_DIR/"pros_cons_generated.csv"
)
 
    pros = pros[
    pros.company_id==company_id
]

    cash = pd.read_csv(
OUTPUT_DIR/"cashflow_intelligence.csv"
)

    cash = cash[
cash.company_id==company_id
]

    company.shape

    ratios.shape

    pl.shape

    bs.shape

    cf.shape

    pros.shape

    cash.shape

    doc = SimpleDocTemplate(
    str(REPORT_DIR / f"{company_id}.pdf"),
    pagesize=A4
)
    story=[]
    styles=getSampleStyleSheet()
    from reportlab.lib.styles import ParagraphStyle

    header_style = ParagraphStyle(
    "Header",
    parent=styles["Title"],
    fontSize=20,
    leading=24,
    alignment=TA_CENTER,
    textColor=colors.white,
    spaceAfter=8
)

    subtitle_style = ParagraphStyle(
    "SubHeader",
    parent=styles["BodyText"],
    fontSize=10,
    alignment=TA_CENTER,
    textColor=colors.white
)
    latest = ratios.iloc[-1]

    header = Table([
    [
        Paragraph(
            f"<b>{company.iloc[0]['company_name']}</b>",
            header_style
        )
    ],
    [
        Paragraph(
            f"""
            <b>Ticker:</b> {company_id}
            &nbsp;&nbsp;&nbsp;&nbsp;
            <b>Latest FY:</b> {latest['year']}
            """,
            subtitle_style
        )
    ]
])

    header.setStyle([
    ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#0B1FA6")),
    ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ("TOPPADDING",(0,0),(-1,-1),8),
    ("ALIGN",(0,0),(-1,-1),"CENTER")
])

    story.append(header)
    story.append(Spacer(1,12))

    def kpi_card(title, value):

        card = Table([
        [
            Paragraph(
                f"<font size=10><b>{title}</b></font>",
                styles["BodyText"]
            )
        ],
        [
            Paragraph(
                f"<font size=17 color='#0B1FA6'><b>{value}</b></font>",
                styles["Heading2"]
            )
        ]
    ], colWidths=[145])

        card.setStyle([
        ("BOX",(0,0),(-1,-1),0.8,colors.grey),
        ("BACKGROUND",(0,0),(-1,-1),colors.whitesmoke),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("ALIGN",(0,0),(-1,-1),"CENTER")
    ])

        return card

    latest = ratios.iloc[-1]
    roe = kpi_card(
    "ROE",
    f"{latest['return_on_equity_pct']:.2f}%"
)

    roce = kpi_card(
    "ROCE",
    f"{latest['return_on_capital_employed_pct']:.2f}%"
)

    pe = kpi_card(
    "PE Ratio",
    f"{latest_market['pe_ratio']:.2f}"
)

    sales = kpi_card(
    "Revenue",
f"{latest['sales']:,.0f} Cr")

    market_cap = kpi_card(
    "Market Cap",
    f"{latest_market['market_cap_crore']:,.0f} Cr"
)

    fcf = kpi_card(
    "Free Cash Flow",
    f"{latest['free_cash_flow_cr']:,.0f} Cr"
)
    row1 = Table(
    [[roe,roce,pe]],
    colWidths=[160,160,160]
)
    row2 = Table(
    [[sales,market_cap,fcf]],
    colWidths=[160,160,160]
)
    story.append(row1)

    story.append(Spacer(1,12))

    story.append(row2)

    story.append(Spacer(1,20))

    revenue_chart = Image(
    str(CHART_DIR / "revenue.png"),
    width=220,
    height=140
)

    profit_chart = Image(
    str(CHART_DIR / "profit.png"),
    width=220,
    height=140
)

    charts = Table([
    [
        revenue_chart,
        profit_chart
    ]
])

    story.append(charts)

    story.append(Spacer(1,20))

    trend = Image(
    str(CHART_DIR / "roe_roce.png"),
    width=440,
    height=180
)

    story.append(trend)

    story.append(Spacer(1,20))
    story.append(PageBreak())
    story.append(
    Paragraph(
        "<b>Balance Sheet Composition</b>",
        styles["Heading2"]
    )
)

    story.append(Spacer(1,10))

    plt.figure(figsize=(6,3))

    equity = bs["equity_capital"] + bs["reserves"]

    borrow = bs["borrowings"]

    other = bs["other_liabilities"]
 
    plt.bar(
    bs["year"],
    equity,
    label="Net Worth"
)

    plt.bar(
    bs["year"],
    borrow,
    bottom=equity,
    label="Borrowings"
)

    plt.bar(
    bs["year"],
    other,
    bottom=equity+borrow,
    label="Other Liabilities"
)
  
    plt.legend()

    plt.xticks(rotation=35)

    plt.title("Balance Sheet Composition")

    plt.tight_layout()

    plt.savefig(CHART_DIR/"balance.png")

    plt.close()

    balance_chart = Image(
    str(CHART_DIR/"balance.png"),
    width=420,
    height=200
)

    story.append(balance_chart)

    story.append(Spacer(1,20))

    story.append(
    Paragraph(
        "<b>Latest Cash Flow Summary</b>",
        styles["Heading2"]
    )
)

    story.append(Spacer(1,10))
    latest_cf = cf.iloc[-1]

    cash_table = Table([
    ["Metric","Value (Cr)"],
    ["Operating Cash Flow", latest_cf["operating_activity"]],
    ["Investing Cash Flow", latest_cf["investing_activity"]],
    ["Financing Cash Flow", latest_cf["financing_activity"]],
    ["Net Cash Flow", latest_cf["net_cash_flow"]]
])

    cash_table.setStyle([

    ("GRID",(0,0),(-1,-1),0.5,colors.grey),

    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0B1FA6")),

    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

    ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ("BOTTOMPADDING",(0,0),(-1,-1),7),

    ("TOPPADDING",(0,0),(-1,-1),7)

])

    story.append(cash_table)

    story.append(Spacer(1,20))
    story.append(
    Paragraph(
        "<b>Strengths</b>",
        styles["Heading2"]
    )
)
    pros_df = pros[
    pros["type"]=="Pro"
]
    for text in pros_df["text"].head(5):

        story.append(

        Paragraph(

            f"<font color='green'>✔ {text}</font>",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1,15))

    story.append(
    Paragraph(
        "<b>Weaknesses</b>",
        styles["Heading2"]
    )
)
     
    cons_df = pros[
    pros["type"]=="Con"
]

    for text in cons_df["text"].head(5):

        story.append(

        Paragraph(

            f"<font color='red'>✖ {text}</font>",

            styles["BodyText"]

        )

    )

    cash = pd.read_csv(
    OUTPUT_DIR/"cashflow_intelligence.csv"
)

    company_cash = cash[
    cash.company_id==company_id
]

    allocation = company_cash.iloc[0]["capital_allocation"]

    story.append(Spacer(1,20))

    story.append(
    Paragraph(
        "<b>Capital Allocation</b>",
        styles["Heading2"]
    )
)

    badge = Table([
    [allocation]
])
    badge_colors = {
    "Shareholder Returns": colors.darkgreen,
    "Reinvestor": colors.blue,
    "Growth Funded by Debt": colors.orange,
    "Liquidating Assets": colors.purple,
    "Distress Signal": colors.red,
    "Mixed": colors.darkgoldenrod,
    "Pre-Revenue": colors.grey
}

    bg = badge_colors.get(
    allocation,
    colors.darkblue
)
    badge.setStyle([
    ("BACKGROUND",(0,0),(-1,-1),colors.darkgreen),
    ("TEXTCOLOR",(0,0),(-1,-1),colors.white),
    ("ALIGN",(0,0),(-1,-1),"CENTER"),
    ("BOTTOMPADDING",(0,0),(-1,-1),10),
    ("TOPPADDING",(0,0),(-1,-1),10),
    ("BOX",(0,0),(-1,-1),1,colors.black)
])

    story.append(badge)
    def footer(canvas, doc):

        canvas.saveState()

        canvas.setFont("Helvetica",8)

        canvas.drawString(
        40,
        20,
        "Generated by Nifty 100 Financial Intelligence Platform"
    )

        canvas.drawRightString(
        550,
        20,
        f"Page {doc.page}"
    )

        canvas.restoreState()
    doc.build(
    story,
    onFirstPage=footer,
    onLaterPages=footer
)
    conn.close()

    print("PDF Generated")
    print(f"Generated {company_id}.pdf")

    return True

if __name__ == "__main__":
    generate_tearsheet("TCS")