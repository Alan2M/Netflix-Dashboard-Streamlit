"""Reproduz os dados originais e tratados conforme a EDA da Aula 11."""
from pathlib import Path
import pandas as pd
import numpy as np
import kagglehub

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'data' / 'clean'
OUT.mkdir(parents=True, exist_ok=True)
source = Path(kagglehub.dataset_download('zohairbaloch/netflix-titles-enriched-with-imdb-and-tmdb')) / 'netflix_content_intelligence_combined.csv'
if not source.is_file():
    raise FileNotFoundError(f'Dataset esperado não encontrado: {source}')
original = pd.read_csv(source, low_memory=False)
original.to_csv(OUT / 'netflix_original.csv', index=False)
tratado = original.copy()
for col in ('imdb_rating','tmdb_rating'):
    if col in tratado:
        tratado[col] = pd.to_numeric(tratado[col], errors='coerce')
        tratado[col] = tratado[col].fillna(tratado[col].median())
if 'primary_genre' in tratado:
    tratado['primary_genre'] = tratado['primary_genre'].fillna('Não informado')
if 'imdb_votes' in tratado:
    tratado['imdb_votes_log'] = np.log1p(pd.to_numeric(tratado['imdb_votes'],errors='coerce').clip(lower=0))
tratado.to_csv(OUT / 'netflix_tratado.csv', index=False)
print(f'{len(original)} linhas exportadas; arquivos em {OUT}')
