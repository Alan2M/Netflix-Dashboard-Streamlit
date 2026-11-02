# Justificativa das métricas — Dashboard 2

Público-alvo: estudantes, analistas de conteúdo e gestores interessados na composição de um catálogo de streaming. As métricas descrevem **o dataset**, não resultados financeiros ou audiência real da Netflix.

| Indicador | Variável / cálculo | Por que escolher | Decisão apoiada | Leitura |
|---|---|---|---|---|
| Títulos no recorte | `len(df_filtrado)` | Dimensiona o universo analisado | Verificar representatividade de filtros | Quantos registros restaram |
| Nota IMDb média | Média não nula de `imdb_rating` | Indica nível médio de avaliações | Comparar segmentos | Maior média não implica melhor desempenho comercial |
| Proporção IMDb ≥ 7 | Títulos com `imdb_rating >= 7` / títulos com IMDb válido | Resume quantidade relativa de avaliações altas | Identificar segmentos com maior concentração de notas altas | Percentual do grupo com nota disponível |
| Participação de filmes | Contagem de `type == Movie` / total | Mostra composição do catálogo | Examinar equilíbrio entre formatos | Percentual do recorte que é filme |

Os três visuais complementares do Dashboard 2 são: **barras por tipo**, **barras horizontais dos oito principais gêneros** e **área de títulos por ano de lançamento**. Todos mudam com os filtros compartilhados. Notas imputadas pela mediana na base tratada podem mudar a distribuição; comparar com a base original é recomendado.
