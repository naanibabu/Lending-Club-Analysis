<div align="center">

# 📊 Loan Portfolio Risk & Performance Analytics
### A LendingClub Case Study

**An end-to-end analytics project — from raw loan data to an interactive Power BI dashboard — built to answer the questions a real credit risk, pricing, and finance team would ask.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-233D4D?style=for-the-badge&logo=microsoft&logoColor=white)

📄  [**Read the Full Case Study (PDF)**](./LC_report.pdf) &nbsp;|&nbsp; 📊 [**View Interactive Dashboard**](#) &nbsp;|&nbsp; 💼 [**Connect on LinkedIn**](#)

</div>

<br>

<p align="center">
  <img src="DashboardScreenshots/Risk_ananlysis.png" width="850">
</p>

<br>

## 📌 Overview

LendingClub, once the world's largest peer-to-peer lending platform, issued **over 2.2 million loans** between 2007–2018. Every loan that defaults is a direct financial loss — so LendingClub's core challenge is a constant balancing act: **lend to as many borrowers as possible to grow revenue, while keeping defaults low enough to protect margins.**

This project simulates the work of a Data Analyst tasked with answering that challenge — building a full pipeline from **890,000+ raw loan records** to a **3-page interactive Power BI dashboard**, uncovering which borrowers default, why, and what it's costing the business.

> 💡 **The goal wasn't just to visualize data — it was to produce insights a credit or pricing team could actually act on.**

<br>

## 🎯 Business Questions

This analysis was built to directly answer four questions a real lending business would ask:

| # | Question |
|---|---|
| 1 | Which borrower segments carry the highest default risk, and what patterns predict it? |
| 2 | Is the loan portfolio growing, and what's driving that growth? |
| 3 | Do riskier borrowers pay proportionally higher interest rates? |
| 4 | How much loan value is being lost to default, relative to the size of the portfolio? |

<br>

## 🔑 Key Findings

<table>
<tr>
<td width="25%" align="center"><h2>19.5%</h2>Portfolio-wide default rate</td>
<td width="25%" align="center"><h2>$18.5B</h2>Total funded across 1.3M loans</td>
<td width="25%" align="center"><h2>29.6%</h2>Default rate on Small Business loans — the riskiest purpose</td>
<td width="25%" align="center"><h2>3 pts</h2>Interest rate premium paid by borrowers who defaulted</td>
</tr>
</table>

- **Default risk is highly predictable.** Four signals — loan purpose, DTI, FICO score, and LendingClub's own loan grade — all move in a clean, monotonic relationship with default rate. FICO alone separates a 23.1% default rate (Fair credit) from 8.4% (Excellent credit).
- **Growth exploded post-2012.** The portfolio scaled from a near-zero base in 2007 to ~$5B in annual funded volume by 2014–15, driven by both more loans *and* larger average loan sizes.
- **Debt consolidation dominates the book** at $11B of $18.5B total funded — more than double the next-largest category — a concentration risk worth watching.
- **The pricing gap may not be enough.** Charged-off borrowers paid only a 3-point higher average interest rate (16% vs. 13%), despite carrying meaningfully worse FICO, DTI, and income profiles — raising the question of whether risk is being priced correctly.

📄 📄 *Full breakdown with supporting numbers in the [PDF case study](./LendingClub_Case_Study.pdf#page=8).*

<br>

## 🖼️ Dashboard Preview

### 1️⃣ Risk Analysis
Breaks down default rate by loan purpose, DTI band, FICO band, and loan grade — pinpointing exactly which borrower segments carry disproportionate risk.

<p align="center"><img src="DashboardScreenshots/Risk_ananlysis.png" width="800"></p>

### 2️⃣ Portfolio Growth
Tracks origination volume, funded amount, and average loan size from 2007–2018, plus a breakdown of what's driving growth by loan purpose.

<p align="center"><img src="DashboardScreenshots/Portfolio_growth.png" width="800"></p>

### 3️⃣ Borrower Profile
A direct side-by-side comparison of Fully Paid vs. Charged Off borrowers across income, DTI, FICO, revolving balance, interest rate, and credit utilisation.

<p align="center"><img src="DashboardScreenshots/Borrower_profile.png" width="650"></p>

<br>

## 🛠️ Tech Stack & Pipeline

```
Raw CSV (890K+ rows, 74+ columns)
        │
        ▼
 🐍 Python (Pandas, NumPy)     →  Clean, filter, engineer features
        │
        ▼
 ⚡ Power Query                 →  Segment into bands, build Date table
        │
        ▼
 📐 DAX Measures                →  KPIs, YoY growth, risk comparisons
        │
        ▼
 📊 Power BI Dashboard          →  3-page interactive report
```

| Stage | Tool | What happened |
|---|---|---|
| Data Cleaning | **Python** (Pandas, NumPy) | Filtered to resolved loans, handled nulls, engineered `avg_fico` and `default_flag` |
| Transformation | **Power Query** | Built 5 segmentation bands (DTI, FICO, income, loan size, utilisation) + Date table |
| Metrics | **DAX** | 15+ measures — core KPIs, YoY growth, Charged Off vs. Fully Paid comparisons |
| Visualization | **Power BI** | 3-page dashboard with custom theming, navigation, and tooltips |

<br>

## 🧹 Data Cleaning (Python)

The raw dataset (`accepted_2007_to_2018Q4.csv`) was trimmed to 26 relevant columns at read time, then cleaned in four steps: filtered to loans with a resolved outcome (*Fully Paid* / *Charged Off* only), nulls dropped only in four critical columns, dates converted, and two features engineered — `avg_fico` (midpoint of the FICO range) and `default_flag` (the binary target).

<details>
<summary><b>▶ Show full cleaning script</b></summary>

```python
## Import Libraries
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

file_name = 'Data/accepted_2007_to_2018Q4.csv'

features = ['id', 'loan_amnt', 'term', 'int_rate', 'installment',
            'grade', 'sub_grade', 'emp_length', 'home_ownership', 'annual_inc',
            'verification_status', 'issue_d', 'loan_status', 'purpose',
            'fico_range_high', 'fico_range_low', 'dti',
            'earliest_cr_line', 'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc',
            'application_type', 'mort_acc', 'pub_rec_bankruptcies']

df = pd.read_csv(file_name, usecols=features, low_memory=True)

# 1. Filter for completed loans only (definitive outcomes)
target_statuses = ['Fully Paid', 'Charged Off']
df = df[df['loan_status'].isin(target_statuses)]

# 2. Drop rows with nulls in critical columns only
critical_cols = ['emp_length', 'dti', 'revol_util', 'annual_inc']
df.dropna(subset=critical_cols, inplace=True)

# 3. Data type conversions
df['issue_d'] = pd.to_datetime(df['issue_d'])
df['earliest_cr_line'] = pd.to_datetime(df['earliest_cr_line'])

# 4. Feature engineering
df['avg_fico'] = (df['fico_range_high'] + df['fico_range_low']) / 2
df.drop(columns=['fico_range_high', 'fico_range_low'], inplace=True)

df['default_flag'] = np.where(df['loan_status'] == 'Charged Off', 1, 0)

df.to_csv('cleaned_data.csv', index=False)
```

</details>

<br>

## ⚙️ Feature Engineering (Power Query)

Continuous fields were binned into categorical bands to make segment-level risk patterns visible in the dashboard:

| Column | Based on | Bands |
|---|---|---|
| `dti_band` | Debt-to-income | Low (<10), Medium (10–20), High (20–30), Very High (30+) |
| `fico_band` | FICO score | Poor (<650), Fair (650–699), Good (700–749), Excellent (750+) |
| `Income_tier` | Annual income | Low (<40K), Middle (40K–80K), Upper-Mid (80K–120K), High (120K+) |
| `Loan_bucket` | Loan amount | Small (<5K), Medium (5K–15K), Large (15K–25K), Very Large (25K+) |
| `revol_util_band` | Revolving utilisation | Low (<25%), Medium (25–50%), High (50–75%), Very High (75%+) |

A dedicated **Date table** was also built (rather than relying on the loan table's dates directly) to enable correct DAX time-intelligence for YoY growth and running totals:

```powerquery
= List.Dates(#date(2007,1,1),
             Duration.Days(#date(2018,12,31) - #date(2007,1,1)) + 1,
             #duration(1,0,0,0))
```

<br>

## 📐 DAX Measures

<details>
<summary><b>▶ Show core measures</b></summary>

```dax
Total Loans = COUNT('Loans'[id])

Total Funded Amount = SUM('Loans'[loan_amnt])

Total Defaults = SUM(Loans[default_flag])

Default Percentage = AVERAGE(Loans[default_flag])

Average Loan Amount = DIVIDE([Total Funded Amount], [Total Loans])

YoY Funded Growth % =
VAR CurrentYear = SUM(Loans[loan_amnt])
VAR LastYear =
    CALCULATE(
        SUM(Loans[loan_amnt]),
        FILTER(
            ALL(Loans[Issued_year]),
            Loans[Issued_year] = MAX(Loans[Issued_year]) - 1
        )
    )
RETURN
    DIVIDE(CurrentYear - LastYear, LastYear) * 0.1
```

</details>

<details>
<summary><b>▶ Show Charged Off vs. Fully Paid comparison measures</b></summary>

```dax
Avg FICO - Charged Off =
CALCULATE(AVERAGE(Loans[avg_fico]), Loans[loan_status] = "Charged Off")

Avg FICO - Fully Paid =
CALCULATE(AVERAGE(Loans[avg_fico]), Loans[loan_status] = "Fully Paid")

Avg DTI - Charged Off =
CALCULATE(AVERAGE(Loans[dti]), Loans[loan_status] = "Charged Off")

Avg DTI - Fully Paid =
CALCULATE(AVERAGE(Loans[dti]), Loans[loan_status] = "Fully Paid")

Avg Income - Charged Off =
CALCULATE(AVERAGE(Loans[annual_inc]), Loans[loan_status] = "Charged Off")

Avg Income - Fully Paid =
CALCULATE(AVERAGE(Loans[annual_inc]), Loans[loan_status] = "Fully Paid")

Avg Interest - Charged Off =
CALCULATE(AVERAGE(Loans[int_rate]), Loans[loan_status] = "Charged Off") * 0.01

Avg Interest - Fully Paid =
CALCULATE(AVERAGE(Loans[int_rate]), Loans[loan_status] = "Fully Paid") * 0.01

Avg Revol Util - Charged Off =
CALCULATE(AVERAGE(Loans[revol_util]), Loans[loan_status] = "Charged Off") * 0.01

Avg Revol Util - Fully Paid =
CALCULATE(AVERAGE(Loans[revol_util]), Loans[loan_status] = "Fully Paid") * 0.01
```

</details>

<br>

## 🎨 Design Details

The dashboard's look was deliberately built rather than left to Power BI defaults — a small detail that separates a portfolio piece from a default template.

- **Brand-matched palette** — Navy (`#233D4D`) and Orange (`#FE7F2D`), pulled directly from LendingClub's own branding
- **Custom navigation** — built with Power BI's Navigator, active page highlighted in orange
- **Custom tooltips** — black background, orange values, replacing Power BI's default white tooltip box

<p align="center"><img src="DashboardScreenshots/Tool_tip.png" width="450"></p>

- **Custom in-bar chart labels** — the *Default Percentage by Purpose* chart uses a zero-value placeholder measure to create bar spacing, plus a DAX-built label placed directly on each bar instead of the default axis-end label:

<p align="center"><img src="DashboardScreenshots/PurposeVsDefault.png" width="300"></p>

<br>

## 💡 Business Recommendations

- **Tighten underwriting on high-risk purpose categories** — Small Business, Renewable Energy, and Moving loans default well above the portfolio average.
- **Re-examine the interest rate premium** — the current 3-point gap between Fully Paid and Charged Off borrowers may not fully price in their DTI, FICO, and income gap.
- **Use DTI and FICO bands as early screening signals** — both show a clean, monotonic relationship with default risk.
- **Monitor concentration risk in debt consolidation** — $11B of $18.5B total funded sits in a single loan purpose.
- **The existing grading system is well-calibrated** — Grade A→G shows a near-linear risk escalation, validating LendingClub's own risk model.

<br>

## 📁 Repository Structure

```text
├── .gitignore
├── README.md
├── LC_report.pdf
├── lending_club_dashboard.pbix
│
├── Dashboard_Screenshots/
│   ├── Borrower_profile.png
│   ├── Portfolio_growth.png
│   ├── PurposeVsDefault.png
│   ├── Risk_ananlysis.png
│   └── Tool_tip.png
│
├── Canvas_background/
│   └── ...
│
└── Data/
    └── accepted_2007_to_2018Q4.csv    # Raw dataset (not included in GitHub)
```



> 📦 **Dataset:** Sourced from [LendingClub's public loan data on Kaggle](https://www.kaggle.com/datasets/wordsforthewise/lending-club). Not included in this repo due to file size — download separately and place in `/data`.

<br>

## 🚀 Reproducing This Project

1. Download the **Lending Club accepted loans dataset** from Kaggle and place `accepted_2007_to_2018Q4.csv` inside the local `Data/` folder.

2. Open `lending_club_dashboard.pbix` in **Power BI Desktop**.

3. Update the data source path if required so Power BI points to the local dataset.

4. Refresh the Power BI dashboard to load the data and reproduce the analysis.

> **Note:** The raw dataset and cleaned dataset are not included in this repository because of their large file sizes. The dataset remains in the local `Data/` folder and is excluded through `.gitignore`.


<br>

## 🧠 Skills Demonstrated

`Python` `Pandas` `NumPy` `Data Cleaning` `Feature Engineering` `Power Query` `DAX` `Power BI` `Data Visualization` `Dashboard Design` `Credit Risk Analysis` `Business Analytics`

<br>

<div align="center">

### 📬 Let's Connect

**[Ghantasala Nani Babu]** — Data Analyst  
[LinkedIn](https://www.linkedin.com/in/ghantasala-nani-babu-b87760255/) &nbsp;•&nbsp; [Portfolio](https://github.com/naanibabu) &nbsp;•&nbsp; [Email](mailto:ghantasalananibabu@gmail.com)

*If this project is useful or interesting, a ⭐ on the repo is appreciated!*

</div>
