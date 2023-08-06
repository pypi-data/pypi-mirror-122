from sqlalchemy import create_engine
import pandas as pd
import json
import psycopg2
import geopandas as gpd

### driver???
import psycopg2
import osgeo.ogr

import io



def getObj(json_file, pg_arguments):

    # read file
    with open(json_file, 'r') as myfile:
        data = myfile.read()

    # parse file
    obj = json.loads(data)

    ##### ----- keys ---------------------------------########################
    obj['pg_arguments_json'] = pg_arguments

    return(obj)



def getPGargs(obj):
    print('---getEngine(obj)---------')
    print(obj['pg_arguments_json'])

    # read file
    with open(obj['pg_arguments_json'], 'r') as myfile:
        data = myfile.read()

    # parse file
    json_obj = json.loads(data)
    print(json_obj)
    return json_obj



def getEngine(obj):
    print('---getEngine(obj)---------')
    print(obj['pg_arguments_json'])

    # read file
    with open(obj['pg_arguments_json'], 'r') as myfile:
        data = myfile.read()

    # parse file
    json_obj = json.loads(data)
    print(json_obj)

    engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(json_obj['username'],
                                                                     json_obj['password'],
                                                                     json_obj['host'],
                                                                     json_obj['port'],
                                                                     obj['pgdb']))
    print(engine)
    return engine



def getConn(obj):
    print('---def getConn(obj)---------')
    print(obj['pg_arguments_json'])

    # read file
    with open(obj['pg_arguments_json'], 'r') as myfile:
        data = myfile.read()

    # parse file
    json_obj = json.loads(data)
    print(json_obj)
    conn = psycopg2.connect(host=json_obj['host'], database=obj['pgdb'], user=json_obj['username'], password=json_obj['password'])

    print(conn)
    return conn

def pandasCSV_io(obj, df, schema, tablename):
    engine = getEngine(obj)

    # df = pd.read_csv(filepath, dtype = {"user_id": int})
    # df = pd.read_csv(filepath, nrows = 10000)



    df.columns = map(str.lower, df.columns)
    print('df-----------------------', df)

    df.head(0).to_sql(tablename, engine, schema=schema, index=False)#truncates the table

    # df = df.fillna(0)
    # df.fillna(value="", inplace=True)

    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep=',', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, '{0}.{1}'.format(schema, tablename), null="", sep=',') # null values become ''
    conn.commit()

    ###close things
    conn.close()
    cur.close()



def pandasCSV_io_multifile(obj, filepath1, filepath2, schema, tablename):
    engine = getEngine(obj)

    # df = pd.read_csv(filepath, dtype = {"user_id": int})
    # df = pd.read_csv(filepath, nrows = 10000)
    df1 = pd.read_csv(filepath1)
    df2 = pd.read_csv(filepath2)
    df = pd.concat([df1, df2])

    df.columns = map(str.lower, df.columns)
    print('df-----------------------', df)

    df.head(0).to_sql(tablename, engine, schema=schema, index=False)#truncates the table

    # df = df.fillna(0)
    df.fillna(value="", inplace=True)

    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep=',', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, '{0}.{1}'.format(schema, tablename), null="", sep=',') # null values become ''
    conn.commit()

    ###close things
    conn.close()
    cur.close()



def readSQLfile2DF(obj, sqlfile):

    engine = getEngine(obj)

    # Read the sql file
    query = open(sqlfile, 'r')

    # connection == the connection to your database, in your case prob_db
    df = pd.read_sql_query(query.read(), engine)
    print(' ########## readSQL from sqlfile ############## ', sqlfile)
    print(df)

    query.close()

    return df


def readSQLQuery2DF(obj, query):

    engine = getEngine(obj)

    # # Read the sql file
    # query = open(sqlfile, 'r')

    # connection == the connection to your database, in your case prob_db
    df = pd.read_sql_query(query, engine)
    # print(' ########## readSQL from sqlfile ############## ', sqlfile)
    print(df)

    # query.close()

    return df


def readSQL_format(obj, sqlfile, format_array):
    engine = getEngine(obj)

    # Read the sql file
    query = open(sqlfile, 'r')

    x = query.read()
    print(type(x))
    x_format = x.format(format_array[0], format_array[1])
    print(x_format)
    #
    # # connection == the connection to your database, in your case prob_db
    df = pd.read_sql_query(x_format, engine)
    # print(' ########## readSQL from sqlfile ############## ', sqlfile)
    # print(df)

    query.close()

    return df

def getGEO_DFfromQuery(obj, query, geom_col):
    conn = getConn(obj)

    # connection == the connection to your database, in your case prob_db
    # df = pd.read_sql_query(query, engine)

    df = gpd.GeoDataFrame.from_postgis(query, conn, geom_col)
    print('------------------ df from getDFfromQuery ------------------------------------------')
    print(df)

    return df


def exportToPG(obj, query):
    conn = getConn(obj)
    cursor = conn.cursor()
    cursor.execute(query)

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()


def exportToPGfromSQLfile(obj, sqlfile):

    conn = getConn(obj)
    cursor = conn.cursor()
    cursor.execute(open(sqlfile, "r").read())

    # Commit your changes in the database
    conn.commit()

    # Closing the connection
    conn.close()


def CSVtoDF(filepath, usecols):
    if usecols == 'all':
        cols = pd.read_csv(filepath, nrows=1).columns
        df = pd.read_csv(filepath, usecols=cols)
    else:
        df = pd.read_csv(filepath, usecols=usecols)
    return(df)



def exportDFtoPG(obj, df, schema, tablename):
    engine = getEngine(obj)

    df.to_sql(tablename, engine, schema)


def exportGEODFtoPG(obj, gdf, schema, tablename):
    engine = getEngine(obj)

    gdf.to_postgis(tablename, engine, schema)


def readFile(filepath):
    with open(filepath, 'r') as file:
        query = file.read().replace('\n', ' ')
        print(query)
        return query



def shapefileToPG_pandas(obj, filepath, schema, tablename):
    engine = getEngine(obj)
    gdf = gpd.read_file(filepath)
    print(gdf.crs)
    gdf = gdf.to_crs(gdf.crs)
    gdf.to_postgis(tablename, engine, schema)


def getColumnDict(layer):
    fields = layer.schema
    print('fields', fields)

    col_dict = {}
    for f in fields:
        type = f.GetType()
        type_name = f.GetFieldTypeName(type)
        col_dict[f.GetName()] = type_name
        # print(f.GetName())
        # print(type_name)

    print('col_dic:', col_dict)
    return col_dict


def getColumnArray(layer):
    fields = layer.schema
    print('fields', fields)

    col_array = []
    for f in fields:
        type = f.GetType()
        col_array.append(f.GetName())

    print('col_array:', col_array)
    return col_array


def records(layer):
    # generator
    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        yield json.loads(feature.ExportToJson())


def shapefileToPG_gdal(obj, srcFile):

    conn = getConn(obj)
    cursor = conn.cursor()

    shapefile = osgeo.ogr.Open(srcFile)
    layer = shapefile.GetLayer(0)
    print(layer)

    col_dict = getColumnArray(layer)

    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        wkt = feature.GetGeometryRef().ExportToWkt()
        print(wkt)


def fileToPG(obj, schema, tablename, filepath, type):
    print(filepath)
    if type == 'csv':
        df = pd.read_csv(filepath)
    if type == 'excel':
        df = pd.read_excel(filepath, sheet_name='data')

    #### format columns and remove newlines
    df.replace('\n', '', regex=True)
    print(df)
    exportDFtoPG(obj, df, schema, tablename)


def PGtoFile(obj, query, outfile):
    engine = getEngine(obj)
    df = pd.read_sql_query(query, con=engine)
    df.fillna(value="",
              inplace=True)
    df.to_csv(outfile, index=False)



def getFilesinDir(dirpath, wc):
    import glob
    return(glob.glob('{}/*{}'.format(dirpath, wc)))





def getColumnNames(filepath):
    # making data frame
    data = pd.read_csv(filepath)

    print(list(data.columns))










