# Justificativa das métricas — Dashboard 2 (Netflix Intelligence)

**Base:** dataset Netflix enriquecido com IMDb e TMDB, analisado na EDA da Aula 11. As métricas se atualizam com o intervalo escolhido pelo usuário. Elas descrevem o recorte analisado, não o catálogo atual da Netflix.

## 1. Quantidade de títulos
- **Variável:** registros da tabela (uma linha por título, conforme a base utilizada).
- **O que mede:** quantidade de linhas incluídas após o filtro de intervalo.
- **Por que foi escolhida:** permite compreender o tamanho da amostra que sustenta os demais indicadores.
- **Público-alvo:** analistas de conteúdo e responsáveis pelo catálogo.
- **Decisão apoiada:** verificar representatividade antes de comparar segmentos.
- **O que comunica:** dimensão do recorte selecionado.

## 2. Nota média IMDb
- **Variável:** `imdb_rating`.
- **O que mede:** média das notas IMDb válidas no recorte.
- **Por que foi escolhida:** resume a avaliação agregada do conteúdo analisado.
- **Público-alvo:** analistas de conteúdo e curadoria.
- **Decisão apoiada:** investigar subgrupos com notas acima ou abaixo da média.
- **O que comunica:** avaliação média, sem inferir satisfação de todos os espectadores.

## 3. Proporção de títulos bem avaliados
- **Variável:** `imdb_rating`.
- **O que mede:** porcentagem das notas válidas maiores ou iguais a 7,0.
- **Por que foi escolhida:** complementa a média com uma medida de proporção acima de um limiar simples.
- **Público-alvo:** analistas de qualidade do catálogo.
- **Decisão apoiada:** comparar a presença de títulos mais bem avaliados entre recortes.
- **O que comunica:** concentração de notas elevadas sob um critério analítico, não oficial.

## 4. Participação de filmes
- **Variável:** `type`.
- **O que mede:** registros com `type = Movie` divididos pelo total de registros filtrados.
- **Por que foi escolhida:** revela o equilíbrio entre filmes e outros tipos de conteúdo.
- **Público-alvo:** gestores e analistas de portfólio.
- **Decisão apoiada:** identificar desbalanceamentos e explorar a diversidade de formatos.
- **O que comunica:** peso dos filmes no recorte.

## Visualizações planejadas
- **Barras de quantidade por categoria:** `type`, `primary_genre`, `release_year_group` ou `rating`; permite inspecionar a distribuição de frequências.
- **Barras da média IMDb por `type`:** ajuda a comparar avaliações agregadas por formato.

## Cuidado metodológico
A base tratada utiliza imputação pela mediana em `imdb_rating` e `tmdb_rating`, de acordo com a EDA. Isso pode alterar médias, distribuições e percentuais. Utilize a alternância entre bases original e tratada para avaliar diferenças. Valores faltantes na base original são excluídos do denominador de indicadores baseados em notas.
