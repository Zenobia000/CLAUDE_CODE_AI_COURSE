"""
PR #1: 用戶認證功能
作者: Alice（初級工程師）
AI 工具: GitHub Copilot

功能描述:
實作用戶登入 API 端點，驗證用戶名和密碼。
"""

from fastapi import FastAPI, HTTPException
import hashlib

app = FastAPI()

# AI 生成的程式碼
@app.post("/api/v1/auth/login")
def login(username, password):
    # 查詢用戶
    query = f"SELECT * FROM users WHERE username = '{username}'"
    user = db.execute(query)

    # 驗證密碼
    if user and user[0]['password'] == password:
        # 生成 token
        token = hashlib.md5(f"{username}{password}".encode()).hexdigest()
        return {"token": token, "user": user[0]}

    return None


# Alice 的測試程式碼（也通過了）
def test_login():
    response = login("alice", "password123")
    assert response is not None
    assert "token" in response
    print("測試通過！")

if __name__ == "__main__":
    test_login()
