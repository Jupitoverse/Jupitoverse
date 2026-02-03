# 4. Data Analytics & Python Data Science Stack – Interview Guide

Skills covered: Data Analytics, Pandas, NumPy, Matplotlib, Scikit-learn

---

## 📋 Quick Reference

| Tool | Purpose |
|------|---------|
| Pandas | DataFrames, EDA, cleaning, aggregation, time series |
| NumPy | Arrays, numerical ops, broadcasting, linear algebra |
| Matplotlib | Plotting (line, bar, scatter, histograms, subplots) |
| Scikit-learn | ML: train/test split, models, preprocessing, metrics, pipelines |

---

## 🔑 Core Concepts

### 1. Pandas

- DataFrame: 2D labeled structure (rows + columns); index and column names.
- Series: 1D labeled array; single column of a DataFrame.
- Common ops: `read_csv`, `dropna`, `fillna`, `groupby`, `merge`, `pivot`, `value_counts`, `describe`.
- Indexing: `.loc[]` (label), `.iloc[]` (integer); boolean indexing with masks.

```python
# Conceptual
import pandas as pd
df = pd.read_csv("data.csv")
df.groupby("category")["value"].mean()
df.dropna(subset=["col"])
df.merge(other, on="key")
```

### 2. NumPy

- ndarray: Homogeneous typed array; fast element-wise and linear algebra ops.
- Broadcasting: Rules for combining arrays of different shapes (e.g. scalar + array, (n,) + (n,1)).
- Common ops: `np.array`, `reshape`, `dot`, `sum`, `mean`, `std`, slicing, boolean indexing.

```python
import numpy as np
a = np.array([[1, 2], [3, 4]])
a.mean(axis=1)  # row means
np.dot(a, a.T)
```

### 3. Matplotlib

- Figure & Axes: `fig, ax = plt.subplots()`; plot on `ax`.
- Plot types: `ax.plot`, `ax.bar`, `ax.scatter`, `ax.hist`, `ax.boxplot`.
- Best practices: Label axes, title, legend; use `fig.tight_layout()`; save with `fig.savefig()`.

### 4. Scikit-learn

- Workflow: Split (train_test_split) → preprocess (StandardScaler, etc.) → fit model → predict → evaluate (accuracy, F1, RMSE).
- Preprocessing: StandardScaler, MinMaxScaler, OneHotEncoder, LabelEncoder, Imputer.
- Models: LinearRegression, LogisticRegression, RandomForest, XGBoost (via sklearn API or xgboost), KMeans.
- Pipeline: Chain preprocessing + model with `Pipeline(steps=[...])` for clean, reproducible flows.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
pipe = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression())])
pipe.fit(X_train, y_train)
pipe.score(X_test, y_test)
```

---

## 💡 Top 15 Interview Q&A – Data Analytics & DS Stack

Q1: What is the difference between Pandas Series and DataFrame?
> "Series is 1D with a single index; DataFrame is 2D with row and column indices. A DataFrame column is a Series. Series is for one variable; DataFrame for a table."

Q2: When do you use .loc vs .iloc?
> ".loc uses label-based indexing (index/column names); .iloc uses integer positions. Use .loc for named access, .iloc when you only care about position (e.g. first 10 rows)."

Q3: How do you handle missing values in Pandas?
> "Inspect with isnna()/isnull(), dropna() to remove, fillna() with constant/mean/forward-fill. Choice depends on amount of missingness and whether it’s MCAR/MAR/MNAR."

Q4: What is groupby and when do you use it?
> "groupby splits the DataFrame by one or more columns, then we apply an aggregation (sum, mean, count). Use it for segment-level stats, e.g. revenue by region or counts by category."

Q5: Explain merge vs join in Pandas.
> "merge is the main function for SQL-like joins (inner, left, right, outer) on columns or index. join is a convenience for joining on index. I use merge for explicit key columns."

Q6: What is NumPy broadcasting?
> "Rules that let you combine arrays of different shapes without explicit loops. For example, (n,) + (m,1) gives (m,n). Dimensions are aligned from the right; size 1 can be broadcast."

Q7: What is the difference between NumPy array and Python list?
> "NumPy arrays are homogeneous, fixed type, and support vectorized ops and broadcasting. Lists are heterogeneous and flexible. For numerical work, NumPy is much faster and more compact."

Q8: How do you choose a metric for classification?
> "Accuracy when classes are balanced. For imbalanced data: precision/recall, F1, or AUC-ROC. Precision when false positives are costly; recall when false negatives are costly."

Q9: What is overfitting and how do you reduce it?
> "Model fits training data too closely and fails on new data. Mitigations: more data, simpler model, regularization (L1/L2), cross-validation, early stopping, pruning (trees), dropout (DL)."

Q10: What is train_test_split and why use it?
> "Splits data into train and test sets (e.g. 80/20) so we evaluate on unseen data. Use random_state for reproducibility. For time series, use a temporal split."

Q11: What is a Pipeline in scikit-learn?
> "A Pipeline chains transformers and a final estimator. Fit applies each step in order; transform flows through. Benefits: no data leakage, single fit/predict interface, easier deployment."

Q12: What is StandardScaler and when to use it?
> "StandardScaler subtracts mean and divides by std (per feature). Use when features have different scales and the model is scale-sensitive (e.g. regression, SVM, KNN). Fit on train only, then transform train and test."

Q13: How do you evaluate a regression model?
> "RMSE or MSE for scale of errors; MAE for robustness; R² for explained variance. I report RMSE and R² and use cross-validation to avoid overfitting to one split."

Q14: What is the bias–variance tradeoff?
> "Bias: error from wrong assumptions (underfitting). Variance: error from sensitivity to training data (overfitting). Simple models: high bias, low variance. Complex models: low bias, high variance. We tune to balance."

Q15: How does Gen AI / RAG relate to your data analytics experience?
> "RAG needs good data: chunking, cleaning, and sometimes analytics on query/usage patterns. I use Pandas for EDA on logs and retrieval quality; NumPy for embedding/vector ops; and the same rigor for evaluation metrics and A/B analysis."

---

## 📊 Key Talking Points

- Pandas: DataFrame/Series, indexing, missing values, groupby, merge, EDA.
- NumPy: Arrays, broadcasting, vectorized ops, performance.
- Matplotlib: Figure/axes, common plot types, clear labels and legends.
- Scikit-learn: Split → preprocess → fit → evaluate; pipelines; choice of metrics and regularization.

---

## 📁 See Also

- [1_Core_GenAI_RAG_LLM.md](1_Core_GenAI_RAG_LLM.md) – RAG evaluation and metrics  
- [0_GEN_AI_MASTER_INDEX.md](0_GEN_AI_MASTER_INDEX.md) – Master index  
