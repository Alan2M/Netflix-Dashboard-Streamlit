"""Netflix Intelligence — Streamlit, Aulas 21 e 22."""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Netflix Intelligence", page_icon="🎬", layout="wide")
ROOT = Path(__file__).resolve().parent
PREFERRED = ["imdb_rating", "tmdb_rating", "runtime_minutes", "release_year", "imdb_votes", "tmdb_popularity"]
NAMES = {"imdb_rating": "Nota IMDb", "tmdb_rating": "Nota TMDB", "runtime_minutes": "Duração (min)", "release_year": "Ano de lançamento", "imdb_votes": "Votos IMDb", "tmdb_popularity": "Popularidade TMDB", "content_age": "Idade do conteúdo", "country_count": "Quantidade de países", "genre_count": "Quantidade de gêneros", "data_completeness_score": "Completude dos dados", "type": "Tipo de conteúdo", "primary_genre": "Gênero principal", "rating": "Classificação etária", "release_year_group": "Período de lançamento"}

def nome(c):
    return NAMES.get(c, c.replace("_", " ").capitalize())

@st.cache_data(show_spinner=False)
def carregar(caminho):
    return pd.read_csv(caminho)

st.title("🎬 Netflix Intelligence")
st.caption("Análise Exploratória de Dados • Aulas 21 e 22 • Dados originais e tratados da EDA")
with st.sidebar:
    st.header("Controles da análise")
    fonte = st.radio("Base", ["Tratados", "Originais"], horizontal=True)
    arquivo = ROOT / "data" / ("netflix_tratado.csv" if fonte == "Tratados" else "netflix_original.csv")
if not arquivo.exists():
    st.warning("Os CSVs não estão incluídos no arquivo recebido. Execute `python preparar_dados.py` (requer internet) ou a célula de exportação do notebook da EDA.")
    st.stop()

df = carregar(arquivo)
numericas = [c for c in df.select_dtypes(include="number").columns if df[c].notna().sum() >= 2 and df[c].nunique(dropna=True) > 1]
if not numericas:
    st.error("Esta base não possui variáveis quantitativas suficientes para o Dashboard 1.")
    st.stop()

with st.sidebar:
    escolhidas = st.multiselect("Variáveis da correlação", numericas, default=[c for c in PREFERRED if c in numericas][:5], format_func=nome)
    variavel_filtro = st.selectbox("Variável do filtro por intervalo", numericas, format_func=nome)
    serie = pd.to_numeric(df[variavel_filtro], errors="coerce").dropna()
    minimo, maximo = float(serie.min()), float(serie.max())
    intervalo = st.slider("Intervalo permitido", min_value=minimo, max_value=maximo, value=(minimo, maximo)) if minimo < maximo else (minimo, maximo)
    metodo = st.selectbox("Correlação", ["spearman", "pearson", "kendall"])
    st.caption("A seleção do intervalo afeta as duas abas. Linhas sem valor na variável filtrada são excluídas.")

filtrado = df[df[variavel_filtro].between(*intervalo)].copy()
tab1, tab2 = st.tabs(["📊 Dashboard 1 — Correlação e distribuição", "📈 Dashboard 2 — KPIs do catálogo"])

with tab1:
    st.subheader("Distribuições e relações quantitativas")
    a, b, c = st.columns(3)
    a.metric("Títulos filtrados", f"{len(filtrado):,}".replace(",", "."))
    b.metric("Variáveis quantitativas", len(numericas))
    c.metric("Registros fora do filtro", f"{len(df)-len(filtrado):,}".replace(",", "."))
    esquerda, direita = st.columns(2, gap="large")
    with esquerda:
        st.markdown("#### Matriz de correlação")
        if len(escolhidas) == 0:
            st.info("Escolha ao menos duas variáveis na barra lateral. Nenhuma está selecionada.")
        elif len(escolhidas) == 1:
            st.info("Há uma variável selecionada. Escolha uma segunda para comparar.")
        elif len(filtrado) < 3:
            st.warning("A amostra filtrada é pequena demais para análise de correlação.")
        else:
            correlacao = filtrado[escolhidas].corr(method=metodo)
            if correlacao.isna().all().all():
                st.warning("Não foi possível calcular correlações válidas para esta seleção.")
            else:
                fig, ax = plt.subplots(figsize=(7.5, 6))
                sns.heatmap(correlacao, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, center=0, xticklabels=[nome(c) for c in escolhidas], yticklabels=[nome(c) for c in escolhidas], ax=ax)
                ax.tick_params(axis="x", rotation=45)
                ax.tick_params(axis="y", rotation=0)
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
                st.caption("Associação não implica causalidade. Dados ausentes são ignorados em cada par.")
    with direita:
        st.markdown("#### Distribuição (histograma)")
        variavel_hist = st.selectbox("Variável para visualizar", numericas, index=numericas.index("imdb_rating") if "imdb_rating" in numericas else 0, format_func=nome)
        bins = st.slider("Quantidade de faixas", 5, 80, 25, 5)
        valores = filtrado[variavel_hist].dropna()
        if valores.empty:
            st.info("Não há valores válidos para esta seleção.")
        else:
            fig, ax = plt.subplots(figsize=(7.5, 6))
            sns.histplot(valores, bins=bins, color="#E50914", ax=ax)
            ax.axvline(valores.median(), color="#B8B8B8", linestyle="--", linewidth=2, label="Mediana")
            ax.set(xlabel=nome(variavel_hist), ylabel="Quantidade de títulos")
            ax.legend()
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
            st.caption(f"Valores válidos: {len(valores):,} • Média: {valores.mean():.2f} • Mediana: {valores.median():.2f}")
    with st.expander("Inspecionar dados e estatísticas"):
        st.dataframe(filtrado.head(1000), use_container_width=True)
        if not filtrado.empty:
            st.dataframe(filtrado[numericas].describe().T, use_container_width=True)
        st.download_button("Exportar dados filtrados", filtrado.to_csv(index=False).encode("utf-8-sig"), "netflix_filtrado.csv", "text/csv")

with tab2:
    st.subheader("Visão geral do catálogo")
    st.caption("Indicadores recalculados sobre os mesmos títulos filtrados na barra lateral.")
    if filtrado.empty:
        st.warning("Nenhum título atende aos filtros atuais. Amplie o intervalo para ver as métricas.")
    else:
        total = len(filtrado)
        notas = pd.to_numeric(filtrado["imdb_rating"], errors="coerce") if "imdb_rating" in filtrado else pd.Series(dtype=float)
        notas_validas = notas.dropna()
        altas = int((notas_validas >= 7).sum())
        taxa_altas = altas / len(notas_validas) if len(notas_validas) else None
        filmes = (filtrado["type"] == "Movie").sum() if "type" in filtrado else None
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Títulos no recorte", f"{total:,}".replace(",", "."))
        k2.metric("Nota IMDb média", f"{notas_validas.mean():.2f}" if len(notas_validas) else "N/D")
        k3.metric("IMDb ≥ 7,0", f"{taxa_altas:.1%}" if taxa_altas is not None else "N/D", help="Títulos com nota IMDb ≥ 7 divididos pelos títulos com nota IMDb válida.")
        k4.metric("Participação de filmes", f"{filmes/total:.1%}" if filmes is not None else "N/D")
        st.divider()
        categ_disponiveis = [c for c in ["type", "primary_genre", "release_year_group", "rating"] if c in filtrado.columns]
        if categ_disponiveis:
            graf_esq, graf_dir = st.columns([2, 1], gap="large")
            with graf_esq:
                st.markdown("#### Distribuição por categoria")
                categoria = st.selectbox("Agrupar títulos por", categ_disponiveis, format_func=nome)
                limite = st.slider("Quantidade máxima de categorias", 3, 20, 10)
                contagens = filtrado[categoria].fillna("Não informado").astype(str).value_counts().head(limite)
                fig, ax = plt.subplots(figsize=(9, 4.7))
                sns.barplot(x=contagens.values, y=contagens.index, color="#E50914", ax=ax)
                ax.set(xlabel="Quantidade de títulos", ylabel=nome(categoria))
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            with graf_dir:
                st.markdown("#### Leitura do indicador")
                st.write("O gráfico apresenta as categorias mais frequentes dentro do filtro atual. Use-o para identificar a composição do catálogo.")
                st.dataframe(contagens.rename("Títulos").to_frame(), use_container_width=True)
        if "type" in filtrado.columns and "imdb_rating" in filtrado.columns:
            st.markdown("#### Nota IMDb média por tipo de conteúdo")
            medias = filtrado.groupby("type")["imdb_rating"].mean().dropna().sort_values(ascending=False)
            if not medias.empty:
                st.bar_chart(medias.rename("Nota IMDb média"), color="#E50914")
                st.caption("Comparação descritiva. Notas faltantes não entram na média; a base tratada pode conter notas imputadas pela mediana.")
        with st.expander("Definições e limitações dos KPIs"):
            st.write("Os valores apresentados descrevem a amostra filtrada, não necessariamente todo o catálogo atual da plataforma.")
            st.write("Uma nota IMDb ≥ 7 é um critério analítico escolhido para representar títulos bem avaliados, não uma classificação oficial da Netflix.")
            st.write("No tratamento da EDA, notas IMDb e TMDB ausentes foram preenchidas pela mediana; compare com a base original para avaliar a sensibilidade dos resultados.")

st.caption(f"Fonte selecionada: {fonte} • Filtro: {nome(variavel_filtro)} entre {intervalo[0]:g} e {intervalo[1]:g} • Dataset da EDA da Aula 11")
