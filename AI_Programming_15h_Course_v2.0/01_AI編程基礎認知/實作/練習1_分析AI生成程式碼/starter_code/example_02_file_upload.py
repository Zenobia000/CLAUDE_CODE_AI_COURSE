"""
PR #2: 檔案上傳功能
作者: Bob（初級工程師）
AI 工具: Claude Code

功能描述:
允許用戶上傳專案附件（圖片、文檔等）。
"""

from fastapi import FastAPI, UploadFile
import os

app = FastAPI()

# AI 生成的程式碼
@app.post("/api/v1/projects/{project_id}/attachments")
def upload_file(project_id, file: UploadFile):
    # 儲存檔案
    upload_dir = "/var/www/uploads"
    filename = file.filename
    file_path = f"{upload_dir}/{filename}"

    # 寫入檔案
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # 返回檔案 URL
    return {
        "url": f"/files/{filename}",
        "size": os.path.getsize(file_path)
    }


# 下載端點
@app.get("/files/{filename}")
def download_file(filename):
    file_path = f"/var/www/uploads/{filename}"
    return open(file_path, "rb").read()
