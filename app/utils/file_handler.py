import zipfile
import os

async def process_file(file):
    file_location = f"tests/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    if file.filename.endswith(".zip"):
        with zipfile.ZipFile(file_location, 'r') as zip_ref:
            zip_ref.extractall("tests/")
        return f"Extracted {file.filename}"

    return f"Uploaded {file.filename}"
