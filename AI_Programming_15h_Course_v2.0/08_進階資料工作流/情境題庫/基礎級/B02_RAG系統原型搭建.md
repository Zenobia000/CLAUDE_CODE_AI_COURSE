# B02: RAG 系統原型搭建 - 10 分鐘建立智能問答系統

## 📋 情境描述

**你的困擾**：
```
團隊技術文檔散落各處：
- README 在 GitHub
- API 文檔在 Confluence
- 內部規範在 Google Docs
- 部署指南在 Notion

新人入職經常問：
- "XX 服務怎麼部署？"
- "這個 API 怎麼用？"
- "錯誤碼 500 是什麼意思？"

你總是回答相同的問題，浪費大量時間。
```

**你想要的**：
```
一個智能問答系統：
- 輸入問題 → 自動找到答案
- 附上來源文檔連結
- 10 分鐘快速搭建原型
```

---

## 🎯 學習目標

完成本題後，你將能夠：
- [ ] 理解 RAG（檢索增強生成）的基本原理
- [ ] 10 分鐘搭建可運行的 RAG 原型
- [ ] 知道如何調整檢索策略提升準確度
- [ ] 理解常見 RAG 工具的選擇邏輯

**時間**：45-60 分鐘

---

## 🏗️ RAG 系統架構速覽

### 什麼是 RAG？

```
傳統 LLM 的問題：
Q: "我們公司的部署流程是什麼？"
A: "我不知道你們公司的具體流程..." ❌

RAG 系統的解決方案：
Q: "我們公司的部署流程是什麼？"
   ↓
1. 檢索：在公司文檔中搜尋相關內容
2. 增強：把找到的內容加入提示詞
3. 生成：LLM 基於文檔回答問題
   ↓
A: "根據部署指南文檔，流程是..." ✅
   來源：docs/deployment.md
```

### RAG 系統的核心組件

```
┌─────────────┐
│ 文檔         │ → 切塊 → 嵌入 → ┌─────────────┐
│ (MD/PDF/TXT)│                │ 向量資料庫   │
└─────────────┘                │ (Chroma)    │
                               └─────────────┘
                                      ↓ 檢索
                               ┌─────────────┐
用戶問題 → 嵌入 → 相似度檢索 → │ 相關文檔片段 │
                               └─────────────┘
                                      ↓
                               ┌─────────────┐
                               │ LLM 生成回答 │
                               │ (GPT-4等)   │
                               └─────────────┘
                                      ↓
                                 答案 + 來源
```

---

## 📝 任務階段

### 階段 1：環境準備（5 分鐘）

**任務 1.1**：安裝依賴

```bash
# 創建專案目錄
mkdir rag-prototype
cd rag-prototype

# 安裝核心套件
pip install langchain chromadb openai python-dotenv
```

**任務 1.2**：設定 API Key

創建 `.env` 檔案：
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

**任務 1.3**：準備測試文檔

創建 `docs/` 目錄，放入 5-10 個 Markdown 文檔：
```bash
mkdir docs

# 範例：創建測試文檔
cat > docs/deployment.md << 'EOF'
# 部署指南

## 環境要求
- Python 3.9+
- Docker 20.10+
- Kubernetes 1.24+

## 部署步驟
1. 建置 Docker image
2. 推送到 registry
3. 更新 k8s manifest
4. 執行 kubectl apply

## 常見問題
- 如果遇到權限錯誤，檢查 service account
- 如果 pod 無法啟動，檢查 image pull secrets
EOF
```

---

### 階段 2：搭建最小原型（10 分鐘）

**任務 2.1**：載入文檔

創建 `rag_simple.py`：
```python
import os
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# 載入環境變數
load_dotenv()

# Step 1: 載入文檔
print("正在載入文檔...")
loader = DirectoryLoader('docs/', glob="**/*.md")
documents = loader.load()
print(f"載入了 {len(documents)} 個文檔")

# Step 2: 切分文檔
print("正在切分文檔...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # 每塊 1000 字元
    chunk_overlap=200  # 重疊 200 字元（避免截斷）
)
chunks = text_splitter.split_documents(documents)
print(f"切分為 {len(chunks)} 個片段")

# Step 3: 建立向量資料庫
print("正在建立向量資料庫...")
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"  # 持久化儲存
)

# Step 4: 建立 QA 鏈
print("正在建立 QA 系統...")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # 最簡單的策略：把所有檢索到的內容塞入提示詞
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),  # 檢索 top 3
    return_source_documents=True  # 返回來源文檔
)

print("✅ RAG 系統已就緒！")

# Step 5: 測試問答
def ask(question):
    print(f"\n問題：{question}")
    result = qa_chain({"query": question})
    print(f"答案：{result['result']}")
    print(f"\n來源：")
    for doc in result['source_documents']:
        print(f"  - {doc.metadata['source']}")

# 互動式問答
if __name__ == "__main__":
    while True:
        question = input("\n請輸入問題（輸入 'quit' 結束）：")
        if question.lower() == 'quit':
            break
        ask(question)
```

**任務 2.2**：執行測試

```bash
python rag_simple.py
```

**預期輸出**：
```
正在載入文檔...
載入了 10 個文檔
正在切分文檔...
切分為 45 個片段
正在建立向量資料庫...
正在建立 QA 系統...
✅ RAG 系統已就緒！

請輸入問題：我們的部署流程是什麼？

問題：我們的部署流程是什麼？
答案：根據部署指南文檔，部署流程如下：
1. 建置 Docker image
2. 推送到 registry
3. 更新 k8s manifest
4. 執行 kubectl apply

來源：
  - docs/deployment.md
```

---

### 階段 3：測試與驗證（10 分鐘）

**任務 3.1**：測試多種問題

準備測試問題清單：
```python
test_questions = [
    "部署需要哪些環境？",
    "如果 pod 無法啟動怎麼辦？",
    "API 認證怎麼做？",
    "資料庫連線字串在哪裡設定？",
    "怎麼回滾到上一個版本？"
]

for q in test_questions:
    ask(q)
    print("\n" + "="*50)
```

**任務 3.2**：評估回答品質

檢查以下指標：
- [ ] 答案是否準確？
- [ ] 來源文檔是否相關？
- [ ] 是否有遺漏重要信息？
- [ ] 回答是否自然流暢？

**問題記錄範本**：
```
問題 1：部署需要哪些環境？
答案：✅ 正確 / ❌ 錯誤 / ⚠️ 部分正確
來源：✅ 相關 / ❌ 不相關
備註：___________
```

---

### 階段 4：優化檢索策略（15 分鐘）

**問題**：如果回答不準確怎麼辦？

**優化策略 A：調整 chunk size**

```python
# 原本：chunk_size=1000
# 問題：太大 → 包含太多無關信息
#      太小 → 可能截斷重要上下文

# 實驗不同大小
for size in [500, 1000, 1500]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=200
    )
    # 測試並記錄結果
```

**優化策略 B：調整檢索數量**

```python
# 原本：k=3 （檢索 top 3）
# 調整：k=5 （檢索 top 5）

retriever = vectorstore.as_retriever(
    search_type="similarity",  # 或 "mmr" (最大邊際相關性)
    search_kwargs={"k": 5}
)
```

**優化策略 C：使用 MMR 檢索**

```python
# MMR (Maximal Marginal Relevance)：
# 不只看相似度，還確保多樣性

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,  # 先取 20 個候選
        "lambda_mult": 0.7  # 平衡相似度和多樣性
    }
)
```

**任務 4.1**：實驗優化效果

創建 `optimize_rag.py`：
```python
from rag_simple import ask

# 測試問題
test_question = "如果 pod 無法啟動怎麼辦？"

# 配置 1: 小 chunk + k=3
print("=== 配置 1: chunk_size=500, k=3 ===")
# 測試...

# 配置 2: 中 chunk + k=5
print("=== 配置 2: chunk_size=1000, k=5 ===")
# 測試...

# 配置 3: MMR 檢索
print("=== 配置 3: MMR retrieval ===")
# 測試...

# 記錄哪個配置效果最好
```

---

### 階段 5：加入來源追蹤（10 分鐘）

**任務 5.1**：顯示詳細來源信息

優化 `ask()` 函數：
```python
def ask_with_sources(question):
    print(f"\n問題：{question}")
    result = qa_chain({"query": question})

    print(f"\n答案：{result['result']}")

    print(f"\n📚 來源文檔：")
    for i, doc in enumerate(result['source_documents'], 1):
        print(f"\n[來源 {i}] {doc.metadata['source']}")
        print(f"相關片段：")
        print(f"{doc.page_content[:200]}...")  # 顯示前 200 字元
        print(f"──────────────────────────")
```

**任務 5.2**：加入信心度評分（可選）

```python
# 基於檢索的相似度分數評估信心度
def ask_with_confidence(question):
    # 手動檢索以取得分數
    docs_with_scores = vectorstore.similarity_search_with_score(question, k=3)

    print(f"\n檢索結果信心度：")
    for doc, score in docs_with_scores:
        confidence = f"{(1 - score) * 100:.1f}%"  # 轉換為百分比
        print(f"  {confidence} - {doc.metadata['source']}")

    # 然後正常問答
    result = qa_chain({"query": question})
    print(f"\n答案：{result['result']}")
```

---

## ✅ 檢查點

### 檢查點 1：原型可運行

- [ ] 成功安裝所有依賴
- [ ] 成功載入文檔並建立向量資料庫
- [ ] 可以問問題並得到回答
- [ ] 回答附有來源文檔

### 檢查點 2：理解核心概念

- [ ] 理解 RAG 的三個步驟（檢索-增強-生成）
- [ ] 知道什麼是向量嵌入（embedding）
- [ ] 理解 chunk size 的影響
- [ ] 知道如何調整檢索參數

### 檢查點 3：能獨立優化

- [ ] 能根據回答品質調整 chunk size
- [ ] 能選擇合適的檢索策略（similarity vs MMR）
- [ ] 能評估不同配置的效果
- [ ] 知道何時需要更複雜的方案

---

## 💡 常見問題與解決

### Q1：回答經常說"我不知道"

**原因**：
- 文檔沒有相關信息
- 檢索沒有找到相關片段
- chunk size 太小，上下文不完整

**解決**：
```python
# 1. 檢查檢索結果
docs = vectorstore.similarity_search(question, k=5)
for doc in docs:
    print(doc.page_content)  # 看看檢索到什麼

# 2. 調整 chunk size
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # 增大 chunk
    chunk_overlap=300
)

# 3. 增加檢索數量
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
```

---

### Q2：回答包含錯誤信息

**原因**：
- 檢索到不相關的文檔
- LLM 產生幻覺（hallucination）

**解決**：
```python
# 使用更嚴格的提示詞
from langchain.prompts import PromptTemplate

template = """
請僅根據以下文檔回答問題。
如果文檔中沒有相關信息，請明確說"文檔中沒有相關信息"。
不要自行推測或添加文檔之外的信息。

文檔：
{context}

問題：{question}

答案：
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)
```

---

### Q3：處理速度很慢

**原因**：
- 文檔太多
- 嵌入計算慢
- 向量資料庫未持久化

**解決**：
```python
# 1. 持久化向量資料庫（避免重複嵌入）
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# 2. 使用更快的 embedding 模型
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. 限制檢索數量
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

---

### Q4：如何支援多種文檔格式？

**解決**：
```python
# 安裝額外 loader
pip install pypdf docx2txt

# 載入不同格式
from langchain.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)

# 自動識別格式
loaders = [
    DirectoryLoader('docs/', glob="**/*.md", loader_cls=TextLoader),
    DirectoryLoader('docs/', glob="**/*.pdf", loader_cls=PyPDFLoader),
    DirectoryLoader('docs/', glob="**/*.docx", loader_cls=Docx2txtLoader),
]

all_docs = []
for loader in loaders:
    all_docs.extend(loader.load())
```

---

## 🎯 擴展挑戰

### 挑戰 1：加入 CLI 介面

讓系統更易用：
```bash
python rag_cli.py ask "部署流程是什麼？"
python rag_cli.py search "部署"
python rag_cli.py add-docs ./new_docs/
```

### 挑戰 2：建立 Web 介面

使用 Streamlit：
```python
import streamlit as st

st.title("企業文檔問答系統")
question = st.text_input("請輸入問題：")

if question:
    result = qa_chain({"query": question})
    st.write(result['result'])

    st.subheader("來源文檔：")
    for doc in result['source_documents']:
        st.write(f"- {doc.metadata['source']}")
```

### 挑戰 3：多語言支援

支援中英文混合文檔：
```python
# 使用多語言 embedding 模型
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
```

### 挑戰 4：增加對話記憶

讓系統記住對話歷史：
```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

# 現在可以進行多輪對話
qa_chain({"question": "部署流程是什麼？"})
qa_chain({"question": "那需要哪些環境？"})  # 理解"那"指的是部署
```

---

## 📚 延伸學習

### 推薦閱讀

- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Chroma Documentation](https://docs.trychroma.com/)
- [Vector Database Comparison](https://github.com/erikbern/ann-benchmarks)

### 工具選擇

```
場景                           推薦工具
─────────────────────────────────────────────
快速原型（本地）                Chroma
生產環境（雲端）                Pinecone, Weaviate
大規模（百萬文檔+）             Qdrant, Milvus
企業私有部署                    Weaviate (self-hosted)
```

### 進階主題

- **Hybrid Search**：結合關鍵字搜尋和向量搜尋
- **Re-ranking**：對檢索結果重新排序
- **Query Expansion**：擴展用戶問題以提升召回率
- **Multi-hop Reasoning**：多步推理

---

## 🎓 總結

完成本題後，你應該：

**理解的概念**：
- ✅ RAG 系統的基本架構（檢索-增強-生成）
- ✅ 向量嵌入和相似度檢索的原理
- ✅ chunk size 和檢索策略的影響

**掌握的技能**：
- ✅ 10 分鐘搭建 RAG 原型
- ✅ 調整參數優化回答品質
- ✅ 評估不同配置的效果

**建立的認知**：
- ✅ RAG 適用於企業內部文檔問答
- ✅ 原型搭建很快，但優化需要時間
- ✅ 工具選擇取決於使用場景（本地 vs 雲端）

---

**下一步**：
- 繼續 B03：自動化分析報告生成
- 或挑戰組合級 C02：企業文檔問答系統（完整版）

**記住**：
> RAG 不是魔法，是工具。
> 原型很快，優化需要耐心。
> 從簡單開始，逐步優化。
