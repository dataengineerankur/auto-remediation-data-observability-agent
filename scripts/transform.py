"""Example transformation script.

This script demonstrates a simple transformation that references certain columns
in the input DataFrame. It's used by the auto-remediation agent example to
illustrate how schema drift might require updates to transformation logic.
"""

import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Add a processed full_name column based on the existing 'name' column."""
    df = df.copy()
    df["full_name"] = df["name"] + " processed"
    return df


if __name__ == "__main__":
    # Example usage: create a simple DataFrame and run the transformation
    import pandas as pd  # noqa: F401 (imported for example code)

    sample_df = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"], "age": [25, 30]})
    print(transform(sample_df))
