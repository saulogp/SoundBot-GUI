import discord
import asyncio

class DiscordManager:
    def __init__(self, token, server_id):
        self.token = token
        self.server_id = server_id
        self.voice_channels = []
        self.voice_client = None

    async def connect_and_list_channels(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.voice_states = True

        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = discord.utils.get(client.guilds, id=self.server_id)
            if guild:
                print(f"Conectado ao servidor '{guild.name}'")
                self.voice_channels = [channel for channel in guild.voice_channels]
            await client.close()

        await client.start(self.token)

    def get_voice_channels(self):
        asyncio.run(self.connect_and_list_channels())
        return self.voice_channels

    async def connect_to_voice_channel(self, channel_id):
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            guild = discord.utils.get(client.guilds, id=self.server_id)
            voice_channel = discord.utils.get(guild.voice_channels, id=channel_id)

            if voice_channel:
                if self.voice_client and self.voice_client.is_connected():
                    await self.voice_client.disconnect()
                self.voice_client = await voice_channel.connect()
                print(f"Conectado ao canal de voz: {voice_channel.name}")

        await client.start(self.token)

    async def play_audio_channel(self, file_path):
        if self.voice_client and self.voice_client.is_connected():
            if not self.voice_client.is_playing():
                self.voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=file_path))
                print(f"Tocando áudio: {file_path}")
            else:
                print("Já está tocando um áudio.")
        else:
            print("O bot não está conectado a um canal de voz.")

    async def disconnect_from_voice(self):
        if self.voice_client and self.voice_client.is_connected():
            await self.voice_client.disconnect()
            print("Desconectado do canal de voz.")


