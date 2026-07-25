import os
import requests
import streamlit as st
from dotenv import load_dotenv

# =========== CARREGAR VARIÁVEIS DE AMBIENTE ===========
# Carrega as chaves escondidas do arquivo .env local
load_dotenv()

# =========== CONFIGURAÇÃO DA IA (NUVEM GROQ) ===========
# Puxa a chave de forma segura do sistema (do seu arquivo .env)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODELO = "llama-3.1-8b-instant"

# =========== CARREGAR BASE DE CONHECIMENTO ===========
try:
    with open("./data/conhecimento_sql.txt", "r", encoding="utf-8") as f:
        base_conhecimento = f.read()
except FileNotFoundError:
    base_conhecimento = "Responda com conhecimentos gerais de SQL e banco de dados."

# =========== SYSTEM PROMPT (DBA MENTOR) ===========
SYSTEM_PROMPT = f"""Você é o DBA Mentor, um especialista sênior em Banco de Dados, didático e paciente.

REGRAS DE OURO:
1. Você SÓ PODE responder sobre Banco de Dados, SQL, Modelagem e Tecnologia.
2. Se o usuário perguntar sobre QUALQUER outro assunto (ex: comprar celular, viagens, esportes), responda EXATAMENTE: "Desculpe, mas meu foco é ajudar você apenas com assuntos de Banco de Dados e Tecnologia."
3. Responda 100% em Português do Brasil.
4. Seja direto, use no máximo 3 parágrafos e formate comandos SQL em blocos identados.

BASE DE CONHECIMENTO TÉCNICA:
{base_conhecimento}
"""

# =========== FUNÇÃO DE COMUNICAÇÃO ===========
def perguntar(msg, historico):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 1. Coloca a regra do DBA Mentor como a instrução principal
    mensagens_api = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # 2. Adiciona as últimas interações do chat para a IA "ter memória"
    for h in historico[-4:]: 
        mensagens_api.append({"role": h["role"], "content": h["content"]})
        
    # 3. Adiciona a pergunta atual do usuário
    mensagens_api.append({"role": "user", "content": msg})
    
    dados = {
        "model": MODELO,
        "messages": mensagens_api,
        "temperature": 0.2 
    }
    
    try:
        r = requests.post(GROQ_URL, headers=headers, json=dados)
        retorno = r.json()
        
        # Verifica se a API devolveu a resposta corretamente
        if 'choices' in retorno:
            return retorno['choices'][0]['message']['content']
        else:
            return f"Erro retornado pela API: {retorno}"
            
    except Exception as e:
        return f"Erro de conexão com a API: {e}"

# =========== INTERFACE (STREAMLIT) ===========
st.set_page_config(page_title="DBA Mentor", page_icon="🗄️")
st.title("🗄️ DBA Mentor, seu Assistente de Banco de Dados")

# Inicializar histórico do chat na memória do Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensagens anteriores na tela sempre que atualizar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de texto para o usuário digitar
if prompt := st.chat_input("Sua dúvida sobre modelagem, normalização ou SQL..."):
    # Mostra a pergunta do usuário na tela
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Chama a IA e mostra o resultado
    with st.chat_message("assistant"):
        with st.spinner("Analisando estrutura de dados..."):
            resposta = perguntar(prompt, st.session_state.messages)
            st.markdown(resposta)
            
    # Salva o papo no histórico para a IA lembrar depois
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": resposta})