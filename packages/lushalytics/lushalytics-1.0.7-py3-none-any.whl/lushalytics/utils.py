
# delete egg, build and ditst (i think)
# update code
# update version
# python3 setup.py bdist_wheel
# python3 -m twine upload dist/*

from pyspark.sql import functions as F
import pyspark.sql.types as T
import plotly.express as px

# helper functions
def human_format(num):
    num = int(num)
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def freq_2_percent(df, colname, new_colname):
    # multiply by 100 and round
    df = df.withColumn(new_colname, F.round(F.col(f'{colname}')*100).cast("integer"))
    # convert to string and add '%'
    df = df.withColumn(new_colname, F.col(f'{new_colname}').cast("string"))
    df = df.withColumn(new_colname, F.concat(F.col(f'{new_colname}'), F.lit('%')))                   
    return df  

def counts_2_freqs(df, colname, new_colname):
    # create frequency
    df = df.withColumn(new_colname, F.col(f'{colname}') / df.agg(F.sum(f'{colname}')).collect()[0][0])         
    return df

def counts_2_percent(df, colname, new_colname):
    # create frequency
    df = df.withColumn(new_colname, F.col(f'{colname}') / df.agg(F.sum(f'{colname}')).collect()[0][0])
    # frequency to percent
    df = freq_2_percent(df, new_colname, new_colname)                
    return df

def counts_2_human_format(df, colname, new_colname):
    convertUDF = F.udf(lambda z: human_format(z), T.StringType())
    df = df.withColumn(new_colname, convertUDF(F.col(f'{colname}')))
    return df

def add_ticks_2_counts(df, colname, new_colname):
    df = df.withColumn(new_colname, F.format_number(F.col(f'{colname}'), 0))
    return df
 
def lower_col_names(self, df):
    for col in df.columns:
        df = df.withColumnRenamed(col, col.lower())
    return df   

class DF_formatter():

        def __init__(self):
            pass
            
        def freq_2_percent(self, df, cols, new_cols=False):
            if not new_cols:
                new_cols = cols
            for col, new_col in zip(cols, new_cols):
                df = freq_2_percent(df, col, new_col)
            return df

        def counts_2_freqs(self, df, cols, new_cols=False):
            if not new_cols:
                new_cols = cols
            for col, new_col in zip(cols, new_cols):
                df = counts_2_freqs(df, col, new_col)
            return df

        def counts_2_percent(self, df, cols, new_cols=False):
            if not new_cols:
                new_cols = cols
            for col, new_col in zip(cols, new_cols):
                df = counts_2_percent(df, col, new_col)
            return df
        
        def counts_2_human_format(self, df, cols, new_cols=False):
            if not new_cols:
                new_cols = cols
            for col, new_col in zip(cols, new_cols):
                df = counts_2_human_format(df, col, new_col)
            return df
        
        def add_ticks_2_counts(self, df, cols, new_cols=False):
            if not new_cols:
                new_cols = cols
            for col, new_col in zip(cols, new_cols):
                df = add_ticks_2_counts(df, col, new_col)
            return df
        
        def lower_col_names(self, df):
            for col in df.columns:
                df = df.withColumnRenamed(col, col.lower())
            return df   

def bar_chart(df, x_col, y_cols, text_cols=False, y_axis_title=False, legened_x=False, legened_y=False):
    
    # convert dataframe to pandas
    df_p = df.toPandas()
    
    # basic settings
    fig = px.bar(data_frame = df_p,
        x = x_col,
        y = y_cols,
        barmode = 'group')
    
    # add text labels
    if text_cols:
        for i, t in enumerate([df_p[text_cols[0]].tolist(), df_p[text_cols[1]].tolist()]):
            fig.data[i].text = t
            fig.data[i].textposition = 'outside'
    
    # font size
    fig.update_layout(
        font=dict(
            size=18
        ),
        yaxis_title=y_axis_title)
    
    # legend if needed
    if len(y_cols) > 1:
        fig.update_layout(
            legend=dict(
                x=legened_x,
                y=legened_y,
                traceorder="normal"))
        
    # ajust text position above bars
    fig.update_traces(textangle=0, textposition="outside", cliponaxis=False)

def str_to_list(df, colname, bracets=True):
    if bracets:
        df = df.withColumn(colname, F.split(F.regexp_replace(colname,'[\[\]"]',''),', '))
    else:
        df = df.withColumn(colname, F.split(colname,', '))
    return df

def get_column_max(df, col):
    return df.agg(F.max(f"{col}")).collect()[0][0]
def get_column_min(df, col):
    return df.agg(F.min(f"{col}")).collect()[0][0]
def get_column_mean(df, col):
    return df.agg(F.mean(f"{col}")).collect()[0][0]
def get_column_sum(df, col):
    return df.agg(F.sum(f"{col}")).collect()[0][0]
def get_column_std(df, col):
    return df.agg(F.stddev(f"{col}")).collect()[0][0]
def get_column_median(df, col):
    return df.agg(F.percentile_approx(f"{col}", 0.5)).alias("median").collect()[0][0]
def get_column_mode(df, col):
    return df.groupby(f"{col}").count().orderBy("count", ascending=False).first()[0]

def query_snowflake(spark_context, secrets, query):
    result = spark_context.read.format("snowflake")\
    .option("sfUrl", "wja95242.us-east-1.snowflakecomputing.com")\
    .option("sfUser", secrets['snowflake']["username"])\
    .option("sfPassword", secrets['snowflake']["password"])\
    .option("sfDatabase", "LUSHA")\
    .option("query", query).load()
    return result
