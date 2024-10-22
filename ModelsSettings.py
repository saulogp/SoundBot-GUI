import json
import os
import uuid


class Channel:
    def __init__(self, id="", display=""):
        self.id = int(id)
        self.display = display

class SoundProfile:
    def __init__(self, id=None, display="", file_name="", file_path="", img_path=""):
        self.id = str(uuid.uuid4())
        self.display = display
        self.file_name = file_name
        self.file_path = file_path
        self.img_path = img_path

    def to_dict(self):
        return {
            "id": self.id,
            "display": self.display,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "img_path": self.img_path
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância de SoundProfile a partir de um dicionário."""
        return SoundProfile(
            id=data.get("id"),
            display=data.get("display", ""),
            file_name=data.get("file_name", ""),
            file_path=data.get("file_path", ""),
            img_path=data.get("img_path", "")
        )

class SettingsManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.settings = self._load_settings()

    def _load_settings(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    content = file.read().strip()
                    if content:
                        return json.loads(content)
                    else:
                        return []
            except json.JSONDecodeError:
                print(f"Erro ao ler o arquivo {self.file_path}. O conteúdo não está no formato JSON correto.")
                return []
        else:
            return []

    def _save_settings(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def add_profile(self, profile):
        # Verifica se já existe um objeto com o mesmo id
        if any(item['id'] == profile.id for item in self.settings):
            print(f"Perfil com id {profile.id} já existe.")
        else:
            self.settings.append(profile.to_dict())
            self._save_settings()
            print(f"Perfil com id {profile.id} adicionado.")

    def remove_profile(self, profile_id):
        initial_count = len(self.settings)
        self.settings = [item for item in self.settings if item['id'] != profile_id]
        if len(self.settings) < initial_count:
            self._save_settings()
            print(f"Perfil com id {profile_id} removido.")
        else:
            print(f"Perfil com id {profile_id} não encontrado.")

    def list_profiles(self):
        return [SoundProfile.from_dict(item) for item in self.settings]