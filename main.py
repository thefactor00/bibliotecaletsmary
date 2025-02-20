import streamlit as st
from PIL import Image
import pandas as pd
import streamlit as st

# Função para autenticar o login
def verificar_login(usuario, senha):
    # Defina suas credenciais
    usuario_correto = "lets"
    senha_correta = "lets@2025"
    
    if usuario == usuario_correto and senha == senha_correta:
        return True
    else:
        return False

# Configuração da página
st.set_page_config(page_title="Lets Mary Biblioteca", page_icon="📚", layout="wide")

# # Aplicar tema branco fixo
def aplicar_tema():
    st.markdown(
        """
        <style>
            html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
                background-color: #ffffff !important;
                color: #000000 !important;
            }
            h1, h2, h3, h4, h5, h6, p, div, span, label {
                color: #000000 !important;
            }
            .stButton > button {
                background-color: #45d0c1 !important;
                color: white !important;
                border-radius: 5px !important;
                border: none !important;
            }
            /* Ajustando os inputs */
            input[type="text"], input[type="password"], textarea, select {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 1px solid #ccc !important;
                border-radius: 5px !important;
                padding: 8px !important;
            }
            input::placeholder, textarea::placeholder {
                color: #666 !important;
            }
            /* Ajustando os dropdowns (multiselect) */
            [data-baseweb="select"] > div {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 1px solid #ccc !important;
                border-radius: 5px !important;
                padding: 5px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

aplicar_tema()

# Estilo CSS para deixar o front mais refinado
st.markdown("""
    <style>
        .reportview-container { margin-top: -2em; }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}

        /* Estilo do título */
        h1 {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: lighter;
            font-size: 40px;
            color: #fff;  /* Fonte branca */
            text-align: center;
            margin-bottom: 10px;
            pointer-events: none; /* Torna o título não clicável */
        }

        /* Estilo do subtítulo */
        h2 {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: lighter;
            font-size: 24px;
            color: #fff;  /* Fonte branca */
            text-align: center;
            margin-top: 0;
            margin-bottom: 20px;
            pointer-events: none; /* Torna o título não clicável */
        }

        /* Estilo geral do texto */
        .stMarkdown {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: lighter;
            color: #fff;  /* Fonte branca */
        }

        /* Estilo do botão */
        .stButton > button {
            background-color: #45d0c1;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            border-radius: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# Texto de boas-vindas com fontes refinadas
st.markdown('<h1>Bem-vindo(a) à biblioteca da Lets Mary</h1>', unsafe_allow_html=True)
st.markdown('<h2>Aqui você encontra toda coleção da Leticia Ribeiro</h2>', unsafe_allow_html=True)

st.divider()

# Carregar o DataFrame
df = pd.read_excel('dados - Copia.xlsx', sheet_name='TODOS OS VOLUMES')

# Filtros de pesquisa na mesma linha
col1, col2, col3, col4 = st.columns(4)

with col1:
    titulo_input = st.multiselect(
        "Selecione ou pesquise o nome do livro", placeholder="Escolha uma opção",
        options=sorted(df['TÍTULO'].unique())  # Ordena os títulos
    )

with col2:
    autor_input = st.multiselect(
        "Selecione os autores", options=sorted(df['AUTOR'].unique())  # Inclui a opção vazia
    )

with col3:
    editora_input = st.multiselect(
        "Selecione as editoras", options=sorted(df['EDITORA'].unique())  # Inclui a opção vazia
    )

with col4:
    status_input = st.multiselect(
        "Selecione os status de leitura", options=sorted(df['STATUS DE LEITURA'].astype(str).unique())  # Inclui a opção vazia
    )
    # Aplicar filtro de título
    if titulo_input:
        df = df[df['TÍTULO'].isin(titulo_input)]

    if autor_input:
        df = df[df['AUTOR'].isin(autor_input)]

    if editora_input:
        df = df[df['EDITORA'].isin(editora_input)]

    if status_input:
        df = df[df['STATUS DE LEITURA'].isin(status_input)]

    # Paginamento
    results_per_page = 12
    total_pages = len(df) // results_per_page + (1 if len(df) % results_per_page > 0 else 0)

    # Inicializando a página
    if 'page' not in st.session_state:
        st.session_state.page = 1

    # Botões de navegação (setas)
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button("⬅️ Anterior") and st.session_state.page > 1:
            st.session_state.page -= 1

    with col3:
        if st.button("➡️ Próximo") and st.session_state.page < total_pages:
            st.session_state.page += 1

    # Exibição do contador de páginas
    st.markdown(f"""
        <div style="text-align: center; font-size: 14px; font-weight: bold;">
            Página {st.session_state.page} de {total_pages}
        </div>
    """, unsafe_allow_html=True)

    # Exibição dos cards
    start_idx = (st.session_state.page - 1) * results_per_page
    end_idx = start_idx + results_per_page
    page_data = df.iloc[start_idx:end_idx]

    if not page_data.empty:
        num_results = len(page_data)
        cols_per_row = 4

        for i in range(0, num_results, cols_per_row):
            cols = st.columns(min(cols_per_row, num_results - i))

            for j, row in enumerate(page_data.iloc[i:i+cols_per_row].iterrows()):
                with cols[j]:
                    card_html = f"""
                    <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px; height: auto; text-align: center;">
                    """
                    
                    # Exibir status de leitura (faixa de "Livro Disponível")
                    status_leitura = row[1]['STATUS DE LEITURA']
                    if status_leitura:  # Verifica se existe algum valor na coluna
                        if status_leitura.lower() == 'não lido':  # Para "Não Lido", cor vermelha
                            card_html += f"""<div style='background-color: #ff4f4f; border: 1px solid #ff4f4f; color: #ffffff; padding: 1px; border-radius: 5px 5px 0px 0px; margin-bottom: 5px;'>
                          <strong>📕 {status_leitura}</strong>
                        </div>
                      """
                        elif status_leitura.lower() == 'lendo':  # Para "Lendo", cor azul
                            card_html += f"""<div style='background-color: #007bff; border: 1px solid #007bff; color: #ffffff; padding: 1px; border-radius: 5px 5px 0px 0px; margin-bottom: 5px;'>
                          <strong>📘 {status_leitura}</strong>
                        </div>
                      """
                        else:  # Para outros status, cor verde
                            card_html += f"""<div style='background-color: #45d0c1; border: 1px solid #45d0c1; color: #ffffff; padding: 1px; border-radius: 5px 5px 0px 0px; margin-bottom: 5px;'>
                          <strong>📗 {status_leitura}</strong>
                        </div>
                      """
                    # Imagem do livro
                    card_html += f"""
                    <img src="{row[1]['LINK DA IMAGEM']}" style="width: 200px; height: auto; display: block; margin-left: auto; margin-right: auto;"/>
                    """
                    
                    # Título, Autor, Editora, Código
                    card_html += f"""
                    <h4 style="color:#ffffff; margin: 5px 0; font-size: 18px; font-weight: bold; text-align: center; color: #ffffff; font-family: Arial, sans-serif; text-transform: uppercase; pointer-events: none;">{row[1]['TÍTULO']}</h4>
                    <p style="margin: 5px 0; font-size: 14px; font-family: Arial, sans-serif;"><strong>Autor:</strong> {row[1]['AUTOR']}</p>
                    <p style="margin: 5px 0; font-size: 14px; font-family: Arial, sans-serif;"><strong>Editora:</strong> {row[1]['EDITORA']}</p>
                    <p style="margin: 5px 0; font-size: 14px; font-family: Arial, sans-serif;"><strong>Código:</strong> {row[1]['CÓDIGO']}</p>
                    """

                    # Link do livro
                    link = row[1]['LINK DO LIVRO']
                    card_html += f'<div style="text-align: center;"><a href="{link}" target="_blank"><button>💡 Acessar</button></a></div>'

                    card_html += "</div>"

                    st.markdown(card_html, unsafe_allow_html=True)

    else:
        st.markdown("<h2>Não há livros disponíveis para esta busca.</h2>", unsafe_allow_html=True)
