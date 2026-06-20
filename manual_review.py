import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    id,
    company_name
FROM companies
ORDER BY RANDOM()
LIMIT 5
"""

df = pd.read_sql(query, conn)

print("\n5 RANDOM COMPANIES\n")
print(df)

conn.close()

import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    company_id,
    COUNT(DISTINCT year) AS years
FROM profitandloss
GROUP BY company_id
ORDER BY years ASC
LIMIT 20
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()

import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    company_id,
    COUNT(DISTINCT year) AS years
FROM profitandloss
GROUP BY company_id
HAVING years < 5
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()