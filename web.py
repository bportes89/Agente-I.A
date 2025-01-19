import streamlit as st
import sys
import os
import time
import pandas as pd
from datetime import datetime

# Adiciona o diretório pai ao path do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.agent import IAAgent

# Configuração da página
st.set_page_config(
    page_title="Agente IA Avançado",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

def check_password():
    """Retorna `True` se o usuário tiver a senha correta."""
    def password_entered():
        if st.session_state["password"] == "senha123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Digite a senha", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    
    return st.session_state["password_correct"]

def main():
    if not check_password():
        st.stop()
    
    # Layout principal
    st.title("🤖 Agente IA Avançado")
    
    # Inicializa o agente
    if 'agent' not in st.session_state:
        with st.spinner('Inicializando o agente...'):
            st.session_state.agent = IAAgent()
            st.session_state.historico = []
    
    # Sidebar com opções
    with st.sidebar:
        st.header("⚙️ Configurações")
        modo = st.selectbox(
            "Selecione o modo:",
            ["Conversa", "Análise de Sentimento", "Resumo de Texto"]
        )
        
        st.header("📊 Estatísticas")
        if st.session_state.historico:
            df = pd.DataFrame(st.session_state.historico)
            st.write(f"Total de interações: {len(df)}")
            
        st.header("ℹ️ Sobre")
        st.write("Este é um agente de IA avançado com múltiplas funcionalidades.")
        st.write("Desenvolvido como exemplo educacional.")
    
    # Área principal
    if modo == "Conversa":
        prompt = st.text_area("💭 Digite sua pergunta:", height=100)
        col1, col2 = st.columns([1, 4])
        with col1:
            max_length = st.slider("Tamanho máximo:", 50, 200, 100)
        
        if st.button("📤 Enviar", use_container_width=True):
            if prompt:
                with st.spinner("🤔 Pensando..."):
                    # Simula processamento para melhor UX
                    time.sleep(0.5)
                    resposta = st.session_state.agent.gerar_resposta(
                        prompt,
                        max_length=max_length
                    )
                    st.session_state.historico.append({
                        'timestamp': datetime.now(),
                        'modo': modo,
                        'entrada': prompt,
                        'saida': resposta
                    })
                    
                st.success("✨ Resposta gerada!")
                st.write("### 🤖 Resposta:")
                st.write(resposta)
            else:
                st.warning("⚠️ Por favor, digite uma pergunta.")
    
    elif modo == "Análise de Sentimento":
        texto = st.text_area("📝 Digite o texto para análise:", height=100)
        if st.button("📊 Analisar Sentimento", use_container_width=True):
            if texto:
                with st.spinner("🔍 Analisando..."):
                    sentimento = st.session_state.agent.analisar_sentimento(texto)
                    st.write("### 📊 Resultado da Análise:")
                    st.json(sentimento)
            else:
                st.warning("⚠️ Por favor, digite um texto para análise.")
    
    elif modo == "Resumo de Texto":
        texto = st.text_area("📝 Digite o texto para resumir:", height=200)
        if st.button("📝 Gerar Resumo", use_container_width=True):
            if texto:
                with st.spinner("✂️ Resumindo..."):
                    resumo = st.session_state.agent.resumir_texto(texto)
                    st.write("### 📋 Resumo:")
                    st.write(resumo)
            else:
                st.warning("⚠️ Por favor, digite um texto para resumir.")
    
    # Histórico de interações
    if st.session_state.historico:
        st.write("---")
        st.write("### 📜 Histórico de Interações")
        df = pd.DataFrame(st.session_state.historico)
        st.dataframe(df)

if __name__ == "__main__":
    main()