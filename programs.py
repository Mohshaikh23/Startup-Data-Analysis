import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from itertools import combinations
import networkx as nx



df= pd.read_csv('Startup_clean.csv')

def load_investor(investor):
    st.header(investor)
    
    col1,col2,col3,col4 = st.columns(4)

    with col1:
        investments_per_investor = round(df[df['Investors'].str.contains(investor)]['Startup'].value_counts().sum(),2)

        st.metric('No.of Investments Done',
                  investments_per_investor,
                  delta = 'Across '+ str(df[df['Investors'].str.contains(investor)]['City'].nunique())+' Cities',
                  border=True)
    
    with col2:
        investments_per_investor = round(df[df['Investors'].str.contains(investor)]['Amount'].sum().sum(),2)
        st.metric('Total Investments',
                  '₹ '+str(investments_per_investor)+' Cr',
                  delta = 'Across '+ str(df[df['Investors'].str.contains(investor)]['Vertical'].nunique())+' Verticals',
                  border=True)

    with col3:
        highest_investement = highest_investement = df[df['Investors'].str.contains('Sequoia')].groupby(['Startup','Round','Year','City'])['Amount'].sum().sort_values(ascending=False).head(1)
        st.metric('Highest Investment',
                  highest_investement.index[0][0],
                  delta = '₹ '+ str(highest_investement.values[0])+' Cr at '+str(highest_investement.index[0][1]),
                  border=True)
    with col4:
        st.metric('City with highest Funding',
                  highest_investement.index[0][3],
                  delta = 'on ' + str(highest_investement.index[0][2]),
                  border=True)

    col1,col2 =st.columns(2)
    with col1:
        last_5_Investments = df[df['Investors'].str.contains(investor)][['Date', 'Startup', 'Vertical','City','Round', 'Amount']]
        st.subheader('Most Recent Investments')
        st.dataframe(last_5_Investments,
                    hide_index=True)
    
    with col2:
        st.subheader('Investment Seasonality')
        seasonality = df[df['Investors'].str.contains(investor)].groupby(['month_name','month_num'],as_index=False)['Amount'].sum().sort_values('month_num')
        fig = px.bar(seasonality,
                     x=seasonality.month_name,
                     y=seasonality.Amount)
        st.plotly_chart(fig)

    col1,col2= st.columns(2)
    with col1:
        st.subheader('Top 10 Big investment')
        big_investments = df[df['Investors'].str.contains(investor)].groupby('Startup')['Amount'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(big_investments,
                     x=big_investments.index,
                     y=big_investments.values
                     )

        st.plotly_chart(fig)
    with col2:
        st.subheader('Vertical investments')
        big_investments = df[df['Investors'].str.contains(investor)].groupby('Vertical')['Amount'].sum().sort_values(ascending=False).head(10)
        fig = px.pie(names=big_investments.index,
                     values=big_investments.values)
        st.plotly_chart(fig)    

    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Round Wise Investment')
        Roundwise_investment = df[df['Investors'].str.contains(investor)].groupby('Round')['Amount'].sum().sort_values(ascending=False)
        fig = px.bar(big_investments,
                     x=Roundwise_investment.index,
                     y=Roundwise_investment.values
                     )
        st.plotly_chart(fig)  

    with col2:
        st.subheader('City Wise Investment')
        Citywise_investment = df[df['Investors'].str.contains(investor)].groupby('City')['Amount'].sum().sort_values(ascending=False)
        fig = px.pie(names=Citywise_investment.index,
                     values=Citywise_investment.values)
        st.plotly_chart(fig)   

    st.subheader("Year-on-Year Investments")
    YOY_Investment = df[df['Investors'].str.contains(investor)].groupby('Year')['Amount'].sum()
    fig = px.line(YOY_Investment,
                     x=YOY_Investment.index,
                     y=YOY_Investment.values
                     )
    st.plotly_chart(fig)

    st.subheader('Focus Index')
    all_verticals = df.groupby(['Vertical'])['Amount'].sum()
    required_vertical = df[df['Investors'].str.contains(investor)].groupby('Vertical')['Amount'].sum()
    Focus_Index = (required_vertical/all_verticals)*100
    st.dataframe(Focus_Index.dropna().sort_values(ascending=False))

def general_analysis():
    col1,col2,col3,col4 =st.columns(4)
    with col1:
        st.metric(label='Total Invested Amount',
              value = '₹'+str(round(df['Amount'].sum(),2))+' Cr',
              delta='Amount in Cr.',
              border=True)

    with col2:
        highest_investment_startup = df.groupby('Startup')['Amount'].sum().sort_values(ascending=False)
        
        st.metric(label='Highest Invested Startup',
                  delta=highest_investment_startup.index[0],
                  delta_color="normal",
                  value = '₹'+str(round(highest_investment_startup.values[0],2))+' Cr',
                  border=True)
    
    with col3:
        avg_funding = df.groupby('Startup')['Amount'].sum().mean()
        st.metric(label='Average Invested Amount',
              value ='₹'+str(round(avg_funding,2))+' Cr',
              delta= str(df['Startup'].nunique())+' startups across India',
              delta_color="normal",
              border=True)
        

    with col4:
        grow_data = df.groupby('Year',as_index=False)['Amount'].sum()
        grow_data['Previous_Value'] = grow_data['Amount'].shift(1)
        grow_data['YoY_Growth'] = round((grow_data['Amount'] - grow_data['Previous_Value']) / grow_data['Previous_Value'] * 100,2)
        grow_data = grow_data.fillna(0)
        YoY_average_growth = grow_data['YoY_Growth'].iloc[1:].mean()
        
        st.metric(label='Average Year-over-Year Growth',
              value =str(round(YoY_average_growth,2))+' %',
              delta= str(grow_data['YoY_Growth'].iloc[-1])+'% compared to '+str(grow_data['Year'].iloc[-2]),
              border=True)

    col1,col2 = st.columns(2)
    
    
    with col1:
        st.subheader("Year-on-Year Investments")
        tab1, tab2 = st.tabs(['Funding','Startups'])
        with tab1:
            temp_df = df.groupby(['Year'],as_index=False).agg({'Startup':'count','Amount':'sum'})
            
            fig = px.line(temp_df[['Year', 'Amount']],
                            x=temp_df.Year,
                            y=temp_df.Amount,
                            hover_name=temp_df.Startup,
                            labels = dict(x='Year',
                                    y = 'Funding Amount in Cr.')
                            )
            st.plotly_chart(fig)

        with tab2:
            temp_df = df.groupby(['Year'],as_index=False).agg({'Startup':'count','Amount':'sum'})

            fig = px.line(temp_df[['Year', 'Startup']],
                            x=temp_df.Year,
                            y=temp_df.Startup,
                            hover_name=temp_df.Startup,
                            labels = dict(x='Year',
                                    y = 'Funding Amount in Cr.')
                            )
            st.plotly_chart(fig)
    
    with col2:
        st.subheader("Month-on-Month Investments")
        tab1, tab2 = st.tabs(['Funding','Startups'])
        with tab1:
            temp_df = df.groupby(['Year','month_num','Month_Year'],as_index=False).agg({'Startup':'count','Amount':'sum'})
            
            fig = px.line(temp_df[['Month_Year', 'Amount']],
                            x=temp_df.Month_Year,
                            y=temp_df.Amount,
                            hover_name=temp_df.Startup,
                            labels = dict(x='Month',
                                    y = 'Funding Amount in Cr.')
                            )
            st.plotly_chart(fig)
        
        with tab2:
            temp_df = df.groupby(['Year','month_num','Month_Year'],as_index=False).agg({'Startup':'count','Amount':'sum'})
            
            fig = px.line(temp_df[['Month_Year', 'Amount']],
                            x=temp_df.Month_Year,
                            y=temp_df.Startup,
                            hover_name=temp_df.Startup,
                            labels = dict(x='Month',
                                    y = 'Funding Amount in Cr.')
                            )
            st.plotly_chart(fig)
    
    
    st.subheader('Top 20')
    
    tab1,tab2,tab3,tab4 = st.tabs(['Startups',
                                   'Verticals',
                                   'SubVerticals',
                                   'City'])
    with tab1:
        temp_df =df.groupby('Startup')['Amount'].sum().sort_values(ascending=False).head(20)
        fig = px.bar(temp_df,
                        hover_name=temp_df.index,
                        orientation='v',
                        labels = dict(Startup='Startups',
                                    value = 'Funded Amount in Cr.')
                        )
        fig.update_layout(showlegend=False)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig)

    with tab2:
        temp_df =df.groupby('Vertical')['Amount'].sum().sort_values(ascending=False).head(20)
        fig = px.bar(temp_df,
                     hover_name=temp_df.index,
                     orientation='v',
                     labels = dict(Vertical='Verticals',
                                   value = 'Funded Amount in Cr.')
                    )
        fig.update_layout(showlegend=False)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig)
    
    with tab3:
        temp_df =df.groupby('SubVertical')['Amount'].sum().sort_values(ascending=False).head(20)
        fig = px.bar(temp_df,
                     hover_name=temp_df.index,
                     orientation='v',
                     labels = dict(Vertical='SubVerticals',
                                   value = 'Funded Amount in Cr.')
                    )
        fig.update_layout(showlegend=False)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig)
    
    with tab4:
        temp_df =df.groupby('City')['Amount'].sum().sort_values(ascending=False).head(20)
        fig = px.bar(temp_df,
                     hover_name=temp_df.index,
                     orientation='v',
                     labels = dict(Vertical='City',
                                   value = 'Funded Amount in Cr.')
                    )
        fig.update_layout(showlegend=False)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig)

    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Top 10 Active Investors')
        active_investors = df['Investors'].value_counts().sort_values(ascending=False).head(10)
        fig = px.bar(active_investors,
                    hover_name=active_investors.index,
                    orientation='v',
                    labels = dict(Vertical='SubVerticals',
                                    value = 'Funded Amount in Cr.')
                        )
        fig.update_layout(showlegend=False)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig)

    with col2:
        st.subheader("City Wise Investments")
        tab1, tab2 = st.tabs(['Funding','Startups'])
        with tab1:
            temp_df = df.groupby(['City'],as_index=False).agg({'Startup':'count','Amount':'sum'})
            
            fig = px.bar(temp_df[['City', 'Amount']],
                            x=temp_df. City,
                            y=temp_df.Amount,
                            hover_name=temp_df.Startup,
                            labels = dict(x='City',
                                    y = 'Funding Amount in Cr.')
                            )
            st.plotly_chart(fig)
        
        with tab2:
            temp_df = df.groupby(['City'],as_index=False).agg({'Startup':'count','Amount':'sum'})
            
            fig = px.pie(temp_df[['City', 'Amount']],
                         values=temp_df['Amount'],
                         names=temp_df['City'])
            st.plotly_chart(fig)
        
    st.subheader('YoY Growth in Funding')
    year_trend = round(df.groupby('Year')['Amount'].sum().pct_change()*100,2)
    year_trend = year_trend.reset_index()
    year_trend['Color'] = np.where(year_trend["Amount"] < 0, 'red', 'green')
    year_trend.fillna(0)
    year_trend['Growth'] = year_trend['Amount'].astype('str')+'%'

    fig = px.bar(year_trend,
                 x='Year',
                 y='Amount',
                 hover_name=year_trend.Growth)
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_color=year_trend["Color"])
    st.plotly_chart(fig)

    col1,col2= st.columns(2)
    with col1:
        st.subheader('Round Wise Funding')
        temp_df = df.groupby('Round',as_index=False)['Amount'].sum().sort_values(by='Amount',ascending=False)
        temp_df['Share'] = temp_df.Amount / sum(temp_df.Amount)
        fig = px.pie(temp_df,
                    values=temp_df['Share'],
                    names=temp_df['Round'],
                    )
        fig.update_traces(hoverinfo='label+percent')
        st.plotly_chart(fig)
    
    with col2:
        st.subheader('No. of Times Startups Raised Funds')
        temp_df = df.Startup.value_counts().reset_index()
        temp_df.rename(columns={'count':'Funding_times'},inplace=True)
        # st.dataframe(temp_df)

        st.dataframe(temp_df,hide_index=True)

       
    st.subheader("Funding Seasonality")
    tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs(["Overall","2015", "2016", "2017", "2018", "2019", "2020"])

      
    with tab1:
        funding_by_month = df.groupby(['month_name','month_num'],as_index=False)['Amount'].sum().sort_values(by='month_num')
        fig = px.line(funding_by_month,
                  x=funding_by_month['month_name'],
                  y=funding_by_month['Amount'])
        st.plotly_chart(fig)
    
    with tab2:
        timeseries = df[df['Year'] ==2015]
        funding_by_month = timeseries.groupby(['month_name','month_num'],as_index=False)['Amount'].sum().sort_values(by='month_num')
        fig = px.line(funding_by_month,
                  x=funding_by_month['month_name'],
                  y=funding_by_month['Amount'])
        st.plotly_chart(fig)
    
    with tab3:
        timeseries = df[df['Year'] ==2016]
        funding_by_month = timeseries.groupby(['month_name','month_num'],as_index=False)['Amount'].sum().sort_values(by='month_num')
        fig = px.line(funding_by_month,
                  x=funding_by_month['month_name'],
                  y=funding_by_month['Amount'])
        st.plotly_chart(fig)
    
    with tab4:
        timeseries = df[df['Year'] ==2017]
        funding_by_month = timeseries.groupby(['month_name','month_num'],as_index=False)['Amount'].sum().sort_values(by='month_num')
        fig = px.line(funding_by_month,
                  x=funding_by_month['month_name'],
                  y=funding_by_month['Amount'])
        st.plotly_chart(fig)
    
    with tab5:
        timeseries = df[df['Year'] ==2018]
        funding_by_month = timeseries.groupby(['month_name','month_num'],as_index=False)['Amount'].sum().sort_values(by='month_num')
        fig = px.line(funding_by_month,
                  x=funding_by_month['month_name'],
                  y=funding_by_month['Amount'])
        st.plotly_chart(fig)
    
    with tab6:
        timeseries = df[df['Year'] ==2019]
        funding_by_month = timeseries.groupby(['month_name','month_num'],as_index=False)['Amount'].sum().sort_values(by='month_num')
        fig = px.line(funding_by_month,
                  x=funding_by_month['month_name'],
                  y=funding_by_month['Amount'])
        st.plotly_chart(fig)
    
    with tab7:
        timeseries = df[df['Year'] ==2020]
        funding_by_month = timeseries.groupby(['month_name','month_num'],as_index=False)['Amount'].sum().sort_values(by='month_num')
        fig = px.line(funding_by_month,
                  x=funding_by_month['month_name'],
                  y=funding_by_month['Amount'])
        st.plotly_chart(fig)

    st.subheader('City and Sector Correlation')
    city_sector_correlation = df.groupby(['City', 'Vertical'],as_index=False)['Amount'].sum()
    selected_city = st.selectbox('City',city_sector_correlation.City.unique().tolist())
    temp_df = city_sector_correlation[city_sector_correlation['City']==selected_city][['Vertical','Amount']]
    fig= px.bar(temp_df,
                x=temp_df.Vertical,
                y=temp_df.Amount)
    st.plotly_chart(fig)


    st.subheader('Year-over-Year Growth Rate per Sector')
    sector_year_growth = df.groupby(['Year', 'Vertical'])['Amount'].sum().unstack().pct_change() * 100
    fig = px.imshow(sector_year_growth.T)
    fig.update_layout(height=1500)
    st.plotly_chart(fig)


def load_startups(startup):
    st.header(startup)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        Funding = df[df['Startup'].str.contains(startup)]['Amount'].sum()
        Funding_times = df[df['Startup'].str.contains(startup)]['Startup'].value_counts().sum()
        st.metric('Total Funding',
                  value= '₹ '+str(round(Funding,2))+' Cr.',
                  delta= 'Across '+str(Funding_times)+' Funding',
                  border=True)
    
    with col2:
        Avg_Funding = round(df[df['Startup'].str.contains(startup)]
        ['Amount'].mean(),2)
        total_cities = df[df['Startup'].str.contains(startup)]['City'].unique().size
        city_pl = ['City' if total_cities<2 else 'Cities']
        st.metric('Average Funding',
                  value= '₹ '+str(Avg_Funding)+' Cr.',
                  delta = 'Across '+ str(total_cities)+ ' '+ str(city_pl[0]),
                  border=True)
    
    with col3:
        temp_df = df[df['Startup'].str.contains(startup)].groupby(['Year','month_num','Month_Year','Startup','City'],as_index=False)['Amount'].sum().sort_index()
        Recent_Funding = temp_df.sort_values(by=['Year','month_num'],ascending=[False,False]).iloc[0]
        st.metric('Recent Funding',
                  value= '₹ '+str(round(Recent_Funding[5],2))+' Cr.',
                  delta = 'On ' + str(Recent_Funding[2]) + ' at '+str(Recent_Funding[4]),
                  border=True)
    
    with col4:
        sector_focus = df[df['Startup'].str.contains(startup)].groupby('Startup')['Vertical'].apply(lambda x: x.mode()[0])
        primary_city = df[df['Startup'].str.contains(startup)].groupby('Startup')['City'].apply(lambda x: x.mode()[0]).iloc[0]
        st.metric('City Wise Sector Focus',
                  value =primary_city,
                  delta= sector_focus.iloc[0],
                  border=True)
    
    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Fundings across Time')
        tab1,tab2 = st.tabs(['YOY -Fundings','MOM - Fundings'])
        
        with tab1:
            temp_df = df[df['Startup'].str.contains(startup)].groupby(['Year'],as_index=False)['Amount'].sum().sort_values(['Year'],ascending=[True])
            fig=px.line(temp_df,
                    x =temp_df.Year,
                    y =temp_df.Amount,
                    labels={'Amount':'Amount in Cr.'})
            st.plotly_chart(fig)
        
        with tab2:
            temp_df = df[df['Startup'].str.contains(startup)].groupby(['Year','month_num','Month_Year'],as_index=False)['Amount'].sum().sort_values(['Year','month_num'],ascending=[True,True])
            fig=px.line(temp_df,
                    x =temp_df.Month_Year,
                    y =temp_df.Amount,
                    labels={'Amount':'Amount in Cr.'})
            st.plotly_chart(fig)
    
    with col2:
        st.subheader('City Wise Fundings')
        tab1,tab2 = st.tabs(['Fundings','Investors'])
        
        with tab1:
            temp_df = df[df['Startup'].str.contains(startup)].groupby('City')['Amount'].sum()
            fig=px.bar(temp_df,
                    x =temp_df.index,
                    y =temp_df.values,
                    labels={'y':'Amount in Cr.'})
            st.plotly_chart(fig)
        
        with tab2:
            temp_df = df[df['Startup'].str.contains(startup)].groupby(['City'])['Investor_num'].sum()
            fig=px.bar(temp_df,
                    x =temp_df.index,
                    y =temp_df.values,
                    labels={'y':'No. of Investors'})
            st.plotly_chart(fig)

    col1,col2,col3 = st.columns(3)
    with col1:
        investors = sorted(set(df[df['Startup'].str.contains(startup)]['Investors'].str.split(',').sum()))
        st.subheader('Investors')
        st.dataframe(investors)
    
    with col2:
        st.subheader('Round-Wise Funding')
        round_wise_funding = df[df['Startup'].str.contains('Ola')].groupby('Round')['Amount'].sum()
        fig = px.bar(round_wise_funding,
                     x=round_wise_funding.index,
                     y=round_wise_funding.values,
                     labels={'y':'Amount in Cr.'})
        st.plotly_chart(fig)

    with col3:
        st.subheader('Vertical Fundings')
        temp_df= df[df['Startup'].str.contains(startup)].groupby('Vertical')['Amount'].sum()
        fig=px.bar(temp_df,
                   x=temp_df.index,
                   y=temp_df.values,
                   labels={'y':'Amount in Cr.'})
        st.plotly_chart(fig)
    
    st.subheader('Relationship between Year, Round and Funding')
    fig = px.scatter(df[df['Startup'].str.contains(startup)],
                     x="Year",
                     y="Amount",
                     size="Amount",
                     color="Round",
                     hover_name="Startup",
                     log_x=True, 
                     size_max=60)
    st.plotly_chart(fig)

    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Funding Frequency')
        temp_df = df[df['Startup'].str.contains('Ola')].groupby(['Year'],as_index=False)['Round'].count()
        fig = px.histogram(temp_df,
                     x='Year',
                     y='Round',
                     nbins=6)
        st.plotly_chart(fig)
    
    with col2:
        st.subheader('Growth in Funding')
        temp_df = df[df['Startup'].str.contains('Ola')].groupby(['Year'])['Amount'].sum().pct_change() * 100
        temp_df = temp_df.reset_index()
        temp_df.fillna(0)
        temp_df['Color'] = np.where(temp_df["Amount"] < 0, 'red', 'green')
        fig= px.bar(temp_df,
                    x=temp_df.Year,
                    y=temp_df.Amount)
        fig.update_layout(showlegend=False)
        fig.update_traces(marker_color=temp_df["Color"])
        st.plotly_chart(fig)