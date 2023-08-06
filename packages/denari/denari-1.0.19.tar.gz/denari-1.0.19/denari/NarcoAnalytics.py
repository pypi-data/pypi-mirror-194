import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime as dt
slash = '/'
path = os.getcwd()
class NarcoAnalytics():
    #APPEARANCE
    def color_list(category_list,colors='basic'):
        sets = {'basic':['#FFA89E','#A4DEF5','#ACE1AD'],
                'one':['#60FA5A','#FF8791','#75AEFA','#FA69B9','#9B70A4','#FAF682','#FACC75'],
                'profit':['#60FA5A','#FF8791','#75AEFA'],
                'binary-p/b':['#75AEFA','#FA69B9']
               }
        a = len(category_list)
        col = ['lightslategray',] * a
        color_set = sets[colors]
        color_set = color_set[:a]
        for i in color_set:
            col[color_set.index(i)] = i
        return col
    
    #GENERAL
    def column_set(df,group,group_by,ascending=True):
        df = df.sort_values(group_by,ascending=ascending)
        a = pd.Series(df[group].unique()).tolist()
        return a
    
    #DATES/TIMES
    def set_dates(df:pd.DataFrame,date_name='date',date_index=False):
        #If date index == True...
        df[date_name] = pd.to_datetime(df[date_name], dayfirst = True)
        df.sort_values(by=date_name,inplace=True)           
        df.reset_index(inplace=True,drop=True)
        return df
    
    def tax_year(df,country_code='uk'):
        '''
        creates a tax year pd.Series
        '''
        dff = df.loc[:, ['date']].copy()
        tax = {'uk': {'start': '6-4', 'end': '5-4'},
               'usa': {'start': '1-1', 'end': '31-12'}
              }
        start = tax[country_code]['start']
        dff['start'] = start
        dff['year'] = dff['date'].dt.year.astype(str)
        dff['start date'] = dff['start'] + '-' + dff['year']
        dff['start date'] = pd.to_datetime(dff['start date'])
        dff['before_start'] = dff['date'] < dff['start date']
        dff['year'] = dff['year'].astype(int)
        dff['year before'] = dff['year'] - 1
        dff['year after'] = dff['year'] + 1
        dff['tax year'] = np.where(dff['before_start'],
                                   (dff['year before']).astype(str) + '/' + (dff['year']).astype(str),
                                   (dff['year']).astype(str) + '/' + (dff['year after']).astype(str))
        return dff['tax year']
    
    def split_dates(df:pd.DataFrame,date_column='date',format='period'):
        
        if format == 'period':
            new_columns = {'tax year':NarcoAnalytics.tax_year(df),
                           'year':pd.to_datetime(df[date_column]).dt.to_period('Y'),
                           'quarter':pd.to_datetime(df[date_column]).dt.to_period('Q'),
                           'month':pd.to_datetime(df[date_column]).dt.to_period('M'),
                           'week': pd.to_datetime(df[date_column]).dt.isocalendar().week,
                           'day':df[date_column].dt.day,
                           'weekday':df[date_column].dt.weekday
                           #'weekday':df[date_column].dt.day_name()
                          }
        elif format == 'numeric':
            new_columns = {'tax year':NarcoAnalytics.tax_year(df),
                           'year':df[date_column].dt.year,
                           'quarter':df[date_column].dt.quarter,
                           'month':df[date_column].dt.month,
                           'week':df[date_column].dt.isocalendar().week,
                           'day':df[date_column].dt.day,
                           'weekday':df[date_column].dt.weekday
                          }
        elif format == 'named_period':
            new_columns = {'tax year':NarcoAnalytics.tax_year(df),
                           'year':pd.to_datetime(df[date_column]).dt.to_period('Y'),
                           'quarter':pd.to_datetime(df[date_column]).dt.to_period('Q'),
                           'month':df[date_column].dt.month_name(),
                           'week':df[date_column].dt.isocalendar().week,
                           'day':df[date_column].dt.day,
                           'weekday':df[date_column].dt.day_name()
                          }
        elif format == 'named_numeric':
            new_columns = {'tax year':NarcoAnalytics.tax_year(df),
                           'year':df[date_column].dt.year,
                           'quarter':df[date_column].dt.quarter,
                           'month':df[date_column].dt.month_name(),
                           'week':df[date_column].dt.isocalendar().week,
                           'day':df[date_column].dt.day,
                           'weekday':df[date_column].dt.day_name()
                          }
        keys = list(new_columns.keys())
        for i in keys:
            df.insert(loc = 1,
                      column = i,
                      value = new_columns[i])
        return df
    
    def create_date_range(first_date,last_date="today",split_dates=True,split_format='named_numeric',date_index=False):
        #Date Index
        dates = pd.date_range(first_date,pd.to_datetime(last_date))
        date_range = pd.DataFrame(dates)
        date_range = date_range.rename(columns={0: 'date'})
        date_range['date'] = pd.to_datetime(date_range['date'])
        if date_index:
            date_range.set_index('date',inplace=True)
        if split_dates == True:
            date_range = split_dates(date_range,format=split_format)
        return date_range
    
    def filter_date_range_(data:pd.DataFrame,start_date,end_date):
        date_range = (data.index > start_date) & (data.index <= end_date)
        return data[date_range]
    
    def filter_date_range(df:pd.DataFrame, start_date, end_date, date_column='date'):
        if date_column not in df.columns:
            date_series = df.index
        else:
            date_series = df[date_column]
        df = df[(date_series >= start_date) & (date_series <= end_date)]
        return df
    
    def fill_dates(df,date_column='date'):
        '''
        Created with ChatGPT
        '''
        df_dates = NarcoAnalytics.create_date_range(df.iloc[0][date_column],split_dates=False,last_date=df.iloc[-1][date_column])
        # Set the date column as the index for both dataframes
        df = df.set_index('date')
        df_dates = df_dates.set_index('date')
        # Combine the dataframes using outer join and fill any missing values with values from df2
        df2 = df.join(df_dates, how='outer')
        # Reset the index of df
        df2 = df2.reset_index()
        # Sort the values by date
        df2 = df2.sort_values('date')
        return df2
    
    #METRICS
    def metric_n(df,group_by,number_column,metric):
        df2 = pd.DataFrame()
        met = {'sum':df2.groupby(df[group_by])[number_column].sum(number_column),
               'mean':df2.groupby(df[group_by])[number_column].mean(number_column),
               'max':df2.groupby(df[group_by])[number_column].mean(number_column),
               'min':df2.groupby(df[group_by])[number_column].min(number_column),
               'count':df2.groupby(df[group_by])[number_column].count().astype(int)
              }
        return met[metric]
    def metric_column_single(df,column_name,metric='sum'):
        met = {'sum':df[column_name].sum(),
               'mean':df[column_name].mean(),
               'max':df[column_name].mean(),
               'min':df[column_name].min(),
               'count':df[column_name].count().astype(int)
              }
        return met[metric]
    
    def metric_columns(df,metric='sum'):
        output = {'sum':df.sum(),
                  'mean':df.mean(),
                  'max':df.max(),
                  'min':df.min(),
                  'std':df.std(),
                  'var':df.var(),
                  'mode':df.mode(),
                  'count':df.count()
                 }
        df2 = output[metric]
        df2 = pd.DataFrame(df2)
        return df2
    
    #CASH FLOW
    def gross_profit(df,group_by,columns='r-e-p',custom_columns=[]):
        column_set = {'r-e-p':['revenue','expenditure','gross profit'],
                      'custom':custom_columns}
        columns_keep = column_set[columns]
        columns_keep.insert(0, group_by)
        df = df[columns_keep]

        met = {'sum':df.groupby(df[group_by]).sum(),
               'mean':df.groupby(df[group_by]).mean(),
               'max':df.groupby(df[group_by]).mean(),
               'min':df.groupby(df[group_by]).min(),
               'count':df.groupby(df[group_by]).count().astype(int)
              }

        df = met['sum']
        return df
    
    def cash_cumulate(df,expenditure=True,revenue=True,profit=True,gross_return=True):
        '''
        Requires Columns Named:
            'Expenditure'
            'Revenue'
            'Gross Profit'
            'Gross Return (%)'
        '''
        if revenue:
            df["cumulative revenue"] = df["revenue"].cumsum()
        if expenditure:
            df["cumulative expenditure"] = df["expenditure"].cumsum()
        if profit:
            df["cumulative profit"] = df["cumulative revenue"] - df["cumulative expenditure"]
        if gross_return:
            df["gross return (%)"] = df["cumulative profit"]/df["cumulative expenditure"] * 100
            df["gross return (%)"] = df["gross return (%)"].fillna(0)
        return df
    
    #AGGREGATE
    def aggregate_category(df,group_by,column_name,number_column,order_list,metric='sum'):
        '''
        level 1
        '''
        a = order_list
        b = []
        for i in a:
            s = df.loc[df[column_name] == i]
            met = {'sum':s.groupby(df[group_by])[number_column].sum(number_column),
                   'mean':s.groupby(df[group_by])[number_column].mean(number_column),
                   'max':s.groupby(df[group_by])[number_column].mean(number_column),
                   'min':s.groupby(df[group_by])[number_column].min(number_column),
                   'count':s.groupby(df[group_by])[number_column].count().astype(int)
                  }
            s = met[metric]
            b.append(s.rename(i))

        df = pd.concat(b, axis=1)
        df = df.fillna(0)
        df = df.sort_values(by=group_by)
        return df
    
    def graph_index_columns(df,colors='one',barmode='group'):
        '''
        level 2

        '''
        if df.index.dtype == 'period[M]':
                df.index = df.index.strftime("%Y-%m").to_list()
        col_names = df.columns.values.tolist()
        index_names = df.index.values.tolist()
        index_names = list(map(str, index_names))
        colors = NarcoAnalytics.color_list(col_names,colors=colors)
        bars = []
        for i in col_names:
            bar = go.Bar(name=i, x=index_names, y=df[i], marker_color=colors[col_names.index(i)])
            bars.append(bar)
        fig = go.Figure(bars)
        fig.update_layout(barmode=barmode)
        return fig
    
    def graph_metrics(df,graph_type='bar',colors='one'):
        index_names = df.index.values.tolist()
        index_names = list(map(str, index_names))
        values = df[0].tolist()
        colors = NarcoAnalytics.color_list(index_names,colors=colors)
        fig_type = {'pie': go.Pie(labels=index_names, values=values, marker_colors=colors, sort=False),
                    'bar': go.Bar(x=index_names, y=values, marker_color=colors)}
        fig = go.Figure(data=fig_type[graph_type])
        #if graph_type == 'pie':
            #fig = go.Figure(data=[go.Pie(labels=index_names, values=values, marker_colors=colors, sort=False)])
        return fig
    
    def metric(column,metric):
        if metric == 'sum':
            x = column.sum()
        elif metric == 'mean':
            x = column.mean()
        elif metric == 'max':
            x = column.max()
        elif metric == 'min':
            x = column.min()
        elif metric == 'std':
            x = column.std()
        elif metric == 'var':
            x = column.var()
        elif metric == 'mode':
            x = column.mode()
        elif metric == 'count':
            x = column.count()
        else:
            return 'error: incorrect metric input'
        return x