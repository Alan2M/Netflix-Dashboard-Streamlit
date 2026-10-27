"""Baixa o dataset original utilizado na EDA e gera os dois CSVs para Streamlit.
Requer internet na primeira execução: python preparar_dados.py
"""
from pathlib import Path
import pandas as pd
import kagglehub

raiz = Path(__file__).resolve().parent
pasta = raiz / "data"
pasta.mkdir(exist_ok=True)
origem = Path(kagglehub.dataset_download("zohairbaloch/netflix-titles-enriched-with-imdb-and-tmdb"))
arquivo = origem / "netflix_content_intelligence_combined.csv"
if not arquivo.exists():
    raise FileNotFoundError(f"Arquivo esperado não encontrado: {arquivo}")
df = pd.read_csv(arquivo)
df.to_csv(pasta / "netflix_original.csv", index=False)
tratado = df.copy()
for coluna in ["imdb_rating", "tmdb_rating"]:
    if coluna in tratado.columns:
        tratado[coluna] = tratado[coluna].fillna(tratado[coluna].median())
if "primary_genre" in tratado.columns:
    tratado["primary_genre"] = tratado["primary_genre"].fillna("Não informado")
tratado.to_csv(pasta / "netflix_tratado.csv", index=False)
print(f"Exportados {len(df)} registros para {pasta}")
