# 10 分鐘搭建 RAG 系統

## 🎯 目標

在 10 分鐘內從零開始搭建一個可運行的 RAG（檢索增強生成）系統。

---

## ⏱️ 時間分配

```
分鐘 1-3：環境設置與依賴安裝
分鐘 4-5：文檔準備與載入
分鐘 6-7：建立向量資料庫
分鐘 8-9：實現問答功能
分鐘 10：測試與驗證
```

---

## 🚀 快速開始

### 步驟 1：安裝依賴（3 分鐘）

```bash
# 建立虛擬環境（可選，但推薦）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝必要套件
pip install langchain openai chromadb tiktoken
```

---

### 步驟 2：準備文檔（2 分鐘）

**建立測試文檔**：
```bash
mkdir docs
echo "Claude Code 是 Anthropic 推出的 AI 編程助手。" > docs/intro.txt
echo "RAG 系統結合了檢索與生成，可以回答基於文檔的問題。" > docs/rag.txt
```

---

### 步驟 3：最小可行代碼（5 分鐘）

**`rag_quick.py`**：
```python
import os
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# 設定 API Key
os.environ["OPENAI_API_KEY"] = "你的 API Key"

# 1. 載入文檔
loader = DirectoryLoader("docs", glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()
print(f"✅ 載入 {len(documents)} 個文檔")

# 2. 切塊
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
chunks = splitter.split_documents(documents)
print(f"✅ 切成 {len(chunks)} 個塊")

# 3. 建立向量資料庫
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)
print(f"✅ 向量資料庫建立完成")

# 4. 建立 QA 鏈
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=vectorstore.as_retriever()
)
print(f"✅ RAG 系統就緒\n")

# 5. 測試問答
questions = [
    "什麼是 Claude Code？",
    "RAG 系統的特點是什麼？"
]

for q in questions:
    print(f"Q: {q}")
    answer = qa.run(q)
    print(f"A: {answer}\n")
```

---

### 步驟 4：執行測試（分鐘）

```bash
python rag_quick.py
```

**預期輸出**：
```
✅ 載入 2 個文檔
✅ 切成 2 個塊
✅ 向量資料庫建立完成
✅ RAG 系統就緒

Q: 什麼是 Claude Code？
A: Claude Code 是 Anthropic 推出的 AI 編程助手。

Q: RAG 系統的特點是什麼？
A: RAG 系統結合了檢索與生成，可以回答基於文檔的問題。
```

---

## 🎓 恭喜！

你成功在 10 分鐘內搭建了第一個 RAG 系統！

---

## 📈 下一步

### 擴展功能

1. **加入更多文檔**：放入 PDF、Markdown 等
2. **持久化資料庫**：加入 `persist_directory` 參數
3. **優化切塊策略**：調整 `chunk_size` 和 `chunk_overlap`
4. **改善提示詞**：客製化 prompt template
5. **建立 Web 介面**：使用 Streamlit 或 Flask

---

**版本**：v1.0
**最後更新**：2025-10-30
