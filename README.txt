# Dashboard Analítico de Vendas (UFPI)

## Conteúdo
- `app.py`: código do dashboard Streamlit.
- `vendas.csv`: base de dados fictícia para demonstração.
- `requirements.txt`: bibliotecas necessárias.
- `relatorio_projeto.docx`: documento explicativo inicial.

## Executar no computador
1. Instale Python 3.10 ou superior.
2. Extraia todos os arquivos para a mesma pasta.
3. Abra o terminal nessa pasta.
4. Execute: `python -m pip install -r requirements.txt`
5. Execute: `streamlit run app.py`
6. O navegador abrirá o painel localmente.

## Publicar gratuitamente no Streamlit Community Cloud
1. Crie/acesse uma conta no GitHub.
2. Crie um repositório e envie `app.py`, `vendas.csv` e `requirements.txt`.
3. Entre em https://share.streamlit.io/ e conecte o GitHub.
4. Escolha o repositório, selecione `app.py` e clique em Deploy.
5. Teste o link público em janela anônima antes de entregar.

## Observação
A base contém dados fictícios, não dados de uma empresa real. O funcionamento das seleções de gráfico depende da versão do Streamlit instalada; os filtros laterais atualizam todos os componentes.
