import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("Olympic History Dashboard")
st.header("Created By: Asif Dar")

# Load the Olympic data
df_a = pd.read_csv("athlete_events.csv")
df_n = pd.read_csv("noc_regions.csv")

df = pd.merge(df_a, df_n, how='outer', on='NOC')

df.to_csv("merged_file.csv", index=False) 
df.rename(columns={'region':'Region','notes':'Notes'}, inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.dropna(inplace=True)

# Total Number of Participations
participations = len(df['Games'].unique())

# Number of Gold Medals
gold_medals = len(df[df['Medal'] == 'Gold'])

# Number of Silver Medals
silver_medals = len(df[df['Medal'] == 'Silver'])

# Number of Bronze Medals
bronze_medals = len(df[df['Medal'] == 'Bronze'])

col1, col2, col3, col4 = st.columns(4)
with col1:
   st.metric("Total # of Participations", participations)
with col2:
   st.metric("# of Gold Medals", gold_medals)
with col3:
   st.metric("# of Silver Medals", silver_medals)
with col4:
   st.metric("# of Bronze Medals", bronze_medals)


# Number of Medals over Years For Each Medal Type (G,S,B) Single Line Chart
medal_years = df.groupby(['Year', 'Medal']).size().unstack(fill_value=0)
medal_years.plot(kind='line')
st.line_chart(medal_years)

# Horizontal Bar Chart by # of Medals Received by Each Athlete Sorted by the Most & Top 5 Only
athlete_medals = df.groupby(['Name'])['Medal'].count().reset_index(name='Medals')
athlete_medals = athlete_medals.sort_values('Medals', ascending=False)
top_athletes = athlete_medals.head(5)
fig, ax = plt.subplots()
ax.barh(top_athletes['Name'], top_athletes['Medals'])
ax.invert_yaxis()
plt.title('Number of Medals Received by Each Athlete - Top 5')
plt.xlabel('Number of Medals')
st.pyplot(fig)

# Highlight Table by Number of Medals Received in each Sport Sorted by the Most & Top 5 Only
sport_medals = df.groupby(['Sport'])['Medal'].count().reset_index(name='Medals')
sport_medals = sport_medals.sort_values('Medals', ascending=False)
top_sports = sport_medals.head(5)
st.write(top_sports.style.highlight_max(color='lightgreen'))

# Number of Medals over Age Histogram Chart, 10 Years Bins
df['Age_bin'] = pd.cut(df['Age'], bins=range(10, 100, 20))
age_medals = df.groupby(['Age_bin', 'Medal']).size().unstack(fill_value=0)
age_medals.plot(kind='bar', stacked=True)
plt.title('Number of Medals over Age Histogram Chart')
plt.xlabel('Age Bins')
plt.ylabel('Number of Medals')
st.pyplot()
plt.close()

# Pie Chart Summary by Number of Medals bifurcated by Gender
gender_medals = df.groupby(['Sex'])['Medal'].count().reset_index(name='Medals')
fig, ax = plt.subplots()
ax.pie(gender_medals['Medals'], labels=gender_medals['Sex'], autopct='%1.1f%%')
plt.title('Summary by Number of Medals bifurcated by Gender')
st.pyplot(fig)
plt.close()

# Vertical Bar Chart by # of Medals Received in each Season
season_medals = df.groupby(['Season'])['Medal'].count().reset_index(name='Medals')
fig, ax = plt.subplots()
ax.bar(season_medals['Season'], season_medals['Medals'])
plt.title('Number of Medals Received in each Season')
plt.xlabel('Season')
plt.ylabel('Number of Medals')
st.pyplot(fig)
plt.close()

# Add a dropdown menu to select the type of medal
medal_type = st.selectbox('Select a medal type', ['All', 'Gold', 'Silver', 'Bronze'])

# Plot the total number of medals won by each country based on the selected medal type
if medal_type == 'All':
    medals_by_country = df.groupby('NOC')['Medal'].count().sort_values(ascending=False)
else:
    medals_by_country = df[df['Medal'] == medal_type].groupby('NOC')['Medal'].count().sort_values(ascending=False)
st.bar_chart(medals_by_country)

# Add a slider to select the age range
age_range = st.slider('Select an age range', min_value=10, max_value=100, value=(20, 30))

# Show the number of athletes in the selected age range
num_athletes = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]['Name'].nunique()
st.write('Number of athletes:', num_athletes)
