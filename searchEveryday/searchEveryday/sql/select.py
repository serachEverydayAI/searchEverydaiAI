import sqlite3
import pandas as pd


def execute_query(query, params, conn):
    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()  # Return empty DataFrame in case of error

def getCrawledDataMas_WithAnchorDate_Keyword(anchor_date, keyword, conn):
    query = ("SELECT * FROM article_crawled_data_mas"
             " WHERE anchor_date = ? AND keyword = ?")
    return execute_query(query, (anchor_date, keyword), conn)

def getCrawledDataHis_WithAnchorDate_Keyword(reg_date, keyword, conn):
    query = ("SELECT * FROM article_crawled_data_his"
             " WHERE reg_date = ? AND keyword = ?")
    return execute_query(query, (reg_date, keyword), conn)

def getSeCustInfo_WithCi(cust_ci, conn):
    query = ("SELECT * FROM se_cust_info"
             " WHERE cust_ci = ?")
    return execute_query(query, (cust_ci, ), conn)

def getSeCustInfo_WithCust_id(cust_id, conn):
    query = ("SELECT * FROM se_cust_info"
             " WHERE cust_id = ?")
    return execute_query(query, (cust_id, ), conn)
