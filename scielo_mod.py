#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Modulo com rotinas auxiliares para acesso a scielo_db


# In[ ]:



# coding: utf-8


dbuser = 'neilor'
dbpassword = 'n1f2c3n1'
dbhost = 'localhost'
dbport = '5432'
dbname = 'scielo_db'



import os
import sys
import fnmatch
import re
import codecs
import psycopg2 as pg
import pandas as pd

pd.options.display.float_format = '{:,.2f}'.format


connect_cmd = f"dbname='{dbname}' user='{dbuser}' host='{dbhost}' password='{dbpassword}'"
postgres_url = f'postgresql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}'


def open_cursor(query):
    conn=pg.connect(connect_cmd)
    cur = conn.cursor()
    cur.execute(query)
    return cur

def close_cursor(cursor):
    cursor.close()
 

def execute_query(query):
    conn=pg.connect(connect_cmd)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


def pandas_query(sql_query):
    conn=pg.connect(connect_cmd)
    return pd.read_sql_query(sql_query,conn)
    conn.close

