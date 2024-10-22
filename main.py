import asyncio
import flet as ft
import shutil
import os
from DiscordManager import DiscordManager
from ModelsSettings import (SettingsManager, SoundProfile, Channel)

def main(page: ft.Page):
    page.title = "SoundBotGUI"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    settings_file = 'settings.json'
    manager = SettingsManager(settings_file)

    server_id_field = ft.TextField(label="Id do Servidor", icon=ft.icons.CLOUD, width=400)
    token_field = ft.TextField(label="Token de acesso", icon=ft.icons.KEY, width=400)

    listchannels = []
    listDisplayChannels = []

    def fetch_channels(e):
        token = token_field.value
        server_id = int(server_id_field.value)

        global discord_manager
        discord_manager = DiscordManager(token, server_id)
        channels = discord_manager.get_voice_channels()

        listDisplayChannels.clear()
        listchannels.clear()
        for channel in channels:
            listchannels.append(Channel(channel.id, channel.name))
            listDisplayChannels.append(ft.dropdown.Option(channel.name))

        page.update()
    
    def upload_image(e, p: SoundProfile):
        print(f"long-press {p.display}")
        pass

    async def connect_to_channel(e):
        if discord_manager:
            for c in listchannels:
                if c.display == channels.value:
                    print(f"conectado {c.id} {c.display}")
                    await discord_manager.connect_to_voice_channel(c.id)
    
    channels = ft.Dropdown(
            width=400,
            options=listDisplayChannels,
            on_change=connect_to_channel,
            icon=ft.icons.VOICE_CHAT
        )
    
    async def play_audio(e, p: SoundProfile):
        print(f"click: {p.display}")
        if discord_manager:
            await discord_manager.play_audio_channel(p.file_path)

    async def disconnect(e):
        if discord_manager:
            await discord_manager.disconnect_from_voice()

    def upload_files(e):
        for f in e.files:
            copyFile = os.path.join(os.getcwd(),"uploads")
            os.makedirs(copyFile, exist_ok=True)
            shutil.copy(f.path, copyFile)
            
            display = f.name.split(".")[0]
            obj = SoundProfile(
                display=display,
                file_name=f.name,
                file_path=f"uploads/{f.name}",
                img_path="uploads/sound-img-default.jpg"
            )
            
            print(obj)
            manager.add_profile(obj)

        reload_profile_cards()

    def on_dialog_result(e: ft.FilePickerResultEvent):
        upload_files(e)

    def reload_profile_cards():
        profiles = manager.list_profiles()
        profile_cards.controls.clear()
        profile_cards.controls.extend(create_profile_cards(profiles).controls)
        page.update()  # Atualiza a interface

    def create_profile_cards(profiles):
        cardRowView = ft.Row(wrap=True, expand=True, scroll=True)
        for profile in profiles:
            cardRowView.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(profile.display, text_align=ft.TextAlign.CENTER),
                        ft.Image(src=profile.img_path, fit=ft.ImageFit.FIT_WIDTH, width=140, height=140)
                    ]),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.BLUE_50,
                    width=150,
                    height=150,
                    border_radius=10,
                    on_click=lambda e, p=profile: asyncio.run(play_audio(e,p)),
                    on_long_press=lambda e, p=profile: upload_image(e, p)
                )
            )
        return cardRowView

    profile_cards = create_profile_cards(manager.list_profiles())

    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)

    page.add(
        ft.Row(
            [server_id_field, token_field, ft.TextButton(text="Conectar", on_click=fetch_channels), ft.TextButton(text="Desconectar", on_click=disconnect)],
            alignment=ft.MainAxisAlignment.START
        ),
        ft.Row(
            [channels, ft.FilledButton(
                "Selecionar arquivo",
                icon=ft.icons.DRIVE_FOLDER_UPLOAD, 
                on_click=lambda _: file_picker.pick_files(
                    allow_multiple=True, 
                    file_type=ft.FilePickerFileType.AUDIO))],
            alignment=ft.MainAxisAlignment.START
        ),
        profile_cards
    )

    page.update()

ft.app(main, upload_dir="uploads")
