# ◈ Netflix Atlas — Inteligência de Catálogo

Dashboard acadêmico em **Streamlit** para as Aulas 21–23 de Análise e Visualização de Dados, desenvolvido a partir da EDA do catálogo Netflix enriquecido com dados IMDb/TMDB.

**Aplicação publicada:** `INSERIR_AQUI_O_LINK_APOS_O_DEPLOY` (o deploy deve ser realizado pelo proprietário do repositório).

## Funcionalidades

- **Dashboard 1 · EDA e Correlações:** matriz de correlação interativa (Spearman/Pearson/Kendall), histograma ajustável, filtro numérico por intervalo, dados e estatísticas descritivas.
- **Dashboard 2 · Inteligência do catálogo:** quatro KPIs (total, IMDb médio, percentual com IMDb ≥ 7, proporção de filmes) e três gráficos complementares (formato, gêneros, lançamentos por ano).
- Filtros compartilhados para tipo, gênero e ano, seleção entre base original e tratada, cache de leitura, download de CSV e identidade visual própria azul-petróleo/verde-água/lilás.

## Executar localmente (PowerShell)

```powershell
py -3.12 -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python preparar_dados.py
python -m streamlit run app.py
```

`preparar_dados.py` requer internet na primeira execução e baixa o dataset `zohairbaloch/netflix-titles-enriched-with-imdb-and-tmdb` do Kaggle. Os arquivos CSV **não vieram no ZIP de origem**, por isso precisam ser gerados e versionados antes do deploy. A base tratada utiliza imputação por mediana para IMDb/TMDB e categoria para gênero ausente, conforme o notebook.

## Publicar no Streamlit Community Cloud

1. Execute `python preparar_dados.py` localmente e confirme `data/clean/netflix_original.csv` e `data/clean/netflix_tratado.csv`.
2. Teste o app. Execute `git status`, `git add app.py preparar_dados.py requirements.txt README.md .gitignore .streamlit/config.toml notebooks entregas prompts data` e `git commit -m "Aula 23 - Netflix Atlas dashboards e deploy"`; depois `git push origin main`.
3. Acesse **https://share.streamlit.io/** e conecte sua conta GitHub.
4. Selecione **Create app → Deploy a public app from GitHub**, repositório `Alan2M/Netflix-Dashboard-Streamlit`, branch `main` e arquivo principal `app.py`. Escolha Python 3.12 em Advanced settings, se disponível.
5. Após a publicação, abra em janela anônima, teste os filtros nas duas abas e **substitua o marcador do link no início deste README** pelo URL real do app. Faça novo commit e push do README.

### Checklist de entrega

- [ ] CSVs gerados e enviados para `data/clean/`
- [ ] App abre localmente sem erros e filtros atualizam os gráficos
- [ ] Dashboard 1 suporta 0, 1 e 2+ variáveis
- [ ] Dashboard 2 contém quatro KPIs e três visuais
- [ ] `entregas/` contém os dois rascunhos e justificativa das métricas
- [ ] `prompts/declaracao-uso-ia.md` revisado
- [ ] GitHub público, branch `main`, `git status` limpo
- [ ] Link real do app incluído neste README
- [ ] App público testado em janela anônima

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
