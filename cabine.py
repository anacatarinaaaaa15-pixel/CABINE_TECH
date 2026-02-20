import streamlit as st
from rembg import remove
from PIL import Image
import qrcode
import os
import uuid
from io import BytesIO

# --- CONFIGURAÇÃO DE AMBIENTE ---
# Na nuvem, usamos caminhos temporários do sistema
PASTA_FOTOS = "static" 
if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS)

st.set_page_config(page_title="Liga de IA UNIFESP - Cabine", layout="centered")

# --- ESTADO DO SISTEMA ---
if 'foto_final_url' not in st.session_state:
    st.session_state['foto_final_url'] = None

st.title("📸 Cabine de Fotos - Liga de IA")
st.write("Transforme sua foto com nossa Inteligência Artificial!")

# --- INTERFACE DE UPLOAD ---
col1, col2 = st.columns(2)
with col1:
    arq_aluno = st.file_uploader("1. Foto do Aluno", type=['jpg', 'png', 'jpeg'])
with col2:
    # Dica: Você pode deixar a moldura fixa no código se preferir não subir toda hora
    arq_fundo = st.file_uploader("2. Moldura da Liga", type=['jpg', 'png', 'jpeg'])

if arq_aluno and arq_fundo:
    if st.button("🚀 PROCESSAR FOTO"):
        with st.spinner("Removendo fundo e aplicando estilo..."):
            # Processamento em memória
            img_aluno = Image.open(arq_aluno).convert("RGBA")
            img_fundo = Image.open(arq_fundo).convert("RGBA")
            
            # IA de remoção de fundo
            sem_fundo = remove(img_aluno)
            
            # Redimensionar fundo para bater com a foto (ou vice-versa)
            img_fundo = img_fundo.resize(sem_fundo.size)
            img_fundo.paste(sem_fundo, (0, 0), sem_fundo)
            
            # Salvar temporariamente para o download
            nome_foto = f"{uuid.uuid4().hex}.png"
            caminho_salvamento = os.path.join(PASTA_FOTOS, nome_foto)
            img_fundo.save(caminho_salvamento)
            
            # Na nuvem, o Streamlit gera o link público automaticamente
            st.session_state['foto_final_url'] = caminho_salvamento
            st.session_state['nome_arquivo'] = nome_foto

# --- EXIBIÇÃO E QR CODE ---
if st.session_state['foto_final_url']:
    foto_path = st.session_state['foto_final_url']
    st.image(foto_path, caption="Sua foto está pronta!")

    # Gerar QR Code que aponta para o arquivo na pasta static
    # O Streamlit Cloud serve arquivos da pasta /static via URL
    # No dia do evento, substitua o link abaixo pela URL que o Streamlit te der
    url_do_site = "https://sua-cabine.streamlit.app" # Link final após o deploy
    link_download = f"{url_do_site}/app/static/{st.session_state['nome_arquivo']}"

    qr = qrcode.make(link_download)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    
    st.success("✅ Escaneie o QR Code abaixo para baixar:")
    st.image(buf.getvalue(), width=250)
    
    if st.button("🔄 Novo Aluno"):
        st.session_state['foto_final_url'] = None
        st.rerun()