import sqlite3, os

for p in [r'D:\djang\db.sqlite3', r'D:\djang\Al_Ven\db.sqlite3']:
    print('DB:', p, 'exists' if os.path.exists(p) else 'MISSING')
    if os.path.exists(p):
        conn = sqlite3.connect(p)
        cur = conn.cursor()
        try:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%product%'")
            print('product tables:', [r[0] for r in cur.fetchall()])
            cur.execute("SELECT COUNT(*) FROM hello_products")
            print('hello_products count:', cur.fetchone()[0])
            cur.execute("SELECT id, name, image FROM hello_products ORDER BY id ASC")
            rows = cur.fetchall()
            print('total rows:', len(rows))
            print('first 5:', [(r[0], (r[1] or '')[:35], (r[2] or '')) for r in rows[:5]])
            print('last 5:', [(r[0], (r[1] or '')[:35], (r[2] or '')) for r in rows[-5:]])
            for d in [r'D:\djang\media', r'D:\djang\Al_Ven\media']:
                pp = os.path.join(d, 'products')
                if os.path.isdir(pp):
                    print(f'files in {pp}:', len(os.listdir(pp)))
        except Exception as e:
            print('ERR:', type(e).__name__, e)
        conn.close()
    print('---')
