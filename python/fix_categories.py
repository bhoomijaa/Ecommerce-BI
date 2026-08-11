import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/cleaned")

products = pd.read_csv(
    CLEAN_DIR / "products_clean.csv"
)

translation = pd.read_csv(
    CLEAN_DIR / "category_translation_clean.csv"
)

# Find categories used by products but missing from translation table
product_categories = set(
    products["product_category_name"].dropna().unique()
)

translated_categories = set(
    translation["product_category_name"].dropna().unique()
)

missing_categories = product_categories - translated_categories

print("Missing categories:")
print(missing_categories)

# Add missing categories using the original category name
# as a fallback English label
for category in missing_categories:
    translation.loc[len(translation)] = [
        category,
        category
    ]

translation.to_csv(
    CLEAN_DIR / "category_translation_clean.csv",
    index=False
)

print(
    f"\nAdded {len(missing_categories)} missing categories."
)

print(
    f"Final translation rows: {len(translation)}"
)