import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image


def pie_plot(df, label, name, hole_size=0):
    fig = px.pie(df, labels=label, names=name, hole=hole_size, color_discrete_sequence=['#b20710', '#221f1f'],
                 width=1000, height=600)
    st.plotly_chart(fig)


def bar_plot(df, x, y):
    fig = px.bar(df, x, y, color_discrete_sequence=['#b20710'], width=1000, height=600)
    st.plotly_chart(fig)


def map_plot(df, location, colors, w, h):
    fig = px.choropleth(df, locations=location, color=colors, width=w, height=h,
                        color_continuous_scale='RdGy')
    st.plotly_chart(fig)


def corr_heatmap_plot(df):
    corr = df.corr()
    heat = go.Heatmap(z=corr, x=corr.columns.values, y=corr.columns.values, colorscale=['darkred', 'red'])
    layout = go.Layout(width=1000, height=800)
    fig = go.Figure(data=heat, layout=layout)
    st.plotly_chart(fig)


def table_plot(vals, cols):
    fig = go.Figure(data=go.Table(header=dict(values=vals, fill_color='#b20710', font_color='white'),
                                  cells=dict(values=cols, fill_color='#221f1f', font_color='white')))
    fig.update_layout(width=1000, height=500)
    st.plotly_chart(fig)


def line_plot(df, x, y):
    fig = px.area(df, x=x, y=y, color_discrete_sequence=['#b20710'], width=1000, height=600)
    st.plotly_chart(fig)


def stack_hist_plot(x1, x2, name1, name2, bar_mode=None):
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc='count', x=x1, name=name1, marker={'color': '#b20710'}))
    fig.add_trace(go.Histogram(histfunc='count', x=x2, name=name2, marker={'color': '#221f1f'}))
    fig.update_layout(barmode=bar_mode, width=1000, height=600)
    st.plotly_chart(fig)


def heatmap_plot(x, y, z):
    fig = go.Heatmap(x=x, y=y, z=z, colorscale=['#221f1f', '#b20710'])
    st.plotly_chart(fig)


def wordcloud_plot():
    img = Image.open('wordcloud.png')
    st.image(img)


def scatter_plot(df, x, y, size):
    fig = px.scatter(df, x, y, size=size, color_discrete_sequence=['#b20710', '#221f1f'])
    st.plotly_chart(fig)


def tree_plot(df, vals):
    fig = px.treemap(df, path=[px.Constant('Genres'), 'Genre'], values=vals, color_discrete_sequence=['#b20710'],
                     width=1000, height=600)
    st.plotly_chart(fig)
