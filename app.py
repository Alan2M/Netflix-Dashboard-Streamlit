"""Netflix Atlas — dashboards exploratório e de indicadores, AVD aulas 21–23."""
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Netflix Atlas | Inteligência de Catálogo", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'clean'
ACCENT = '#38D9BE'
PURPLE = '#B7A2FF'
PINK = '#FFB88C'
PLOT_BG = '#121D2C'
NAMES = {'imdb_rating':'Nota IMDb', 'tmdb_rating':'Nota TMDB', 'runtime_minutes':'Duração (min)', 'release_year':'Ano de lançamento', 'imdb_votes':'Votos IMDb', 'tmdb_popularity':'Popularidade TMDB', 'content_age':'Idade do conteúdo', 'country_count':'Número de países', 'genre_count':'Número de gêneros', 'data_completeness_score':'Completude dos dados', 'popularity_percentile':'Percentil de popularidade', 'match_confidence':'Confiança do vínculo'}
PREFERRED = ['imdb_rating', 'tmdb_rating', 'runtime_minutes', 'release_year', 'imdb_votes', 'tmdb_popularity']

def label(c): return NAMES.get(c, c.replace('_',' ').capitalize())
def layout(fig, height=355):
    fig.update_layout(height=height, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#C9D7E5', size=12), margin=dict(l=10,r=10,t=25,b=25), legend=dict(orientation='h', y=-0.25), hoverlabel=dict(bgcolor=PLOT_BG, font_color='white'))
    fig.update_xaxes(gridcolor='rgba(171,190,211,.10)', zeroline=False)
    fig.update_yaxes(gridcolor='rgba(171,190,211,.10)', zeroline=False)
    return fig

st.markdown('''<style>
.stApp{background:radial-gradient(circle at 85% 0%,#1d2d46 0%,#0A111D 42%,#09111A 100%);color:#EFF5FC}
.block-container{max-width:1450px;padding-top:1.4rem;padding-bottom:3rem}
[data-testid="stSidebar"]{background:#101C2C;border-right:1px solid #29364A}
[data-testid="stMetric"]{background:linear-gradient(145deg,#1B2A3F,#142131);padding:20px 18px;border:1px solid #324255;border-radius:16px}
[data-testid="stMetricLabel"]{color:#ADC0D2}
[data-testid="stMetricValue"]{color:#F3F9FF}
.stTabs [data-baseweb="tab-list"]{gap:9px;border-bottom:1px solid #2A3A4C}
.stTabs [data-baseweb="tab"]{background:#1B2A3C;border-radius:10px 10px 0 0;padding:10px 23px}
.stTabs [aria-selected="true"]{color:#42DEC6!important}
.hero{padding:30px 36px;border:1px solid #344457;border-radius:22px;background:linear-gradient(115deg,#1B3041,#102031 75%);margin-bottom:22px}
.hero .eyebrow{font-size:12px;letter-spacing:3px;color:#48E0C5;font-weight:800}.hero h1{font-size:clamp(2rem,4vw,3.3rem);margin:6px 0;color:#F7FAFF;font-weight:750}.hero p{margin:0;color:#B4C6D8;font-size:16px}
.sectionlabel{font-size:12px;letter-spacing:2px;color:#53DDC6;font-weight:700;margin-top:12px}
.note{color:#9CB2C6;font-size:13px}
</style>''', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def read_data(path):
    df = pd.read_csv(path, low_memory=False)
    for c in PREFERRED + ['content_age','genre_count','country_count']:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

st.markdown('<div class="hero"><span class="eyebrow">STREAMING DATA LAB  /  2026</span><h1>◈ Netflix Atlas</h1><p>Uma visão exploratória da composição, qualidade e diversidade do catálogo — construída com dados, não suposições.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('### ◈ CONTROLES')
    fonte = st.radio('Base de análise', ['Tratados','Originais'], horizontal=True)
    arquivo = DATA / ('netflix_tratado.csv' if fonte == 'Tratados' else 'netflix_original.csv')

if not arquivo.exists():
    st.error('Não encontrei os CSVs necessários. Gere-os localmente e inclua data/clean/ no GitHub antes do deploy.')
    st.code('python preparar_dados.py', language='powershell')
    st.info('Depois, confirme que data/clean/netflix_tratado.csv e data/clean/netflix_original.csv foram adicionados ao Git (ou que ao menos a base usada no app esteja presente).')
    st.stop()

df = read_data(str(arquivo))
nums = [c for c in df.select_dtypes(include='number').columns if df[c].notna().sum() >= 2 and df[c].nunique(dropna=True) > 1]
with st.sidebar:
    if 'type' in df:
        tipos = sorted(df['type'].dropna().astype(str).unique().tolist())
        tipos_sel = st.multiselect('Tipo de conteúdo', tipos, default=tipos)
    else:
        tipos_sel = []
    if 'primary_genre' in df:
        generos = sorted(df['primary_genre'].dropna().astype(str).unique().tolist())
        generos_sel = st.multiselect('Gênero principal', generos, default=[], help='Vazio = todos os gêneros')
    else:
        generos_sel = []
    if 'release_year' in nums:
        y = df['release_year'].dropna()
        year_min, year_max = int(y.min()), int(y.max())
        anos = st.slider('Intervalo de lançamento',year_min, year_max,(year_min, year_max)) if year_min < year_max else (year_min,year_max)
    else:
        anos = None
    st.caption('Filtros aplicados às duas abas. A base tratada pode ter notas imputadas pela mediana.')

filtered = df.copy()
if 'type' in filtered: filtered = filtered[filtered['type'].astype(str).isin(tipos_sel)]
if 'primary_genre' in filtered and generos_sel: filtered = filtered[filtered['primary_genre'].astype(str).isin(generos_sel)]
if anos is not None: filtered = filtered[filtered['release_year'].between(*anos)]
if filtered.empty:
    st.warning('Nenhum registro corresponde aos filtros. Ajuste as seleções na barra lateral.')
    st.stop()

st.caption(f'Base {fonte.lower()} · {len(filtered):,} títulos no recorte · {len(df):,} registros na base'.replace(',','.'))
tab1, tab2 = st.tabs(['01  /  EDA & CORRELAÇÕES', '02  /  INTELIGÊNCIA DO CATÁLOGO'])

with tab1:
    st.markdown('### Relações quantitativas e distribuições')
    st.markdown('<div class="note">Use o recorte compartilhado à esquerda e ajuste a análise estatística abaixo. Ao alterar qualquer filtro, os gráficos são recalculados.</div>', unsafe_allow_html=True)
    if not nums:
        st.warning('Sem variáveis quantitativas suficientes para este recorte.')
    else:
        c1,c2,c3 = st.columns([1.8,1.1,1])
        with c1: choices = st.multiselect('Variáveis na correlação', nums, default=[c for c in PREFERRED if c in nums][:4], format_func=label)
        with c2: method = st.selectbox('Correlação', ['Spearman','Pearson','Kendall'])
        with c3: variable = st.selectbox('Variável do histograma',nums, format_func=label, index=nums.index('imdb_rating') if 'imdb_rating' in nums else 0)
        # Um único recorte quantitativo alimenta tanto a matriz quanto o histograma.
        valores = pd.to_numeric(filtered[variable], errors='coerce').dropna()
        if not valores.empty:
            lo, hi = float(valores.min()), float(valores.max())
            if lo < hi:
                # Sem key fixo: ao trocar de variável, o widget recebe faixa válida.
                interval = st.slider(f'Intervalo: {label(variable)}', lo, hi, (lo, hi), key=f'intervalo_{variable}')
                recorte_eda = filtered[filtered[variable].between(*interval)].copy()
            else:
                recorte_eda = filtered.copy()
        else:
            recorte_eda = filtered.iloc[0:0].copy()
        bins = st.slider('Faixas do histograma', 5, 60, 25)
        st.caption(f'Recorte quantitativo: {len(recorte_eda):,} títulos · controla os dois gráficos'.replace(',','.'))
        n1,n2 = st.columns([1.65,1])
        with n1:
            st.markdown('#### Matriz de correlação')
            if len(choices) < 2:
                st.info('Selecione duas ou mais variáveis para calcular a correlação.')
            elif len(recorte_eda) < 3:
                st.info('Recorte insuficiente para calcular correlações.')
            else:
                corr = recorte_eda[choices].corr(method=method.lower())
                if corr.isna().all().all():
                    st.info('Não há observações suficientes para correlação entre as variáveis selecionadas.')
                else:
                    fig = px.imshow(corr, x=[label(c) for c in choices], y=[label(c) for c in choices], zmin=-1, zmax=1, color_continuous_scale=[[0,'#F48DA4'],[.5,'#1E2D40'],[1,'#39DFC5']], text_auto='.2f', aspect='auto')
                    fig.update_layout(coloraxis_colorbar=dict(title='ρ / r'))
                    st.plotly_chart(layout(fig, 420), use_container_width=True)
                    st.caption('Correlações calculadas apenas dentro do intervalo selecionado; ausentes tratados par a par. Correlação não indica causalidade.')
        with n2:
            st.markdown('#### Distribuição')
            v = pd.to_numeric(recorte_eda[variable], errors='coerce').dropna()
            if v.empty:
                st.info('Nenhum valor válido no intervalo.')
            else:
                fig = px.histogram(x=v, nbins=bins, color_discrete_sequence=[ACCENT], labels={'x':label(variable),'y':'Títulos'})
                fig.add_vline(x=float(v.median()),line_dash='dash',line_color=PINK)
                st.plotly_chart(layout(fig,330),use_container_width=True)
                st.caption(f'Média {v.mean():.2f} · Mediana {v.median():.2f} · N = {len(v):,}'.replace(',','.'))
        st.markdown('#### Detalhes do recorte')
        with st.expander('Estatísticas descritivas e dados (até 1.000 linhas)'):
            st.dataframe(recorte_eda[nums].describe().T, use_container_width=True)
            st.dataframe(recorte_eda.head(1000), use_container_width=True)
            st.download_button('Exportar recorte CSV', recorte_eda.to_csv(index=False).encode('utf-8-sig'),'netflix_recorte.csv','text/csv')

with tab2:
    st.markdown('### Performance e diversidade do catálogo')
    st.caption('Indicadores descritivos do conjunto filtrado. Não são métricas de audiência ou receita da Netflix.')
    metrics = st.columns(4)
    metrics[0].metric('Títulos no recorte',f'{len(filtered):,}'.replace(',','.'))
    if 'imdb_rating' in filtered:
        valid = pd.to_numeric(filtered['imdb_rating'],errors='coerce').dropna()
        metrics[1].metric('IMDb médio',f'{valid.mean():.2f} / 10' if len(valid) else 'N/D')
        metrics[2].metric('IMDb ≥ 7',f'{(valid.ge(7).mean()*100):.1f}%' if len(valid) else 'N/D',help='Percentual entre os registros com nota válida; na base tratada pode incluir valores imputados.')
    else:
        metrics[1].metric('IMDb médio','N/D');metrics[2].metric('IMDb ≥ 7','N/D')
    if 'type' in filtered:
        movies = filtered['type'].astype(str).str.casefold().eq('movie').sum()
        metrics[3].metric('Participação de filmes',f'{movies/len(filtered)*100:.1f}%')
    else: metrics[3].metric('Participação de filmes','N/D')
    st.write('')
    left,right=st.columns(2,gap='large')
    with left:
        st.markdown('#### 01 · Composição por formato')
        if 'type' in filtered:
            grouped=filtered['type'].fillna('Não informado').value_counts().reset_index()
            grouped.columns=['Formato','Títulos']
            fig=px.bar(grouped,x='Formato',y='Títulos',color='Formato',color_discrete_sequence=[ACCENT,PURPLE,PINK],text='Títulos')
            fig.update_layout(showlegend=False)
            st.plotly_chart(layout(fig),use_container_width=True)
        else: st.info('Variável type indisponível.')
    with right:
        st.markdown('#### 02 · Gêneros mais frequentes')
        if 'primary_genre' in filtered:
            grouped=filtered['primary_genre'].fillna('Não informado').value_counts().head(8).sort_values().reset_index()
            grouped.columns=['Gênero','Títulos']
            fig=px.bar(grouped,x='Títulos',y='Gênero',orientation='h',color_discrete_sequence=[PURPLE],text='Títulos')
            st.plotly_chart(layout(fig),use_container_width=True)
        else: st.info('Variável primary_genre indisponível.')
    st.markdown('#### 03 · Evolução dos lançamentos por ano')
    if 'release_year' in filtered:
        years=pd.to_numeric(filtered['release_year'],errors='coerce').dropna().astype(int).value_counts().sort_index().rename_axis('Ano').reset_index(name='Títulos')
        fig=px.area(years,x='Ano',y='Títulos',color_discrete_sequence=[ACCENT],markers=True)
        fig.update_traces(fillcolor='rgba(56,217,190,.13)')
        st.plotly_chart(layout(fig,335),use_container_width=True)
        st.caption('Este gráfico mostra o ano de lançamento dos títulos da amostra, não a data em que entraram na plataforma.')
    else: st.info('Variável release_year indisponível.')
    with st.expander('Como interpretar os indicadores'):
        st.markdown('**Total** mede a dimensão do recorte; **IMDb médio** resume avaliações disponíveis; **IMDb ≥ 7** mede a proporção de títulos com nota igual ou superior a 7, considerando somente notas válidas; **participação de filmes** identifica o equilíbrio entre formatos. Uma base com avaliações preenchidas pela mediana pode alterar esses indicadores. Os gráficos mostram composição, gêneros e distribuição temporal, não necessariamente preferência dos assinantes.')

st.divider()
st.caption('Netflix Atlas · Projeto acadêmico de Análise e Visualização de Dados · Fonte: conjunto de dados enriquecido Netflix/IMDb/TMDB usado na EDA. Projeto não afiliado à Netflix.')
