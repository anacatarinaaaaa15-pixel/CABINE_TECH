import streamlit as st
from rembg import remove
from PIL import Image
import qrcode
import os
import uuid
from io import BytesIO

# --- CONFIGURAÇÃO DE AMBIENTE ---
# Pasta onde as fotos ficam acessíveis publicamente no servidor
PASTA_FOTOS = "static" 
if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS)

st.set_page_config(page_title="Liga de IA UNIFESP - Cabine", layout="centered")

# --- ESTADO DO SISTEMA ---
if 'foto_final_url' not in st.session_state:
    st.session_state['foto_final_url'] = None
if 'nome_arquivo' not in st.session_state:
    st.session_state['nome_arquivo'] = None

st.title("📸 Cabine de Fotos")

# --- INTERFACE DE UPLOAD ---
col1, col2 = st.columns(2)
with col1:
    arq_aluno = st.file_uploader("1. Foto do Aluno", type=['jpg', 'png', 'jpeg'])
with col2:
    arq_fundo = st.file_uploader("2. Moldura da Liga", type=['jpg', 'png', 'jpeg'])

if arq_aluno and arq_fundo:
    if st.button("🚀 PROCESSAR FOTO"):
        with st.spinner("Removendo fundo e aplicando estilo..."):
            img_aluno = Image.open(arq_aluno).convert("RGBA")
            img_fundo = Image.open(arq_fundo).convert("RGBA")
            
            # Processamento
            sem_fundo = remove(img_aluno)
            img_fundo = img_fundo.resize(sem_fundo.size)
            img_fundo.paste(sem_fundo, (0, 0), sem_fundo)
            
            # Nome único para cada aluno
            nome_foto = f"{uuid.uuid4().hex}.png"
            caminho_salvamento = os.path.join(PASTA_FOTOS, nome_foto)
            img_fundo.save(caminho_salvamento)
            
            # Salva no estado da sessão
            st.session_state['foto_final_url'] = caminho_salvamento
            st.session_state['nome_arquivo'] = nome_foto

# --- EXIBIÇÃO E QR CODE DINÂMICO ---
if st.session_state['foto_final_url']:
    st.image(st.session_state['foto_final_url'], caption="Sua foto está pronta!")

    # LOGICA DO LINK AUTOMÁTICO:
    # O Streamlit não dá a URL completa facilmente, mas podemos 
    # instruir o aluno a baixar ou usar um link relativo se for no PC.
    # Como você vai rodar no Streamlit Cloud, o link padrão é:
    
    # PEGAR O NOME DO ARQUIVO DA SESSÃO
    nome = st.session_state['nome_arquivo']
    
    # Aqui, a única coisa que você muda uma VEZ só é o domínio do seu app
    # Ex: https://cabine-unifesp.streamlit.app
    # Se você ainda não sabe o link, pode deixar assim e o QR Code vai
    # funcionar assim que você descobrir a URL final do deploy.
    
    dominio_do_app = st.text_input("Cole o link do seu App aqui (só na primeira vez):", "https://cabinetechgit-mjzmesbpatxk4vapneqxmf.streamlit.app")
    
    link_download = f"{dominio_do_app}/app/static/{nome}"

    # Gerar QR Code
    qr = qrcode.make(link_download)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    
    st.success("✅ Escaneie para baixar direto no seu celular:")
    st.image(buf.getvalue(), width=250)
    
    # Opção extra: Botão de download direto (caso o QR Code falhe no 4G)
    with open(st.session_state['foto_final_url'], "rb") as file:
        st.download_button(
            label="💾 Baixar Foto no Computador",
            data=file,
            file_name="foto_liga_ia.png",
            mime="image/png"
        )
    
    if st.button("🔄 Novo Aluno"):
        st.session_state['foto_final_url'] = None
        st.session_state['nome_arquivo'] = None
        st.rerun()