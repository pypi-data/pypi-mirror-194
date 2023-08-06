import sqlite3


def create_test_results_table(conn):
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_version TEXT NOT NULL,
            device_model TEXT NOT NULL,
            os_version TEXT NOT NULL,
            test_name TEXT NOT NULL,
            test_runtime TEXT NOT NULL,
            test_last_result TEXT NOT NULL,
            number_of_fails INTEGER NOT NULL,
            number_of_passes INTEGER NOT NULL
        )
    """)
    conn.commit()

def test_create_test_results_table():
    conn = sqlite3.connect("test_results.db")
    create_test_results_table(conn)
    conn.close()


def insert_test_result(conn, app_version, device_model, os_version, test_name, test_runtime, test_last_result,
                       number_of_fails, number_of_passes):
    c = conn.cursor()
    c.execute("""
        INSERT INTO test_results (app_version, device_model, os_version, test_name, test_runtime, test_last_result, number_of_fails, number_of_passes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (app_version, device_model, os_version, test_name, test_runtime, test_last_result, number_of_fails,
          number_of_passes))
    conn.commit()


def test_insert_test_result():
    conn = sqlite3.connect("test_results.db")
    insert_test_result(conn, "1.0", "Google Pixel 4", "11", "Login Test", "2023-02-10 10:00:00", "PASS", 0, 1)
    conn.close()


def retrieve_test_results(conn, test_name=None, test_last_result=None, limit=None):
    c = conn.cursor()
    query = "SELECT * FROM test_results"
    params = []
    if test_name is not None:
        query += " WHERE test_name=?"
        params.append(test_name)
    if test_last_result is not None:
        if len(params) == 0:
            query += " WHERE test_last_result=?"
        else:
            query += " AND test_last_result=?"
        params.append(test_last_result)
    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)
    c.execute(query, params)
    return c.fetchall()


def test_retrieve_test_results():
    conn = sqlite3.connect("test_results.db")
    results = retrieve_test_results(conn, test_last_result="PASS", limit=5)
    for result in results:
        print(result)
    conn.close()


def check_for_missing_data(test_results):
    missing_data = []
    for test_result in test_results:
        for i, value in enumerate(test_result):
            if value is None:
                missing_data.append((i, test_result))
                break
    return missing_data


def test_check_for_missing_data():
    conn = sqlite3.connect("test_results.db")
    test_results = retrieve_test_results(conn)
    missing_data = check_for_missing_data(test_results)
    for missing_datum in missing_data:
        print(missing_datum)
    conn.close()


def get_missing_data(test_results):
    missing_data = []
    for test_result in test_results:
        for i, value in enumerate(test_result):
            if value is None:
                missing_data.append(test_result)
                break
    return missing_data


def test_get_missing_data():
    conn = sqlite3.connect("test_results.db")
    test_results = retrieve_test_results(conn)
    missing_data = get_missing_data(test_results)
    for missing_datum in missing_data:
        print(missing_datum)
    conn.close()

