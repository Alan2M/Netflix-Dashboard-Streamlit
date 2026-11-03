# ◈ Netflix Atlas — Inteligência de Catálogo

Dashboard acadêmico em **Streamlit** para as Aulas 21–23 de Análise e Visualização de Dados, desenvolvido a partir da EDA do catálogo Netflix enriquecido com dados IMDb/TMDB.

**Aplicação publicada:** `https://netflix-dashboard-app-alan.streamlit.app`

## Funcionalidades

- **Dashboard 1 · EDA e Correlações:** matriz de correlação interativa (Spearman/Pearson/Kendall), histograma ajustável, filtro numérico por intervalo, dados e estatísticas descritivas.
- **Dashboard 2 · Inteligência do catálogo:** quatro KPIs (total, IMDb médio, percentual com IMDb ≥ 7, proporção de filmes) e três gráficos complementares (formato, gêneros, lançamentos por ano).
- Filtros compartilhados para tipo, gênero e ano, seleção entre base original e tratada, cache de leitura, download de CSV e identidade visual própria azul-petróleo/verde-água/lilás.

## Estrutura

```
app.py
preparar_dados.py
requirements.txt
.streamlit/config.toml
notebooks/Netflix_Aula_11_EDA_Original.ipynb
data/clean/netflix_original.csv  (gerado)
data/clean/netflix_tratado.csv (gerado)
entregas/rascunho-dashboard1.jpg
entregas/rascunho-dashboard2.jpg
entregas/justificativa-metricas.md
prompts/declaracao-uso-ia.md
```

**Observação:** os rascunhos são layouts esquemáticos produzidos como documentação da interface, não capturas da aplicação executada. Projeto educacional não afiliado à Netflix.

## Fidelidade à EDA original

O notebook da Aula 11 identifica assimetrias, ausência relevante nas avaliações IMDb/TMDB e mantém outliers considerados plausíveis. O preparo do dashboard segue suas opções: mediana nas duas notas, gênero ausente como “Não informado”, e coluna derivada `imdb_votes_log`. A base original mantém ausências e não recebe essas transformações. Para evitar interpretação equivocada, os indicadores da base tratada podem incluir avaliações imputadas. A correlação inicial sugerida é Spearman, como no notebook.

**Rascunhos:** estão incluídos dois esquemas digitais de referência; se a professora avaliar o desenho feito pelo estudante, substitua-os pelas suas imagens desenhadas no Paint.
