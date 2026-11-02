# Validação final dos dashboards — Aula 23

## Conferências estáticas realizadas

- Código `app.py` e `preparar_dados.py`: compilação Python sem erro de sintaxe.
- Dashboard 1: seletor de variáveis trata 0 e 1 seleção; 2 ou mais calcula correlação; intervalo numérico agora filtra histograma **e** correlação.
- Dashboard 2: quatro KPIs e três gráficos, alimentados pela base filtrada.
- Dataset: fonte e transformações baseadas no notebook EDA da Aula 11.
- Documentação: justificativa, declaração de IA, rascunhos de referência, README, tema e dependências.

## Testes que o responsável precisa executar com os dados reais

- [ ] `python preparar_dados.py` com internet e comparar contagem/colunas com a EDA.
- [ ] `python -m streamlit run app.py` carrega ambas as abas sem erros.
- [ ] Matriz reage à troca de variável, método e intervalo; testa 0, 1, 2 ou mais variáveis.
- [ ] Histograma reage ao intervalo, número de faixas e filtros laterais.
- [ ] Dashboard 2: quatro métricas e três gráficos reagem aos filtros.
- [ ] CSV tratado e original incluídos no GitHub; nenhum segredo/venv.
- [ ] App publicado, aberto em janela anônima e link real no README.

**Status:** validação estática concluída; validação real e deploy não realizados neste ambiente. Não declarar conclusão final antes de marcar as etapas restantes.
