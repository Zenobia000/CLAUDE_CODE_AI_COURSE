# 資料工作流程工具速查

## 📋 工具對比總覽

### 資料處理工具

```
工具        資料量      速度    記憶體    學習曲線    推薦場景
─────────────────────────────────────────────────────────────────
Pandas     < 1GB      ⭐⭐⭐   高       低          日常分析
Polars     1-10GB     ⭐⭐⭐⭐⭐ 低       低          大檔處理
Dask       > 10GB     ⭐⭐⭐⭐  中       中          平行運算
Spark      > 100GB    ⭐⭐⭐⭐  低       高          大數據
```

---

### ETL 工具

```
工具          適用規模      學習曲線    成本    推薦
───────────────────────────────────────────────────
Python腳本    小型          低          免費    ⭐⭐⭐⭐⭐
Airflow       中大型        中          免費    ⭐⭐⭐⭐
Prefect       中大型        中          免費/付費 ⭐⭐⭐⭐
dbt           資料倉儲      中          免費    ⭐⭐⭐
Talend        企業級        高          付費    ⭐⭐
```

---

### RAG 框架

```
框架          成熟度    文檔    生態    推薦
───────────────────────────────────────────
LangChain    ⭐⭐⭐⭐⭐  ⭐⭐⭐⭐⭐ ⭐⭐⭐⭐⭐ 首選
LlamaIndex   ⭐⭐⭐⭐   ⭐⭐⭐⭐  ⭐⭐⭐⭐  資料整合
Haystack     ⭐⭐⭐     ⭐⭐⭐   ⭐⭐⭐   企業應用
```

---

### 向量資料庫

```
資料庫      類型    成本    效能    推薦場景
──────────────────────────────────────────────
Chroma     本地    免費    ⭐⭐⭐   開發測試
Pinecone   雲端    付費    ⭐⭐⭐⭐⭐ 生產環境
Weaviate   自架    免費    ⭐⭐⭐⭐  企業自建
Qdrant     自架    免費    ⭐⭐⭐⭐⭐ 高效能
Milvus     自架    免費    ⭐⭐⭐⭐⭐ 超大規模
```

---

## 🎯 工具選擇決策樹

### 資料處理工具選擇

```
資料量？
├─ < 1GB → Pandas ✅
├─ 1-10GB → Polars ✅
├─ 10-100GB → Dask ✅
└─ > 100GB → Spark 或找資料工程師 👨‍💻
```

### ETL 工具選擇

```
複雜度？
├─ 單一來源、簡單轉換 → Python 腳本 ✅
├─ 多來源、複雜流程 → Airflow/Prefect ✅
└─ 企業級、需要圖形化介面 → Talend/Informatica 💰
```

### RAG 工具選擇

```
需求？
├─ 快速原型 → LangChain + Chroma ✅
├─ 複雜資料整合 → LlamaIndex ✅
└─ 企業級應用 → Haystack + Weaviate ✅
```

---

## 📊 快速參考表

### Pandas 常用操作

```python
# 讀取
df = pd.read_csv('file.csv')
df = pd.read_excel('file.xlsx')
df = pd.read_sql('SELECT * FROM table', engine)

# 清洗
df.dropna()                          # 刪除空值
df.fillna(value)                     # 填充空值
df.drop_duplicates()                 # 刪除重複
df['col'] = df['col'].str.strip()   # 清理字串

# 轉換
df['date'] = pd.to_datetime(df['date'])
df.groupby('col').agg({'amount': 'sum'})

# 輸出
df.to_csv('output.csv', index=False)
df.to_sql('table', engine, if_exists='append')
```

### LangChain RAG 快速設置

```python
from langchain import ...

# 載入文檔
loader = DirectoryLoader("docs")
documents = loader.load()

# 切塊
splitter = CharacterTextSplitter(chunk_size=1000)
chunks = splitter.split_documents(documents)

# 向量化
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# QA
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    retriever=vectorstore.as_retriever()
)

answer = qa.run("你的問題")
```

---

## 🔗 官方文檔連結

### 資料處理
- [Pandas](https://pandas.pydata.org/docs/)
- [Polars](https://pola-rs.github.io/polars/)
- [Dask](https://docs.dask.org/)

### ETL
- [Apache Airflow](https://airflow.apache.org/docs/)
- [Prefect](https://docs.prefect.io/)
- [dbt](https://docs.getdbt.com/)

### RAG
- [LangChain](https://python.langchain.com/docs/)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [Chroma](https://docs.trychroma.com/)

---

**版本**：v1.0
**最後更新**：2025-10-30
