import datetime
import os
import streamlit as st
import pandas as pd
from collections import defaultdict
from streamlit_option_menu import option_menu
from plots import *


def get_path(file):
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, '..', 'data', file)
    return path


def read_files():
    netflix_top10 = pd.read_csv(get_path('netflix-daily-top-10.csv'))
    netflix_data = pd.read_csv(get_path('netflix.csv'))
    netfix_countries = pd.read_csv(get_path('netflix-countries.csv'))
    netflix_genres_movies = pd.read_csv(get_path('netflix-genres-m.csv'))
    netflix_genres_series = pd.read_csv(get_path('netflix-genres-s.csv'))
    return netflix_top10, netflix_data, netfix_countries, netflix_genres_movies, netflix_genres_series


def top_10_all_time(col):
    df1 = df_top10.copy()
    df1.sort_values(by=col, ascending=False, inplace=True)
    df1['Title'] = df1['Title'].drop_duplicates(keep='first')
    df1 = df1.dropna()
    return df1


def split_file(df, col):
    df_movies = df[df[col] == 'Movie']
    df_series = df[df[col] == 'TV Show']
    return df_movies, df_series


def calc_no_of_types(df):
    types = []
    for i in df['genre']: types += i
    types = set(types)
    return len(types)


def calc_no_releases(df, index, col_name):
    counter = defaultdict(int)
    for val in df['date_added']:
        if isinstance(val, str):
            year = val.split()[index]
            counter[year] += 1
        else:
            continue

    d = {f'{col_name}': list(sorted(reversed(counter.keys()))),
         'Releases': [counter[key] for key in sorted(reversed(counter))]}
    return pd.DataFrame(data=d)


df_top10, df_titles, df_countries, df_genres_movies, df_genres_series = read_files()
df_top10_all_time_days = top_10_all_time('Days In Top 10')
df_top10_all_time_score = top_10_all_time('Viewership Score')
df_top10_all_time_movies, df_top10_all_time_series = split_file(df_top10_all_time_days, 'Type')
df_top10_all_time_score_movies, df_top10_all_time_score_series = split_file(df_top10_all_time_score, 'Type')
df_titles_movies, df_titles_series = split_file(df_titles, 'type')

with st.sidebar:
    selected = option_menu(
        menu_title='Pages',
        options=['Main', 'Netflix Daily Top 10', 'Netflix Data', 'Infographic'],
        menu_icon='None'
    )

if selected == 'Main':
    st.title('Movies and series on Netflix')

    st.write('#### Data Visualization project')
    st.write('#### Created in: 2022')
    st.write('#### Made by: Agnieszka Felis, Aleksandra Jaroszek, Maciej Struski')
    st.write('#### Based on: [Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)\
              [Netflix daily top 10](https://www.kaggle.com/datasets/prasertk/netflix-daily-top-10-in-us)')

    wordcloud_plot()

if selected == 'Netflix Daily Top 10':
    st.title('Netflix Daily Top 10')

    st.write('#### Which day do you want to check?')

    date = str(st.date_input('Choose a date',
                             value=datetime.date(2020, 4, 1),
                             min_value=datetime.date(2020, 4, 1),
                             max_value=datetime.date(2022, 3, 11)))
    ranking = df_top10[df_top10['As of'] == date]['Title']
    table_plot(['Rank', 'Title'], [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ranking])

    st.write('#### Daily Top 10 Ranking - Movies')
    bar_plot(df_top10_all_time_movies.iloc[:10], 'Title', 'Days In Top 10')
    st.write('#### Daily Top 10 Ranking - TV Shows')
    bar_plot(df_top10_all_time_series.iloc[:10], 'Title', 'Days In Top 10')

    st.write('#### Best Viewership Score - Movies')
    bar_plot(df_top10_all_time_score_movies.iloc[:10], 'Title', 'Viewership Score')
    st.write('#### Best Viewership Score - TV Show')
    bar_plot(df_top10_all_time_score_series.iloc[:10], 'Title', 'Viewership Score')

    st.write('#### Are Netflix\'s productions more popular than other productions on Netflix?')
    pie_plot(df_top10_all_time_days, 'Netflix Exclusive', 'Netflix Exclusive', 0.3)

    st.write('#### Movies vs TV Shows in Daily Top 10')
    pie_plot(df_top10.Type, df_top10.Type.values, df_top10.Type.values, 0.3)

if selected == 'Netflix Data':
    st.title('Netflix Data')

    st.write('\n')
    mean_movie_duration = df_titles_movies['duration'].mean().round(2)
    st.write('### Average movie duration on Netflix', str(mean_movie_duration), ' minutes')

    mean_series_duration = df_titles_series['duration'].mean().round(2)
    st.write('### Average TV Show duration on Netflix', str(mean_series_duration), ' seasons')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    st.write('#### Movie and TV Shows distribution')
    pie_plot(df_titles['type'], df_titles['type'].values, df_titles['type'].values, 0.3)

    st.write('#### Map of top producing countries')
    map_plot(df_countries, 'iso_alpha', 'Count', 1000, 800)

    df_titles['genre'] = df_titles['listed_in'].apply(lambda x: x.replace(' ,', ',').replace(', ', ',').split(','))
    df_titles_movies, df_titles_series = split_file(df_titles, 'type')
    res_movies = df_titles_movies['genre'].str.join('|').str.get_dummies()
    res_series = df_titles_series['genre'].str.join('|').str.get_dummies()

    no_movies = calc_no_of_types(df_titles_movies)
    no_series = calc_no_of_types(df_titles_series)

    st.write('#### Correlations between movies genres')
    st.write('##### Number of unique movies genres: ', str(no_movies))
    corr_heatmap_plot(res_movies)
    st.write('#### Correlations between TV Shows genres')
    st.write('##### Number of unique TV Shows genres: ', str(no_series))
    corr_heatmap_plot(res_series)

    all_releases = calc_no_releases(df_titles, 2, 'Years')
    movie_releases = calc_no_releases(df_titles_movies, 2, 'Years')
    series_releases = calc_no_releases(df_titles_series, 2, 'Years')

    st.write('#### Annual content added')
    line_plot(all_releases, all_releases['Years'], all_releases['Releases'])

    months_movies = df_titles_movies.loc[df_titles_movies['month_added'] != 0]
    months_series = df_titles_series.loc[df_titles_series['month_added'] != 0]

    st.write('#### Monthly content added - Movies vs TV Shows')
    stack_hist_plot(months_movies['month_added'], months_series['month_added'], 'Movie', 'TV Show', 'overlay')

    ratings = df_titles.loc[df_titles['rating'].isnull() == False]
    movie_ratings = ratings.loc[ratings['type'] == 'Movie']
    series_ratings = ratings.loc[ratings['type'] == 'TV Show']
    st.write('#### Rating distribution - Movies vs TV Shows')
    stack_hist_plot(movie_ratings['rating'], series_ratings['rating'], 'Movie', 'TV Show')

    st.write('#### Genres distribution - Movies')
    tree_plot(df_genres_movies, df_genres_movies['Count'])

    st.write('#### Genres distribution - TV Shows')
    tree_plot(df_genres_series, df_genres_series['Count'])

if selected == 'Infographic':
    img = Image.open('infografika.jpg')
    st.image(img)
