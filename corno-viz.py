# imports
import pandas as pd
import plotly_express as px
import chart_studio.plotly as py
import chart_studio as cs
from urllib.parse import unquote


confirmed_df = pd.read_csv(unquote(unquote('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv')))
del confirmed_df['Province/State']
confirmed_df.rename(columns={"Country/Region": "Region"},inplace=True)
confirmed_df = pd.melt(confirmed_df,id_vars=['Region','Lat','Long'], var_name='Day', value_name='ConfirmedCount')


recovered_df = pd.read_csv(unquote(unquote('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv')))
del recovered_df['Province/State']
recovered_df.rename(columns={"Country/Region": "Region"},inplace=True)
recovered_df = pd.melt(recovered_df,id_vars=['Region','Lat','Long'], var_name='Day', value_name='RecoveredCount')

death_df = pd.read_csv(unquote(unquote('https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv')))
del death_df['Province/State']
death_df.rename(columns={"Country/Region": "Region"},inplace=True)
death_df = pd.melt(death_df,id_vars=['Region','Lat','Long'], var_name='Day', value_name='DeathCount')

finaldf = confirmed_df.merge(recovered_df,on=["Region",'Lat','Long','Day'],how='left').merge(death_df,on=["Region",'Lat','Long','Day'],how='left')
del finaldf['Lat']
del finaldf['Long']

finaldf['Day'] = pd.to_datetime(finaldf['Day'])
group = finaldf.groupby(['Region','Day'])['RecoveredCount','DeathCount','ConfirmedCount'].sum().reset_index().sort_values('Day')
group['Day'] = group['Day'].astype(str)

fig = px.scatter(group,
           x="RecoveredCount",
           y="DeathCount",
           size="ConfirmedCount",
           size_max=60,
           color="Region",
           hover_name="Region",
           animation_frame="Day",
           animation_group="Region",
           log_x=True,
           range_x=[100, 100000],
           range_y=[0, 15000])
fig.show()