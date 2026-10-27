# Netflix Intelligence — Aulas 21 e 22 (Streamlit)

Projeto construído a partir do notebook `notebooks/Netflix_EDA.ipynb` e aprimorado para os dois dashboards da disciplina.

## Executar no Windows PowerShell (Python 3.12)

```powershell
py -3.12 -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python preparar_dados.py
python -m streamlit run app.py
```

A execução de `preparar_dados.py` requer internet na primeira vez e baixa a base do Kaggle referenciada no notebook. Como os CSVs não estavam no ZIP enviado, é necessário gerá-los antes de abrir o dashboard; alternativamente rode a exportação no notebook. Compare os CSVs resultantes com a EDA original antes de enviar.

## Estrutura

- `app.py`: duas abas, controles globais, correlação, distribuição, KPIs e barras.
- `.streamlit/config.toml`: identidade visual temática.
- `entregas/justificativa-metricas.md`: planejamento e fundamentação de quatro indicadores.
- `entregas/rascunho-dashboard2.jpg`: rascunho visual do segundo dashboard.
- `prompts/declaracao-uso-ia.md`: declaração de assistência de IA.
- `notebooks/Netflix_EDA.ipynb`: EDA da Aula 11 com exportação das bases.
- `preparar_dados.py`: prepara os CSVs quando não disponíveis.

## Checklist de validação

1. Gerar `data/netflix_original.csv` e `data/netflix_tratado.csv`.
2. Executar o Streamlit com dados reais.
3. Testar correlação com 0, 1 e 2 ou mais variáveis; testar filtros estreitos e amplos.
4. Confirmar o recálculo dos KPIs e do gráfico de barras ao mudar o intervalo e a base.
5. Verificar as justificativas e personalizar o rascunho, caso necessário.
6. Fazer commit e push do projeto; incluir os CSVs gerados se exigido pela professora.

Não é preciso concluir todo o Dashboard 2 nesta aula; o arquivo já inclui uma implementação inicial funcional para facilitar a continuidade.
