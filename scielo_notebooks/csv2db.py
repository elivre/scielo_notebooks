
# coding: utf-8

# In[13]:


import psycopg2 as pg
import csv
import os
import sys

def csv2db(dbname,schema,host,user,password,csvfile):
    connect_cmd='dbname="'+dbname+'" user="'+user+'" host="'+host+'" password="'+password+'"'
 
    try:
        conn = pg.connect(connect_cmd)
    except:
        print("Unable to connect to the database")

    cur = conn.cursor()

    # remove the path and extension and use what's left as a table name
    tablename = os.path.splitext(os.path.basename(csvfile))[0]
    if schema!='':
        tablename = schema+'.'+tablename

    with open(csvfile, "r") as f:
        reader = csv.reader(f,delimiter='|', quotechar='"')

        header = True
        for row in reader:
            if header:
                # gather column names from the first row of the csv
                header = False

                sql = "DROP TABLE IF EXISTS %s;" % tablename
                cur.execute(sql)
                sql = "CREATE TABLE %s (%s)" % (tablename,
                          ", ".join([ "%s varchar" % column for column in row ]))
                cur.execute(sql)
                conn.commit()

                for column in row:
                    if column.lower().endswith("_id"):
                        index = "%s__%s" % ( tablename, column )
                        sql = "CREATE INDEX %s on %s (%s)" % ( index, tablename, column )
                        cur.execute(sql)
                        conn.commit()
            else:
                insertsql = "INSERT INTO %s VALUES (E'%s')" % (tablename,"',E'".join( row))
                # skip lines that don't have the right number of columns
                cur.execute(insertsql)
                conn.commit()

    cur.close()
    conn.close()

