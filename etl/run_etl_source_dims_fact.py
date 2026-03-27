from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pyodbc


BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
SQL_DIR = BASE_DIR / "sql"
DEFAULT_INPUT = PROJECT_DIR / "Raw Data" / "earthquakes_raw.csv"


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None or value == "":
        raise ValueError(f"Missing environment variable: {name}")
    return value


def split_sql_batches(sql_text: str) -> list[str]:
    batches: list[str] = []
    buf: list[str] = []
    for line in sql_text.splitlines():
        if line.strip().upper() == "GO":
            chunk = "\n".join(buf).strip()
            if chunk:
                batches.append(chunk)
            buf = []
            continue
        buf.append(line)
    tail = "\n".join(buf).strip()
    if tail:
        batches.append(tail)
    return batches


def execute_sql_file(conn: pyodbc.Connection, sql_path: Path) -> None:
    text = sql_path.read_text(encoding="utf-8-sig")
    cur = conn.cursor()
    for batch in split_sql_batches(text):
        cur.execute(batch)
    cur.close()


def ensure_database(host: str, port: str, user: str, password: str, odbc_driver: str, database: str) -> None:
    conn_str = (
        f"DRIVER={{{odbc_driver}}};"
        f"SERVER={host},{port};"
        "DATABASE=master;"
        f"UID={user};PWD={password};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )
    with pyodbc.connect(conn_str, autocommit=True) as conn:
        conn.execute(f"IF DB_ID(N'{database}') IS NULL EXEC ('CREATE DATABASE [{database}]');")


def get_raw_columns(conn: pyodbc.Connection) -> list[str]:
    sql = """
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA='raw' AND TABLE_NAME='earthquake_raw'
    ORDER BY ORDINAL_POSITION
    """
    return [row[0] for row in conn.cursor().execute(sql).fetchall()]


def normalize_cell(val: object) -> object:
    if val is None:
        return None
    text = str(val).strip()
    if text == "" or text.lower() == "nan":
        return None
    return text


def load_raw_csv(conn: pyodbc.Connection, csv_path: Path) -> int:
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)

    raw_columns = get_raw_columns(conn)
    missing = [c for c in raw_columns if c not in df.columns]
    if missing:
        for col in missing:
            df[col] = None

    load_df = df[raw_columns]
    rows = [tuple(normalize_cell(v) for v in row) for row in load_df.itertuples(index=False, name=None)]

    col_expr = ", ".join(f"[{c}]" for c in raw_columns)
    qmarks = ", ".join("?" for _ in raw_columns)
    insert_sql = f"INSERT INTO raw.earthquake_raw ({col_expr}) VALUES ({qmarks})"

    cur = conn.cursor()
    cur.execute("DELETE FROM raw.earthquake_raw;")
    if rows:
        cur.fast_executemany = True
        cur.executemany(insert_sql, rows)
    cur.close()
    return len(rows)


def main() -> None:
    host = get_env("MSSQL_HOST", "localhost")
    port = get_env("MSSQL_PORT", "1433")
    database = get_env("MSSQL_DATABASE", "dep305_exp")
    user = get_env("MSSQL_USER", "sa")
    password = get_env("MSSQL_PASSWORD")
    odbc_driver = get_env("MSSQL_ODBC_DRIVER", "ODBC Driver 17 for SQL Server")

    input_csv = Path(os.getenv("EARTHQUAKE_INPUT_CSV", str(DEFAULT_INPUT))).resolve()
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")

    ensure_database(host, port, user, password, odbc_driver, database)

    conn_str = (
        f"DRIVER={{{odbc_driver}}};"
        f"SERVER={host},{port};"
        f"DATABASE={database};"
        f"UID={user};PWD={password};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )

    with pyodbc.connect(conn_str, autocommit=True) as conn:
        execute_sql_file(conn, SQL_DIR / "01_create_source.sql")
        execute_sql_file(conn, SQL_DIR / "02_create_dims_fact.sql")
        loaded_rows = load_raw_csv(conn, input_csv)
        execute_sql_file(conn, SQL_DIR / "03_load_dims_fact.sql")

        cur = conn.cursor()
        counts = {}
        for table in [
            "raw.earthquake_raw",
            "DW.dim_time",
            "DW.dim_location",
            "DW.dim_eqmagnitude",
            "DW.dim_intensity",
            "DW.dim_eqdepth",
            "DW.dim_tsunami",
            "DW.dim_volcano",
            "DW.fact_earthquake",
        ]:
            counts[table] = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        cur.close()

    print(f"Loaded raw rows: {loaded_rows}")
    for table, cnt in counts.items():
        print(f"{table}: {cnt}")


if __name__ == "__main__":
    main()


