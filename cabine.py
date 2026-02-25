import streamlit as st
from rembg import remove
from PIL import Image
import qrcode
import os
import uuid
import base64
import requests
from io import BytesIO

# ==============================
# CONFIGURAÇÃO
# ==============================

PASTA_FOTOS = "static"
if not os.path.exists(PASTA_FOTOS):
    os.makedirs(PASTA_FOTOS)

# 🔑 COLE SUA API KEY DO IMGBB AQUI
API_KEY = "b5a8fe20c44ae277be2ccc46d50472ce"

st.set_page_config(page_title="Liga de IA UNIFESP - Cabine", layout="centered")

# ==============================
# ESTADO
# ==============================

if 'foto_final_url' not in st.session_state:
    st.session_state['foto_final_url'] = None

if 'nome_arquivo' not in st.session_state:
    st.session_state['nome_arquivo'] = None

if 'link_publico' not in st.session_state:
    st.session_state['link_publico'] = None

st.title("📸 Cabine de Fotos")

# ==============================
# UPLOAD
# ==============================

col1, col2 = st.columns(2)

with col1:
    arq_aluno = st.file_uploader("1. Foto do Aluno", type=['jpg', 'png', 'jpeg'])

with col2:
    arq_fundo = st.file_uploader("2. Moldura da Liga", type=['jpg', 'png', 'jpeg'])

# ==============================
# PROCESSAMENTO
# ==============================

if arq_aluno and arq_fundo:
    if st.button("🚀 PROCESSAR FOTO"):
        with st.spinner("Removendo fundo e aplicando estilo..."):
            img_aluno = Image.open(arq_aluno).convert("RGBA")
            img_fundo = Image.open(arq_fundo).convert("RGBA")

            # Remove fundo
            sem_fundo = remove(img_aluno)

            # Junta com moldura
            img_fundo = img_fundo.resize(sem_fundo.size)
            img_fundo.paste(sem_fundo, (0, 0), sem_fundo)

            # Nome único
            nome_foto = f"{uuid.uuid4().hex}.png"
            caminho_salvamento = os.path.join(PASTA_FOTOS, nome_foto)
            img_fundo.save(caminho_salvamento)

            st.session_state['foto_final_url'] = caminho_salvamento
            st.session_state['nome_arquivo'] = nome_foto

        # ==============================
        # UPLOAD PARA IMGBB
        # ==============================

        with st.spinner("Enviando imagem para gerar link público..."):

            try:
                with open(caminho_salvamento, "rb") as f:
                    img_base64 = base64.b64encode(f.read())

                response = requests.post(
                    "https://api.imgbb.com/1/upload",
                    data={
                        "key": API_KEY,
                        "image": img_base64
                    }
                )

                data = response.json()

                if response.status_code == 200:
                    link_publico = data["data"]["url"]
                    st.session_state['link_publico'] = link_publico
                else:
                    st.error("Erro ao enviar imagem para hospedagem.")
                    st.session_state['link_publico'] = None

            except Exception as e:
                st.error(f"Erro no upload: {e}")
                st.session_state['link_publico'] = None

# ==============================
# EXIBIÇÃO FINAL
# ==============================

if st.session_state['foto_final_url']:

    st.image(st.session_state['foto_final_url'], caption="Sua foto está pronta!")

    # QR CODE COM LINK REAL
    if st.session_state['link_publico']:

        qr = qrcode.make(st.session_state['link_publico'])
        buf = BytesIO()
        qr.save(buf, format="PNG")

        st.success("✅ Escaneie para baixar direto no seu celular:")
        st.image(buf.getvalue(), width=250)

    else:
        st.warning("⚠️ Não foi possível gerar link público.")

    # Download local
    with open(st.session_state['foto_final_url'], "rb") as file:
        st.download_button(
            label="💾 Baixar Foto no Computador",
            data=file,
            file_name="foto_liga_ia.png",
            mime="image/png"
        )

    # Reset
    if st.button("🔄 Novo Aluno"):
        st.session_state['foto_final_url'] = None
        st.session_state['nome_arquivo'] = None
        st.session_state['link_publico'] = None
        st.rerun()