import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# --- 1. SETUP & DATA LOADING ---
df = pd.read_excel("Store_data.xls")

# Display settings
pd.set_option("display.float_format", lambda x: "%.2f" % x)
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# Basic Data Inspection (Commented out for reference)
# print(df.shape)
# df.info()
# print("Duplicate rows:", df.duplicated().sum())

# --- 2. HIGH-LEVEL BUSINESS METRICS ---
print("\n--- High-Level Summary ---")
print(f"Total Sales: ${df['Sales'].sum():,.2f}")
print(f"Total Profit: ${df['Profit'].sum():,.2f}")
print(f"Total Quantity: {df['Quantity'].sum():,}")

# Filtering positive and negative profits for analysis
negative_profits = df[df["Profit"] < 0]
positive_profits = df[df["Profit"] > 0]


# --- 3. SUB-CATEGORY PROFIT / LOSS MARGIN (Horizontal Bar Chart) ---
plt.figure(figsize=(12, 6))
subcat_profit = df.groupby("Sub-Category")["Profit"].sum().sort_values()
colors = ["red" if x < 0 else "green" for x in subcat_profit]

subcat_profit.plot(kind="barh", color=colors)
plt.title(
    "Profit / Loss Margin by Sub-Category", fontsize=14, fontweight="bold"
)
plt.xlabel("Total Profit ($)")
plt.ylabel("Sub-Category")
plt.tight_layout()
plt.savefig("subcat_profit_loss.png", dpi=300, bbox_inches="tight")
plt.show()


# --- 4. MONTHLY SALES TREND ---
# Ensure Order Date is datetime type if not already
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("YearMonth")["Sales"].sum().reset_index()

plt.figure(figsize=(14, 6))
plt.plot(
    monthly_sales["YearMonth"],
    monthly_sales["Sales"],
    marker="o",
    color="b",
    linewidth=2,
)
plt.xticks(rotation=90)
plt.title(
    "Monthly Sales Trend (Spikes & Holidays)", fontsize=14, fontweight="bold"
)
plt.xlabel("Year-Month")
plt.ylabel("Total Sales ($)")
plt.tight_layout()
plt.savefig("monthly_sales_trend.png", dpi=300, bbox_inches="tight")
plt.show()


# --- 5. REGIONAL SALES & PROFIT (Grouped Bar Chart) ---
regional_sales = df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()

long_df = regional_sales.melt(
    id_vars="Region",
    value_vars=["Sales", "Profit"],
    var_name="Metric",
    value_name="Amount",
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=long_df,
    x="Region",
    y="Amount",
    hue="Metric",
    palette={"Sales": "blue", "Profit": "green"},
)
plt.title("Sales and Profit by Region", fontsize=14, fontweight="bold")
plt.xlabel("Region")
plt.ylabel("Amount ($)")
plt.tight_layout()
plt.savefig("regional_sales_profit.png", dpi=300, bbox_inches="tight")
plt.show()


# --- 6. IMPACT OF DISCOUNT ON AVERAGE PROFIT ---
discount_profit = df.groupby("Discount")["Profit"].mean()

plt.figure(figsize=(10, 6))
sns.lineplot(
    x=discount_profit.index * 100,
    y=discount_profit.values,
    marker="o",
    linewidth=2,
)
plt.axhline(y=0, color="red", linestyle="--", label="Zero Profit (Break-even)")
plt.title("Impact of Discount on Average Profit", fontsize=14, fontweight="bold")
plt.xlabel("Discount (%)")
plt.ylabel("Average Profit ($)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("Discount_analysis.png", dpi=300, bbox_inches="tight")
plt.show()


# --- 7. TOP 5 PROFITABLE VS TOP 5 LOSS-MAKING STATES ---
state_profit = df.groupby("State")["Profit"].sum()
top_states = state_profit.nlargest(5).sort_values()
loss_states = state_profit.nsmallest(5).sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

sns.barplot(
    x=top_states.values,
    y=top_states.index,
    hue=top_states.index,
    palette="Greens",
    legend=False,
    ax=axes[0],
)
axes[0].set_title("Top 5 Most Profitable States", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Total Profit ($)")
axes[0].set_ylabel("State")

sns.barplot(
    x=loss_states.values,
    y=loss_states.index,
    hue=loss_states.index,
    palette="Reds",
    legend=False,
    ax=axes[1],
)
axes[1].set_title("Top 5 Loss-Making States", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Total Profit ($)")
axes[1].set_ylabel("State")

plt.tight_layout()
plt.savefig(
    "profitable_and_loss_making_states.png", dpi=300, bbox_inches="tight"
)
plt.show()


# --- 8. SALES VS PROFIT BY SUB-CATEGORY (Scatter Plot) ---
subcat_analysis = df.groupby("Sub-Category")[["Sales", "Profit"]].sum()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=subcat_analysis, x="Sales", y="Profit", s=100, color="purple")
plt.axhline(y=0, color="red", linestyle="--", label="Break-even Line")

# Annotating specific points for clarity
for name, row in subcat_analysis.iterrows():
  if name in ["Envelopes", "Labels", "Tables", "Bookcases"]:
    plt.annotate(
        name,
        (row["Sales"], row["Profit"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
    )

plt.title("Sales vs Profit by Sub-Category", fontsize=14, fontweight="bold")
plt.xlabel("Total Sales ($)")
plt.ylabel("Total Profit ($)")
plt.legend()
plt.tight_layout()
plt.savefig("sales_vs_profit_subcategory.png", dpi=300, bbox_inches="tight")
plt.show()


# --- 9. SHIPPING MODE PERFORMANCE SUMMARY ---
shipping_summary = df.groupby("Ship Mode").agg(
    {"Sales": "sum", "Profit": "sum"}
)
shipping_summary["Profit Margin %"] = (
    shipping_summary["Profit"] / shipping_summary["Sales"]
) * 100

print("\n--- Shipping Mode Summary ---")
print(shipping_summary)