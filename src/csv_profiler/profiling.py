from __future__ import annotations

''' old basic profile function
def basic_profile(rows: list[dict[str, str]], source: str | None = None) -> dict:
    row_count = len(rows)

    if row_count == 0:
        return {
            "source": source,
            "summary": {"rows": 0, "columns": 0},
            "columns": {},
        }

    col_names = list(rows[0].keys())

    report_columns: dict[str, dict] = {}

    for col in col_names:
        values = [row.get(col, "") for row in rows]

        col_type = infer_type(values)  

        if col_type == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)

        report_columns[col] = {
            "type": col_type,
            **stats,
        }

    return {
        "source": source,
        "summary": {
            "rows": row_count,
            "columns": len(col_names),
        },
        "columns": report_columns,
    }
'''

''' old basic_profile function 
def basic_profile(rows: list[dict[str, str]]) -> dict:
    """Compute row count, column names, and missing values per column."""
    """This is the old one from day 1, i upgrade it"""

    row_count = len(rows)

    if row_count == 0:
        return {
            "row_count": 0,
            "columns": [],
            "missing": {},
        }

    columns = list(rows[0].keys())

    missing = {column: 0 for column in columns}

    for row in rows:
        for column in columns:
            value = row.get(column, "")
            if value.strip() == "":
                missing[column] += 1

    return {
        "row_count": row_count,
        "columns": columns,
        "missing": missing,
    }
    '''

def profile_rows(rows: list[dict[str, str]]) -> dict:
    n_rows = len(rows)
    columns = list(rows[0].keys())
    col_profiles = []

    for col in columns:
        values = [r.get(col, "") for r in rows]
        usable = [v for v in values if not is_missing(v)]
        missing = len(values) - len(usable)
        inferred = infer_type(values)
        unique = len(set(usable))

        profile = {
            "name": col,
            "type": inferred,
            "missing": missing,
            "missing_pct": 100.0 * missing / n_rows if n_rows else 0.0,
            "unique": unique,
        }

        if inferred == "number":
            nums = [try_float(v) for v in usable]
            nums = [x for x in nums if x is not None]
            if nums:
                profile.update({
                    "min": min(nums),
                    "max": max(nums),
                    "mean": sum(nums) / len(nums),
                })

        col_profiles.append(profile)

    return {
        "n_rows": n_rows,
        "n_cols": len(columns),
        "columns": col_profiles,
    }

MISSING = {"", "na", "n/a", "null", "none", "nan"}

def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().casefold() in MISSING


def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"

    for v in usable:
        if try_float(v) is None:
            return "text"

    return "number"

def column_values (rows: list[dict[str, str]], col: str) -> list[str]:
  values = []
  
  for row in rows:
    value = row.get(col, "")
    values.append(value)
  
  return values

def numeric_stats(values: list[str]) -> dict:
  usable = [v.strip() for v in values if not is_missing(v)]
  if not usable:
    return {}
  
  nums =[try_float(v) for v in usable]

  return {
        "count": len(nums),
        "unique": len(set(nums)),
        "mean": sum(nums) / len(nums),
        "min": min(nums),
        "max": max(nums),} 

def text_stats(values: list[str], top_k: int = 5) -> dict:
    missing = 0
    usable: list[str] = []

    usable = [v.strip() for v in values if not is_missing(v)]
    missing = len(values) - len(usable)


    counts: dict[str, int] = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1

    top = sorted(
        counts.items(),
        key=lambda kv: kv[1],
        reverse=True
    )[:top_k]

    return {
        "count": len(usable),
        "missing": missing,
        "unique": len(counts),
        "top": top,
    }

