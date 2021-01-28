# importar pacotes
import pandas as pd
import pydeck as pdk
import streamlit as st

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

# sidebar
st.sidebar.info("Foram carregadas {} linhas.".format(df.shape[0]))

if st.sidebar.checkbox("Ver tabela com dados"):
    st.header("Raw Data")
    st.write(df)

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
