# importar pacotes
import pandas as pd
import pydeck as pdk
import streamlit as st
# import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# from datetime import date


# carregar os meus dados
df = pd.read_csv('kc_dataset_clean.csv')

# dashboard
st.title("Casas em Seattle")
st.markdown(
    """
    Empresas imobiliárias online oferecem avaliações de casas usando técnicas de aprendizado de máquina. 
    O objetivo deste relatório é analisar as vendas de casas em King County, Seattle, Estado de Washington, EUA, 
    usando técnicas de ciência de dados. O conjunto de dados consiste em dados históricos de casas vendidas 
    entre maio de 2014 a maio de 2015.
    """
)

df['y/m'] = df['date'].apply(lambda x: str(x)[:7])

# sidebar
st.sidebar.info("Foram carregadas {} linhas.".format(df.shape[0]))

if st.sidebar.checkbox("Ver dados de preço por número de quartos"):
    fig = plt.figure(figsize=(15, 12))
    plt.title('Média de preço de casa por número de quartos', fontsize=33)
    plt.ylabel('price', fontsize=22)
    plt.xlabel('bedrooms', fontsize=22)
    media_quarto = df[['bedrooms', 'price']].groupby('bedrooms').mean().reset_index()
    sns.barplot(x='bedrooms', y='price', data=media_quarto)
    st.write(fig)

if st.sidebar.checkbox("Média de preço de casa por notas"):
    fig = plt.figure(figsize=(15, 12))
    plt.title('Média de preço de casa por notas', fontsize=33)
    plt.ylabel('price', fontsize=22)
    plt.xlabel('grade', fontsize=22)
    media_nota = df[['grade', 'price']].groupby('grade').mean().reset_index()
    sns.barplot(x='grade', y='price', data=media_nota)
    st.write(fig)

if st.sidebar.checkbox("Evolução dos preços em 1 ano"):
    fig = plt.figure(figsize=(15, 12))
    plt.title('Evolução dos preços em 1 ano', fontsize=33)
    plt.ylabel('', fontsize=22)
    plt.xlabel('', fontsize=22)
    media_preco = df[['y/m', 'price']].groupby('y/m').mean().reset_index()
    media_preco['growth_price'] = 100 * media_preco['price'].pct_change()
    sns.barplot(x='y/m', y='growth_price', data=media_preco)
    plt.xticks(rotation=45)
    st.write(fig)

if st.sidebar.checkbox("Média de preços por mês em 1 ano"):
    fig = plt.figure(figsize=(15, 12))
    plt.title('Média de preços por mês', fontsize=33)
    plt.ylabel('', fontsize=22)
    plt.xlabel('', fontsize=22)
    sns.barplot(x='y/m', y='price', data=df)
    st.write(fig)

df.date = pd.to_datetime(df.date)
ano_selecionado = st.sidebar.slider("Selecione um ano", 2014, 2015)
df_selected = df[df.date.dt.year == ano_selecionado]

st.subheader('Mapa da cidade de Seattle')
# st.map(df)

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=47.608013,
        longitude=-122.335167,
        zoom=7.5,
        min_zoom=3,
        max_zoom=15,
        pitch=40.5,
        bearing=-27.36
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=df_selected[['lat', 'lon']],  # df
            get_position='[lon,lat]',
            radius=150,
            auto_highlight=True,
            elevation_scale=25,
            pickable=False,  # Interfere na manipulação do mapa.
            elevation_range=[0, 3000],
            extruded=True,
            stroked=True,
            filled=True,
            wireframe=True
        )
    ],
))
