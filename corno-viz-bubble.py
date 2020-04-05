# imports
import pandas as pd
import plotly_express as px
import chart_studio.plotly as py
import chart_studio as cs
from urllib.parse import unquote
import plotly
import pycountry_convert as pc
import pycountry


def getcountrycode_from_name(country_name):
    # country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    # print(country_code)
    country_code = pc.country_name_to_country_alpha2(country_name)
    # country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_code

def country_to_continent(country_code):
    # country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    # print(country_code)
    country_continent_code = pc.country_alpha2_to_continent_code(country_code)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

def cleancountries(df):
   # cant find this region hence dropping
  df = df[df.Region != 'Diamond Princess']

  # these region names have to be changed which is understood by pycountry
  df.loc[df['Region'] == 'Taiwan*', ['Region']] = 'Taiwan'
  df.loc[df['Region'] == 'Korea, South', ['Region']] = 'Korea, Republic of'
  df.loc[df['Region'] == 'Holy See', ['Region']] = 'Holy See (Vatican City State)'
  df.loc[df['Region'] == 'Congo (Brazzaville)', ['Region']] = 'Congo'
  df.loc[df['Region'] == 'Congo (Kinshasa)', ['Region']] = 'Congo, The Democratic Republic of the'
  df.loc[df['Region'] == "Cote d'Ivoire", ['Region']] = 'Ivory Coast'
  return df


def getcountry_code(df):
  # cant find this region hence dropping
  df = df[df.Region != 'Diamond Princess']

  # these region names have to be changed which is understood by pycountry
  df.loc[df['Region'] == 'Taiwan*', ['Region']] = 'Taiwan'
  df.loc[df['Region'] == 'Korea, South', ['Region']] = 'Korea, Republic of'
  df.loc[df['Region'] == 'Holy See', ['Region']] = 'Holy See (Vatican City State)'
  df.loc[df['Region'] == 'Congo (Brazzaville)', ['Region']] = 'Congo'
  df.loc[df['Region'] == 'Congo (Kinshasa)', ['Region']] = 'Congo, The Democratic Republic of the'
  df.loc[df['Region'] == "Cote d'Ivoire", ['Region']] = 'Ivory Coast'

  list_country = [i.name for i in list(pycountry.countries)]
  # list_alpha_3 = [i.alpha_3 for i in list(pycountry.countries)]
  def country_flag(df):
      if (df['Region'] in list_country):
          return pycountry.countries.get(name=df['Region']).alpha_2
      else:
          # print(df['Region'])
          return 'Invalid Country'
  df['country_code']=df.apply(country_flag, axis = 1)
  return df

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

# finaldf = cleancountries(finaldf)
# finaldf['country_code']=finaldf['Region'].apply(getcountrycode_from_name)
# finaldf = getcountry_code(finaldf)
# print(finaldf['country_code'].unique())

# finaldf.loc[death_df['Region'] == 'Congo (Brazzaville)']

# finaldf['country_code'] = finaldf['Region'].apply(lambda x: pc.country_name_to_country_alpha2(x, cn_name_format="default"))

# finaldf = getcountry_code(finaldf)




# print(finaldf['country_code'].unique())
# print(finaldf.loc[finaldf['country_code'] == "Invalid Country"])

# print(country_to_continent('AF'))
# finaldf['continent_name']=finaldf['country_code'].apply(country_to_continent)

# finaldf['continent_name'] = finaldf['country_code'].apply(country_to_continent)
# finaldf['continent_code'] = pc.country_alpha2_to_continent_code(finaldf['country_code'])
# print(finaldf.loc[finaldf['country_code'] == "Unknown"])
# finaldf = finaldf[finaldf['Region'] == 'Congo Republic']

group = finaldf.groupby(['Region','Day'])['RecoveredCount','DeathCount','ConfirmedCount'].sum().reset_index().sort_values('Day')
group['Day'] = group['Day'].astype(str)
# print(group)
# print(group.columns)
# print(group['ConfirmedCount'].sum())
# print(group['RecoveredCount'].sum())
# print(group['DeathCount'].sum())



# locator = Nominatim(user_agent="myGeocoder")
# coordinates = "53.480837, -2.244914"
# location = locator.reverse(coordinates)
# print(location.raw)

# locator = Nominatim(user_agent=”myGeocoder”, timeout=10)
# rgeocode = RateLimiter(locator.reverse, min_delay_seconds=0.001)


# cc = countries.CountryChecker('TM_WORLD_BORDERS-0.3.shp')
# print(cc.getCountry(countries.Point(49.7821, 3.5708)).iso)
# print(getplace(51.1, 0.1))
# print(getplace(51.2, 0.1))
# print(getplace(51.3, 0.1))
# coordinates = (-37.81, 144.96), (31.76, 35.21)
# print(reverse_geocode.search(coordinates))

# finaldf = finaldf[finaldf['Region'] != 'Congo (Brazzaville)']
# finaldf.drop(finaldf.loc[death_df['Region'] == 'Congo (Brazzaville)'])



# finaldf['country_code'] = pc.country_name_to_country_alpha2(finaldf['Region'].astype(str), cn_name_format="default")
# print(finaldf['country_code'].unique())
# finaldf['continent_name'] = pc.country_alpha2_to_continent_code(finaldf['country_code'])
# print(finaldf['continent_name'].unique())


fig = px.scatter(group,
           x="RecoveredCount",
           y="DeathCount",
           size="ConfirmedCount",
           size_max=60,
           color = 'Region',
           hover_name="Region",
           animation_frame="Day",
           animation_group="Region",
           log_x=True,
           range_x=[100, 100000],
           range_y=[0, 15000])
fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False,title="Covid-19 Spread Globally",xaxis_title="Recovered Cases",yaxis_title="Death Cases",showlegend=False)
plotly.offline.plot(fig, filename='Covid-19 Spread Acceleration.html')
fig.show()