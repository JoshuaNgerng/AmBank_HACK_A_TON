from pathlib import Path

class FileManagement:
    """
    ideally be a s3 file storage
    but s3 expensive is it will keep the file directory + file name as file key
    and save it to a local storage 
    which is the shared volume between fastapi and celery
    """
    file_root = Path.cwd() / 'storage'

    def upload_file(self, file_bytes: bytes, filename: str | None, dir: str | None = None) -> str:
        file_key = self.file_root
        if dir: file_key = file_key / dir
        file_key.mkdir(exist_ok=True)
        if not filename: filename = 'unknown_file'
        file_key = file_key / filename
        with open(file_key, 'wb') as f:
            f.write(file_bytes)
        return str(file_key)

    def download_file(self, file_key: str | Path) -> bytes | None:
        file_key = Path(file_key)
        if not file_key.exists(): return None
        with open(file_key, 'rb') as f:
            data = f.read()
        return data

file_manager = FileManagement()