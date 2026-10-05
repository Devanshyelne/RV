"""Create data/sample.csv with deliberate duplicates for testing."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 200
base = pd.DataFrame({
    "id": np.arange(1, n + 1),
    "name": [f"User {i}" for i in range(1, n + 1)],
    "email": [f"user{i}@example.com" for i in range(1, n + 1)],
    "city": rng.choice(["Mumbai", "Delhi", "Pune", "Chennai"], n),
    "amount": rng.integers(100, 5000, n),
})

# exact duplicates
exact = base.sample(15, random_state=1)
# messy duplicates: different case + extra spaces, same email
messy = base.sample(10, random_state=2).copy()
messy["email"] = messy["email"].str.upper() + " "
messy["name"] = "  " + messy["name"].str.lower()

df = pd.concat([base, exact, messy]).sample(frac=1, random_state=3).reset_index(drop=True)
df.to_csv("data/sample.csv", index=False)
print(f"Created data/sample.csv with {len(df)} rows")
