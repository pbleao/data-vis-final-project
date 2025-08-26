import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv('../Datasets/project_dataset.csv')

# Convert the date columns to a datetime object
df['date'] = pd.to_datetime(df[['Yr', 'M', 'D', 'HH', 'MM']].rename(columns={'Yr': 'year', 'M': 'month', 'D': 'day', 'HH': 'hour', 'MM': 'minute'}))

# 1. Hourly Traffic Volume
hourly_volume = df.groupby('HH')['Vol'].sum().reset_index()
fig_hourly = px.bar(hourly_volume, x='HH', y='Vol', color="Vol",
                    labels={'HH': 'Hour of the Day', 'Vol': 'Total Volume'},
                    color_continuous_scale=['white', 'red'])  # Red-white color scale
fig_hourly.write_html("hours_volume.html")  # Save as HTML

# 2. Traffic Volume by Boro
if 'Boro' in df.columns:
    boros_volume = df.groupby('Boro')['Vol'].sum().reset_index()
    fig_boros = px.bar(boros_volume, x='Boro', y='Vol', color="Boro",
                       labels={'Boro': 'Borough', 'Vol': 'Total Volume'},
                       color_continuous_scale=['white', 'red'])  # Red-white color scale
    fig_boros.write_html("boros_volume.html")  # Save as HTML
else:
    print("Column 'Borough' not found in the dataset. Skipping boros_volume graph.")

# 3. Monthly Traffic Volume Comparison (2021 vs 2022)
monthly_volume = df.groupby(['Yr', 'M'])['Vol'].sum().unstack()
fig_monthly = go.Figure()
for year in monthly_volume.index:
    fig_monthly.add_trace(go.Scatter(x=monthly_volume.columns, y=monthly_volume.loc[year], mode='lines+markers', name=str(year)))
fig_monthly.update_layout( xaxis_title='Month', yaxis_title='Total Volume')
fig_monthly.write_html("monthly_volume.html")  # Save as HTML
