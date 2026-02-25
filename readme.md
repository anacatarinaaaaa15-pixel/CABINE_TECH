# 📸 Cabine de Fotos - LigaDis UNIFESP

Aplicação web desenvolvida em **Streamlit** para gerar fotos personalizadas com:

- ✅ Remoção automática de fundo
- ✅ Aplicação de moldura da Liga
- ✅ Geração de QR Code
- ✅ Download direto da imagem
- ✅ Link público para acesso via celular (4G)

---

## 🚀 Tecnologias Utilizadas

- Python 3.x  
- Streamlit  
- Rembg (remoção de fundo com IA)  
- Pillow  
- QRCode  
- Requests  
- IMGBB API (hospedagem pública da imagem)

---

## 📦 Como Clonar o Projeto

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

---

## 🛠 Como Instalar as Dependências

Recomendado usar ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

Para desativar o ambiente virtual:
```bash
deactivate
```

Instale as bibliotecas:

```bash
pip install -r requirements.txt
```

Ou manualmente:

```bash
pip install streamlit rembg pillow qrcode requests onnxruntime
```

---

## 🔑 Configurar API Key

No arquivo `cabine.py`, coloque sua chave da API do IMGBB:

```python
API_KEY = "SUA_CHAVE_AQUI"
```

Você pode criar gratuitamente em:
https://api.imgbb.com/

---

## ▶️ Como Rodar o Projeto

Dentro da pasta do projeto:

```bash
streamlit run app.py
```

Se der erro de reconhecimento:

```bash
python -m streamlit run app.py
```

O navegador abrirá automaticamente em:

```
http://localhost:8501
```

---

## 📱 Acesso pelo Celular

Após gerar a foto:

- Um QR Code será exibido
- O QR aponta para um link público da imagem
- Funciona em 4G ou qualquer rede

---

## 🔄 Fluxo de Funcionamento

1. Upload da foto do aluno  
2. Upload da moldura  
3. Remoção automática do fundo  
4. Aplicação da moldura  
5. Upload automático para hospedagem pública  
6. Geração de QR Code  
7. Download disponível  

---

## 📂 Estrutura do Projeto

```
📦 cabine-fotos
 ┣ 📂 static
 ┣ 📜 cabine.py
 ┣ 📜 requirements.txt
 ┗ 📜 README.md
```

---

## 👨‍💻 Autor

Projeto desenvolvido com 💚 por Ana Catarina - Esther Tozzo.
