from typing import Optional
from telethon import TelegramClient, events
from telethon.tl.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    DocumentAttributeVideo,
    DocumentAttributeAudio,
    DocumentAttributeAnimated
)
from dotenv import load_dotenv
import os

load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")

# IDs dos grupos de origem (-100...)
GRUPOS: list[int] = [-1001951562774]  # Substitua pelos IDs reais
GRUPO_DESTINO = -1001795599457        # Substitua pelo ID real do grupo destino

class Config:
    SEND_TEXT = False  # Enviar texto das mensagens
    SEND_MEDIA = True
    SEND_CAPTION = False  # Enviar legenda das mídias
    NEW_MESSAGE: Optional[str] = None  # Mensagem padrão para novos textos, se SEND_TEXT for True

class EchoGroup(TelegramClient):
    def __init__(self, client_name: str = 'client', path: str = 'downloads_dir'):
        load_dotenv()
        self.path = path
        self.api_id = int(os.getenv("API_ID"))
        self.api_hash = os.getenv("API_HASH")
        self.phone_number = os.getenv("PHONE_NUMBER")
        self.grupos = GRUPOS
        self.grupo_destino = GRUPO_DESTINO
        os.makedirs(self.path, exist_ok=True)
        super().__init__(os.path.join(self.path, client_name), self.api_id, self.api_hash, timeout=60)

    async def start(self):
        await super().start(phone=self.phone_number)
        if not await self.is_user_authorized():
            await self.send_code_request(self.phone_number)
            code = input('Digite o código recebido: ')
            await self.sign_in(self.phone_number, code)
        if not self.grupos:
            print("Nenhum grupo monitorado. Adicione IDs à lista self.grupos.")
            return

        @self.on(events.NewMessage(chats=self.grupos))
        async def handler(event):
            if event.media and Config.SEND_MEDIA:
                if isinstance(event.media, (MessageMediaPhoto, DocumentAttributeVideo)):
                    print("Mídia recebida:", event.media ,"de", event.chat.title,end='\r')
                    if not Config.SEND_CAPTION and Config.NEW_MESSAGE is None:
                       return await self.forward_messages(
                            self.grupo_destino,
                            messages=event.message,
                            background=True,
                            drop_media_captions=True,
                            drop_author=True,
                            silent=True
                        )
                    else:
                        file_path = await self.download_media(event.media, file=event.media.file.name or None, folder=self.path)
                        await self.send_file(
                            self.grupo_destino,
                            file_path,
                            caption=event.message.message if Config.SEND_CAPTION else Config.NEW_MESSAGE,
                            background=True
                        )
                        os.remove(file_path)
                else:
                    print("Tipo de mídia não suportado.")
            elif event.text and Config.SEND_TEXT:
                await self.send_message(
                    self.grupo_destino,
                    Config.NEW_MESSAGE or event.text
                )

        print("Monitorando os grupos...")
        await self.run_until_disconnected()

    def run(self):
        with self:
            self.loop.run_until_complete(self.start())

# Exemplo de uso:
if __name__ == "__main__":
    bot = EchoGroup()
    bot.run()
