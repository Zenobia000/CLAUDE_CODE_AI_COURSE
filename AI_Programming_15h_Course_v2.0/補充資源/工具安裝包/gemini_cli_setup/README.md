# Google Gemini CLI 安裝與配置指南

> Google AI 命令列工具完整設定教學

---

## 📋 前置要求

### 系統要求
- **作業系統**: Windows 10/11, macOS, Linux
- **Python**: 3.8 或更高版本
- **Google 帳號**: 需要有效的 Google 帳號

### 檢查環境

```bash
# 檢查 Python 版本
python --version

# 或
python3 --version

# 檢查 pip 版本
pip --version
```

---

## 🔑 取得 API Key

### 申請步驟

1. **前往 Google AI Studio**
   - 訪問 [Google AI Studio](https://aistudio.google.com/)
   - 使用 Google 帳號登入

2. **建立 API Key**
   - 點擊左側選單的 **Get API key**
   - 選擇或建立新專案
   - 點擊 **Create API key**
   - 複製並安全保存 API Key

3. **啟用 Gemini API**（如需要）
   - 前往 [Google Cloud Console](https://console.cloud.google.com/)
   - 導航至 **APIs & Services > Library**
   - 搜尋 **Gemini API**
   - 點擊 **Enable**

---

## 🚀 安裝步驟

### 方法 1: 使用 pip（推薦）

```bash
# 安裝官方 Google GenerativeAI SDK
pip install google-generativeai

# 驗證安裝
python -c "import google.generativeai as genai; print(genai.__version__)"
```

### 方法 2: 使用 Poetry

```bash
# 在專案中使用 Poetry
poetry add google-generativeai

# 啟用虛擬環境
poetry shell
```

### 方法 3: 使用 pipx（隔離安裝）

```bash
# 安裝 pipx（如尚未安裝）
python -m pip install --user pipx
python -m pipx ensurepath

# 使用 pipx 安裝（全域可用但隔離）
pipx install google-generativeai
```

---

## 🔧 基本配置

### 設定 API Key

**方法 1: 環境變數（推薦）**

```bash
# Windows (PowerShell)
$env:GOOGLE_API_KEY="your-api-key-here"

# Windows (CMD)
set GOOGLE_API_KEY=your-api-key-here

# macOS/Linux (Bash)
export GOOGLE_API_KEY="your-api-key-here"

# 永久設定（加入到 .bashrc 或 .zshrc）
echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**方法 2: .env 檔案**

```bash
# 建立 .env 檔案
cat > .env << EOF
GOOGLE_API_KEY=your-api-key-here
EOF

# 確保 .env 在 .gitignore 中
echo ".env" >> .gitignore
```

**方法 3: Python 配置檔**

建立 `~/.gemini/config.json`:

```json
{
  "api_key": "your-api-key-here",
  "default_model": "gemini-pro",
  "temperature": 0.7,
  "max_tokens": 2048
}
```

---

## ✅ 驗證安裝

### 快速測試

建立測試腳本 `test_gemini.py`:

```python
#!/usr/bin/env python3
import os
import google.generativeai as genai

# 設定 API Key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in environment")
    exit(1)

genai.configure(api_key=api_key)

# 測試連線
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello, Gemini!")
    print("✅ Connection successful!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
```

執行測試:

```bash
python test_gemini.py
```

預期輸出：

```
✅ Connection successful!
Response: Hello! How can I help you today?
```

---

## 💡 基本使用範例

### 範例 1: 簡單對話

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# 生成回應
response = model.generate_content("Explain quantum computing in simple terms")
print(response.text)
```

### 範例 2: 程式碼生成

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

prompt = """
Generate a Python function that:
- Takes a list of numbers as input
- Returns the median value
- Handles edge cases (empty list, single element)
- Includes docstring and type hints
"""

response = model.generate_content(prompt)
print(response.text)
```

### 範例 3: 多輪對話

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# 開始對話
chat = model.start_chat(history=[])

# 第一輪
response1 = chat.send_message("What is FastAPI?")
print("User: What is FastAPI?")
print(f"Gemini: {response1.text}\n")

# 第二輪（有上下文）
response2 = chat.send_message("How do I install it?")
print("User: How do I install it?")
print(f"Gemini: {response2.text}\n")

# 查看對話歷史
print("Chat history:")
for message in chat.history:
    print(f"{message.role}: {message.parts[0].text[:100]}...")
```

### 範例 4: 圖片分析（gemini-pro-vision）

```python
import google.generativeai as genai
from PIL import Image
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro-vision')

# 載入圖片
image = Image.open('screenshot.png')

# 分析圖片
response = model.generate_content([
    "Describe what's in this image and identify any potential issues",
    image
])
print(response.text)
```

---

## 🛠️ 進階配置

### 自訂生成參數

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# 配置生成參數
generation_config = {
    "temperature": 0.9,           # 創意度 (0.0-1.0)
    "top_p": 1,                   # Nucleus sampling
    "top_k": 1,                   # Top-K sampling
    "max_output_tokens": 2048,    # 最大輸出長度
}

# 安全性設定
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name='gemini-pro',
    generation_config=generation_config,
    safety_settings=safety_settings
)

response = model.generate_content("Write a creative story")
print(response.text)
```

### 串流輸出（即時回應）

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# 使用串流模式
response = model.generate_content(
    "Write a detailed explanation of Docker containers",
    stream=True
)

# 即時顯示回應
for chunk in response:
    print(chunk.text, end='', flush=True)
```

### 錯誤處理與重試

```python
import google.generativeai as genai
import os
import time
from google.api_core import exceptions

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except exceptions.ResourceExhausted:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit hit, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
        except Exception as e:
            print(f"Error: {e}")
            raise

# 使用
result = generate_with_retry("Explain Python decorators")
print(result)
```

---

## 🎯 實用 CLI 工具腳本

### 建立互動式 CLI

建立 `gemini_cli.py`:

```python
#!/usr/bin/env python3
"""
Gemini CLI - Interactive command-line interface for Google Gemini
"""
import os
import sys
import argparse
import google.generativeai as genai
from pathlib import Path

def setup_api():
    """Configure Gemini API"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("Error: GOOGLE_API_KEY not set")
        sys.exit(1)
    genai.configure(api_key=api_key)

def chat_mode():
    """Interactive chat mode"""
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    print("Gemini Chat Mode (type 'exit' to quit)")
    print("-" * 50)

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            response = chat.send_message(user_input)
            print(f"\nGemini: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

def one_shot_mode(prompt):
    """Single prompt mode"""
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

def file_mode(file_path):
    """Process file content"""
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    content = path.read_text()
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Analyze the following code and provide:
    1. A brief summary
    2. Potential improvements
    3. Any security concerns

    Code:
    ```
    {content}
    ```
    """

    try:
        response = model.generate_content(prompt)
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Gemini CLI - Interactive AI assistant"
    )
    parser.add_argument(
        '-c', '--chat',
        action='store_true',
        help='Start interactive chat mode'
    )
    parser.add_argument(
        '-p', '--prompt',
        type=str,
        help='Single prompt (one-shot mode)'
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Analyze file content'
    )

    args = parser.parse_args()

    setup_api()

    if args.chat:
        chat_mode()
    elif args.prompt:
        one_shot_mode(args.prompt)
    elif args.file:
        file_mode(args.file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

### 使用 CLI 工具

```bash
# 賦予執行權限（Linux/macOS）
chmod +x gemini_cli.py

# 互動模式
./gemini_cli.py --chat

# 單次提問
./gemini_cli.py --prompt "Explain FastAPI routing"

# 分析檔案
./gemini_cli.py --file app.py
```

---

## 🐛 常見問題排解

### 問題 1: API Key 錯誤

**症狀**: `google.api_core.exceptions.PermissionDenied`

**解決方法**:
1. 確認 API Key 正確
2. 檢查 API Key 權限
3. 確認 Gemini API 已啟用

```bash
# 驗證環境變數
echo $GOOGLE_API_KEY  # Linux/macOS
echo %GOOGLE_API_KEY%  # Windows CMD
```

### 問題 2: 配額超限

**症狀**: `google.api_core.exceptions.ResourceExhausted: 429`

**解決方法**:
1. 實作速率限制
2. 使用指數退避重試
3. 檢查 [配額限制](https://ai.google.dev/pricing)

```python
import time
from google.api_core import retry

@retry.Retry(predicate=retry.if_exception_type(
    exceptions.ResourceExhausted
))
def generate_with_retry(prompt):
    return model.generate_content(prompt)
```

### 問題 3: 模型不存在

**症狀**: `ValueError: Invalid model name`

**解決方法**:
```python
# 列出可用模型
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
```

可用模型:
- `gemini-pro` - 文字生成
- `gemini-pro-vision` - 多模態（文字+圖片）

### 問題 4: 安全過濾器阻擋

**症狀**: `response.prompt_feedback.block_reason`

**解決方法**:
```python
# 檢查回應
if response.prompt_feedback.block_reason:
    print(f"Blocked: {response.prompt_feedback.block_reason}")
else:
    print(response.text)

# 調整安全設定（謹慎使用）
safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    }
]
```

---

## 📊 效能優化

### 批次處理

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

prompts = [
    "Explain Docker",
    "Explain Kubernetes",
    "Explain Microservices"
]

# 並發處理（使用 asyncio）
import asyncio

async def generate_async(prompt):
    response = model.generate_content(prompt)
    return response.text

async def batch_generate(prompts):
    tasks = [generate_async(p) for p in prompts]
    return await asyncio.gather(*tasks)

# 執行
results = asyncio.run(batch_generate(prompts))
for i, result in enumerate(results):
    print(f"\n=== Prompt {i+1} ===")
    print(result)
```

### 快取優化

```python
import functools
import hashlib

@functools.lru_cache(maxsize=128)
def cached_generate(prompt_hash):
    # 實際生成
    response = model.generate_content(prompt)
    return response.text

def generate_with_cache(prompt):
    # 生成提示詞的 hash
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    return cached_generate(prompt_hash)
```

---

## 🔐 安全性最佳實踐

### 1. API Key 保護

```python
# ❌ 錯誤做法
api_key = "AIzaSy..."  # 硬編碼在程式碼中

# ✅ 正確做法
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not set")
```

### 2. 輸入驗證

```python
def safe_generate(user_input):
    # 限制輸入長度
    if len(user_input) > 10000:
        raise ValueError("Input too long")

    # 過濾敏感關鍵字
    blocked_words = ['password', 'secret', 'api_key']
    if any(word in user_input.lower() for word in blocked_words):
        raise ValueError("Input contains sensitive information")

    return model.generate_content(user_input)
```

### 3. 輸出清理

```python
import re

def sanitize_output(text):
    # 移除潛在的敏感資訊
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                  '[EMAIL]', text)
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
    return text
```

---

## 📚 學習資源

### 官方資源
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API 文檔](https://ai.google.dev/docs)
- [Python SDK 參考](https://ai.google.dev/api/python)
- [定價與配額](https://ai.google.dev/pricing)

### 範例專案
- [Gemini Cookbook](https://github.com/google-gemini/cookbook)
- [官方範例庫](https://ai.google.dev/examples)

### 社群資源
- [Google AI Developers](https://developers.google.com/ai)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-gemini)

---

## 💰 定價與配額

### 免費額度（Gemini Pro）

| 項目 | 免費額度 |
|------|---------|
| **每分鐘請求數** | 60 requests/min |
| **每日請求數** | 1,500 requests/day |
| **Token 限制** | 32,760 tokens/request |

### 付費方案

查看最新定價: [https://ai.google.dev/pricing](https://ai.google.dev/pricing)

---

## 🔄 更新與維護

### 檢查更新

```bash
# 檢查當前版本
pip show google-generativeai

# 更新到最新版本
pip install --upgrade google-generativeai
```

### 解除安裝

```bash
# 解除安裝
pip uninstall google-generativeai

# 清除快取
rm -rf ~/.cache/google-generativeai
```

---

**安裝完成後，請參考課程 Module 2 開始學習如何整合 Gemini 到你的開發工作流程！** 🚀
