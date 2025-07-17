# echo_group_telegram

Um bot simples usando [Telethon](https://github.com/LonamiWebs/Telethon) para monitorar mensagens em um ou mais grupos do Telegram e encaminhá-las para outro grupo.

## 📦 Funcionalidades

- 🔁 Encaminha **mensagens de mídia** (imagens, vídeos, documentos).
- 📝 Pode opcionalmente encaminhar o **texto das mensagens**.
- ✏️ Permite definir uma **mensagem padrão personalizada** para substituir o conteúdo original.
- 📤 Permite ativar/desativar o envio de **legendas** junto com a mídia.

## ⚙️ Requisitos

- Python 3.8+
- Conta válida no Telegram
- API ID e API Hash obtidos via [my.telegram.org](https://my.telegram.org/)

## 🛠️ Instalação

1. Clone o repositório:

```bash
git clone https://github.com/danilofcosta/echo_group_telegram.git
cd echo_group_telegram
```
2. Instale as dependências:

```bash
pip install -r requirements.txt
```
3.Crie um arquivo .env com suas credenciais:
```
API_ID=123456
API_HASH=abc123def456...
PHONE_NUMBER=+5500000000000
```
4.Defina suas preferências em main.py
```
  SEND_TEXT = False          # Enviar mensagens de texto? (True/False)
  SEND_MEDIA = True          # Enviar mídias (fotos, vídeos, documentos)? (True/False)
  SEND_CAPTION = False       # Enviar legenda junto com a mídia? (True/False)
  NEW_MESSAGE = None         # Mensagem padrão para substituir textos ou legendas
  
  GRUPOS_ORIGEM = [-1001234567890,...] # lista de grupos 
  GRUPO_DESTINO = -1009876543210 # grupo destino

```
5.Execute o bot com:
```bash
python nome_do_arquivo.py

