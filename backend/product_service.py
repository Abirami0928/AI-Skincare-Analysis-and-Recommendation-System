import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "skincare_products.csv"

# Load skincare dataset
df = pd.read_csv(DATA_PATH)

# Convert price into INR
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("£", "", regex=False)
    .str.strip()
)

df["price"] = pd.to_numeric(df["price"], errors="coerce")

exchange_rate = 126.63
df["Price_INR"] = df["price"] * exchange_rate

# Apply the same price filtering as your notebook
df = df.dropna(subset=["Price_INR"])
df = df[df["Price_INR"] <= 7000].copy()

# Clean ingredients
df["ingredients_clean"] = (
    df["ingredients"]
    .fillna("")
    .astype(str)
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
)

def recommend_products_scored(
    skin_label,
    budget=1000,
    product_type=None,
    ingredient_keywords=None,
    top_n=5
):
    results = df.copy()

    results = results[
        results["Price_INR"] <= budget
    ].copy()

    if product_type:
        results = results[
            results["product_type"].str.lower()
            == product_type.lower()
        ].copy()

    keywords = [
        word.lower()
        for word in (ingredient_keywords or [])
    ]

    if keywords:
        results["ingredient_matches"] = results[
            "ingredients_clean"
        ].apply(
            lambda text: sum(
                keyword in text for keyword in keywords
            )
        )

        results = results[
            results["ingredient_matches"] > 0
        ].copy()
    else:
        results["ingredient_matches"] = 0

    results = results.sort_values(
        ["ingredient_matches", "Price_INR"],
        ascending=[False, True]
    )

    results["rank"] = range(1, len(results) + 1)

    return results[
        [
            "rank",
            "product_name",
            "product_type",
            "Price_INR",
            "ingredient_matches",
            "ingredients_clean",
            "product_url"
        ]
    ].head(top_n).to_dict(orient="records")