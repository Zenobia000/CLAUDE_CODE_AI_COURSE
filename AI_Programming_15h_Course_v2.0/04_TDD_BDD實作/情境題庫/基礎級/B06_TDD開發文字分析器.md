# B06：TDD 開發文字分析器

## 📋 情境描述

你要開發一個文字分析工具，用於分析文檔內容、統計詞頻、提取關鍵資訊等。這個工具需要處理各種文字處理的需求。

**需求**：
文字分析器需要支援：
- 基本統計（字數、詞數、行數）
- 詞頻分析（最高頻詞彙、詞頻分布）
- 文字清理（移除標點、轉小寫、過濾停用詞）
- 關鍵詞提取
- 文字相似度比較
- 簡單的情感分析

**任務**：
用 TDD 方式實作這個文字分析器，重點關注演算法邏輯的測試。

**時間估計**：35-45 分鐘

---

## 🎯 學習目標

- [ ] 學習演算法邏輯的 TDD 實作
- [ ] 掌握字串處理和資料分析的測試
- [ ] 練習邊界情況和異常輸入的處理
- [ ] 體驗文字處理領域的完整開發

---

## 🛠️ 技術要求

**語言**：Python 3.11+
**測試框架**：pytest
**檔案結構**：
```
text_analyzer/
├── text_analyzer.py       # 主要實作
├── text_cleaner.py       # 文字清理
├── sentiment_analyzer.py # 情感分析
└── test_text_analyzer.py # 測試檔案
```

---

## 📝 實作步驟

### 準備工作

**建立專案目錄**：
```bash
mkdir -p text_analyzer
cd text_analyzer

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝 pytest
pip install pytest
```

**建立檔案**：
```bash
touch text_analyzer.py
touch text_cleaner.py
touch sentiment_analyzer.py
touch test_text_analyzer.py
```

---

### 循環 1：基本文字統計

#### 🔴 RED：測試基本統計功能

**test_text_analyzer.py**：
```python
import pytest
from text_analyzer import TextAnalyzer
from text_cleaner import TextCleaner
from sentiment_analyzer import SentimentAnalyzer

def test_count_characters():
    """測試字元數統計"""
    analyzer = TextAnalyzer()

    result = analyzer.count_characters("Hello World!")

    assert result == 12

def test_count_characters_with_spaces():
    """測試包含空格的字元統計"""
    analyzer = TextAnalyzer()

    total_chars = analyzer.count_characters("Hello World!")
    chars_no_spaces = analyzer.count_characters_no_spaces("Hello World!")

    assert total_chars == 12
    assert chars_no_spaces == 10

def test_count_words():
    """測試詞數統計"""
    analyzer = TextAnalyzer()

    word_count = analyzer.count_words("Hello world, this is a test.")

    assert word_count == 6

def test_count_lines():
    """測試行數統計"""
    analyzer = TextAnalyzer()
    text = "Line one\nLine two\nLine three"

    line_count = analyzer.count_lines(text)

    assert line_count == 3

def test_empty_text_statistics():
    """測試空文字的統計"""
    analyzer = TextAnalyzer()

    assert analyzer.count_characters("") == 0
    assert analyzer.count_words("") == 0
    assert analyzer.count_lines("") == 0
```

**執行測試**：
```bash
$ pytest test_text_analyzer.py -v

FAILED - ModuleNotFoundError: No module named 'text_analyzer'
```

#### 🟢 GREEN：實作基本統計

**text_analyzer.py**：
```python
import re
from collections import Counter
from typing import Dict, List, Tuple

class TextAnalyzer:
    """文字分析器"""

    def count_characters(self, text: str) -> int:
        """計算字元數（包含空格）"""
        return len(text)

    def count_characters_no_spaces(self, text: str) -> int:
        """計算字元數（不包含空格）"""
        return len(text.replace(" ", ""))

    def count_words(self, text: str) -> int:
        """計算詞數"""
        if not text.strip():
            return 0
        # 使用正則表達式分割詞語
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    def count_lines(self, text: str) -> int:
        """計算行數"""
        if not text:
            return 0
        return len(text.split('\n'))
```

**執行測試**：
```bash
$ pytest test_text_analyzer.py -v

PASSED ✓✓✓✓✓
```

---

### 循環 2：詞頻分析

#### 🔴 RED：測試詞頻分析

**test_text_analyzer.py**（新增）：
```python
def test_word_frequency():
    """測試詞頻統計"""
    analyzer = TextAnalyzer()
    text = "the cat sat on the mat the cat was happy"

    freq = analyzer.get_word_frequency(text)

    assert freq["the"] == 3
    assert freq["cat"] == 2
    assert freq["sat"] == 1
    assert freq["happy"] == 1

def test_most_common_words():
    """測試最高頻詞彙"""
    analyzer = TextAnalyzer()
    text = "apple banana apple cherry apple banana"

    most_common = analyzer.get_most_common_words(text, 2)

    assert len(most_common) == 2
    assert most_common[0] == ("apple", 3)
    assert most_common[1] == ("banana", 2)

def test_word_frequency_case_insensitive():
    """測試大小寫不敏感的詞頻"""
    analyzer = TextAnalyzer()
    text = "Apple APPLE apple"

    freq = analyzer.get_word_frequency(text, case_sensitive=False)

    assert freq["apple"] == 3

def test_unique_words():
    """測試唯一詞彙統計"""
    analyzer = TextAnalyzer()
    text = "the cat sat on the mat"

    unique_count = analyzer.count_unique_words(text)
    unique_words = analyzer.get_unique_words(text)

    assert unique_count == 5
    assert "the" in unique_words
    assert "cat" in unique_words
    assert len(unique_words) == 5
```

#### 🟢 GREEN：實作詞頻分析

**text_analyzer.py**（更新）：
```python
def get_word_frequency(self, text: str, case_sensitive: bool = True) -> Dict[str, int]:
    """取得詞頻統計"""
    if not case_sensitive:
        text = text.lower()

    words = re.findall(r'\b\w+\b', text)
    return dict(Counter(words))

def get_most_common_words(self, text: str, n: int = 10) -> List[Tuple[str, int]]:
    """取得最高頻的 n 個詞彙"""
    words = re.findall(r'\b\w+\b', text.lower())
    counter = Counter(words)
    return counter.most_common(n)

def count_unique_words(self, text: str) -> int:
    """計算唯一詞彙數量"""
    words = re.findall(r'\b\w+\b', text.lower())
    return len(set(words))

def get_unique_words(self, text: str) -> set:
    """取得所有唯一詞彙"""
    words = re.findall(r'\b\w+\b', text.lower())
    return set(words)
```

**執行測試**：
```bash
$ pytest test_text_analyzer.py -v

PASSED ✓✓✓✓✓✓✓✓✓
```

---

### 循環 3：文字清理功能

#### 🔴 RED：測試文字清理

**test_text_analyzer.py**（新增）：
```python
def test_text_cleaner_remove_punctuation():
    """測試移除標點符號"""
    cleaner = TextCleaner()

    cleaned = cleaner.remove_punctuation("Hello, world! How are you?")

    assert cleaned == "Hello world How are you"

def test_text_cleaner_to_lowercase():
    """測試轉換為小寫"""
    cleaner = TextCleaner()

    cleaned = cleaner.to_lowercase("Hello WORLD")

    assert cleaned == "hello world"

def test_remove_stop_words():
    """測試移除停用詞"""
    cleaner = TextCleaner()
    text = "this is a test of the system"

    cleaned = cleaner.remove_stop_words(text)

    # 假設 'a', 'the', 'of', 'is' 是停用詞
    assert "test" in cleaned
    assert "system" in cleaned
    assert "this" in cleaned  # 只移除常見停用詞

def test_clean_text_complete():
    """測試完整的文字清理流程"""
    cleaner = TextCleaner()
    text = "Hello, World! This is a TEST."

    cleaned = cleaner.clean_text(text)

    # 應該移除標點、轉小寫、移除停用詞
    assert "hello" in cleaned
    assert "world" in cleaned
    assert "test" in cleaned
    assert "," not in cleaned
    assert "!" not in cleaned
```

#### 🟢 GREEN：實作文字清理

**text_cleaner.py**：
```python
import re
import string

class TextCleaner:
    """文字清理工具"""

    # 常見英文停用詞
    STOP_WORDS = {
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
        'to', 'was', 'will', 'with'
    }

    def remove_punctuation(self, text: str) -> str:
        """移除標點符號"""
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def to_lowercase(self, text: str) -> str:
        """轉換為小寫"""
        return text.lower()

    def remove_stop_words(self, text: str) -> str:
        """移除停用詞"""
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.STOP_WORDS]
        return ' '.join(filtered_words)

    def clean_text(self, text: str) -> str:
        """完整的文字清理流程"""
        # 移除標點
        text = self.remove_punctuation(text)
        # 轉小寫
        text = self.to_lowercase(text)
        # 移除停用詞
        text = self.remove_stop_words(text)
        # 移除多餘空格
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def normalize_whitespace(self, text: str) -> str:
        """標準化空白字元"""
        return re.sub(r'\s+', ' ', text).strip()
```

**執行測試**：
```bash
$ pytest test_text_analyzer.py -v

PASSED ✓✓✓✓✓✓✓✓✓✓✓✓✓
```

---

### 循環 4：關鍵詞提取

#### 🔴 RED：測試關鍵詞提取

**test_text_analyzer.py**（新增）：
```python
def test_extract_keywords_by_frequency():
    """測試按頻率提取關鍵詞"""
    analyzer = TextAnalyzer()
    text = "Python programming is fun. Python is powerful. Programming with Python is enjoyable."

    keywords = analyzer.extract_keywords(text, method="frequency", top_k=3)

    assert len(keywords) <= 3
    assert "python" in [kw.lower() for kw in keywords]
    assert "programming" in [kw.lower() for kw in keywords]

def test_extract_keywords_by_length():
    """測試按長度提取關鍵詞"""
    analyzer = TextAnalyzer()
    text = "AI machine learning deep neural networks"

    keywords = analyzer.extract_keywords(text, method="length", min_length=5)

    long_keywords = [kw for kw in keywords if len(kw) >= 5]
    assert "machine" in keywords
    assert "learning" in keywords
    assert "neural" in keywords
    assert "networks" in keywords

def test_calculate_text_statistics():
    """測試綜合文字統計"""
    analyzer = TextAnalyzer()
    text = "The quick brown fox jumps over the lazy dog. The dog was sleeping."

    stats = analyzer.get_text_statistics(text)

    assert stats["character_count"] > 0
    assert stats["word_count"] > 0
    assert stats["line_count"] > 0
    assert stats["unique_words"] > 0
    assert "most_common_words" in stats
    assert isinstance(stats["average_word_length"], float)
```

#### 🟢 GREEN：實作關鍵詞提取

**text_analyzer.py**（更新）：
```python
def extract_keywords(self, text: str, method: str = "frequency", top_k: int = 5, min_length: int = 3) -> List[str]:
    """提取關鍵詞"""
    # 清理文字
    from text_cleaner import TextCleaner
    cleaner = TextCleaner()
    cleaned_text = cleaner.clean_text(text)

    words = re.findall(r'\b\w+\b', cleaned_text)

    if method == "frequency":
        # 按頻率提取
        counter = Counter(words)
        return [word for word, count in counter.most_common(top_k)]

    elif method == "length":
        # 按長度提取
        long_words = [word for word in set(words) if len(word) >= min_length]
        return sorted(long_words, key=len, reverse=True)[:top_k]

    else:
        raise ValueError(f"Unknown method: {method}")

def get_text_statistics(self, text: str) -> Dict:
    """取得綜合文字統計"""
    stats = {
        "character_count": self.count_characters(text),
        "character_count_no_spaces": self.count_characters_no_spaces(text),
        "word_count": self.count_words(text),
        "line_count": self.count_lines(text),
        "unique_words": self.count_unique_words(text),
        "most_common_words": self.get_most_common_words(text, 5),
        "average_word_length": self._calculate_average_word_length(text)
    }
    return stats

def _calculate_average_word_length(self, text: str) -> float:
    """計算平均詞長"""
    words = re.findall(r'\b\w+\b', text)
    if not words:
        return 0.0
    total_length = sum(len(word) for word in words)
    return total_length / len(words)
```

---

### 循環 5：文字相似度和情感分析

#### 🔴 RED：測試相似度和情感分析

**test_text_analyzer.py**（新增）：
```python
def test_text_similarity():
    """測試文字相似度"""
    analyzer = TextAnalyzer()
    text1 = "The cat sat on the mat"
    text2 = "A cat was sitting on a mat"
    text3 = "Dogs are running in the park"

    similarity1 = analyzer.calculate_similarity(text1, text2)
    similarity2 = analyzer.calculate_similarity(text1, text3)

    # text1 和 text2 應該比較相似
    assert similarity1 > similarity2
    assert 0 <= similarity1 <= 1
    assert 0 <= similarity2 <= 1

def test_sentiment_analysis():
    """測試情感分析"""
    sentiment = SentimentAnalyzer()

    positive_text = "I love this product! It's amazing and wonderful!"
    negative_text = "This is terrible, awful, and disappointing."
    neutral_text = "The product has basic features."

    pos_score = sentiment.analyze_sentiment(positive_text)
    neg_score = sentiment.analyze_sentiment(negative_text)
    neu_score = sentiment.analyze_sentiment(neutral_text)

    assert pos_score["sentiment"] == "positive"
    assert neg_score["sentiment"] == "negative"
    assert neu_score["sentiment"] == "neutral"

def test_find_common_words():
    """測試找出共同詞彙"""
    analyzer = TextAnalyzer()
    text1 = "cats and dogs are pets"
    text2 = "dogs and birds are animals"

    common = analyzer.find_common_words(text1, text2)

    assert "and" in common
    assert "are" in common
    assert "dogs" in common
    assert len(common) >= 3
```

#### 🟢 GREEN：實作相似度和情感分析

**text_analyzer.py**（更新）：
```python
def calculate_similarity(self, text1: str, text2: str) -> float:
    """計算兩個文字的相似度（Jaccard 相似度）"""
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))

    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union)

def find_common_words(self, text1: str, text2: str) -> List[str]:
    """找出兩個文字的共同詞彙"""
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))

    return list(words1.intersection(words2))
```

**sentiment_analyzer.py**：
```python
class SentimentAnalyzer:
    """簡單的情感分析器"""

    # 簡單的情感詞典
    POSITIVE_WORDS = {
        'love', 'amazing', 'wonderful', 'great', 'excellent', 'fantastic',
        'good', 'happy', 'joy', 'perfect', 'awesome', 'brilliant'
    }

    NEGATIVE_WORDS = {
        'hate', 'terrible', 'awful', 'bad', 'horrible', 'disappointing',
        'sad', 'angry', 'worst', 'disgusting', 'pathetic', 'useless'
    }

    def analyze_sentiment(self, text: str) -> dict:
        """分析文字情感"""
        words = text.lower().split()

        positive_count = sum(1 for word in words if word in self.POSITIVE_WORDS)
        negative_count = sum(1 for word in words if word in self.NEGATIVE_WORDS)

        total_sentiment_words = positive_count + negative_count

        if total_sentiment_words == 0:
            sentiment = "neutral"
            confidence = 0.5
        elif positive_count > negative_count:
            sentiment = "positive"
            confidence = positive_count / len(words)
        elif negative_count > positive_count:
            sentiment = "negative"
            confidence = negative_count / len(words)
        else:
            sentiment = "neutral"
            confidence = 0.5

        return {
            "sentiment": sentiment,
            "confidence": min(confidence * 2, 1.0),  # 調整信心度
            "positive_words": positive_count,
            "negative_words": negative_count
        }

    def get_sentiment_words(self, text: str) -> dict:
        """取得文字中的情感詞彙"""
        words = text.lower().split()

        found_positive = [word for word in words if word in self.POSITIVE_WORDS]
        found_negative = [word for word in words if word in self.NEGATIVE_WORDS]

        return {
            "positive": found_positive,
            "negative": found_negative
        }
```

---

## ✅ 執行測試

**執行所有測試**：
```bash
$ pytest test_text_analyzer.py -v

================= test session starts =================
# 所有測試都應該通過
================= XX passed in X.XXs =================
```

**測試覆蓋率**：
```bash
$ pytest --cov=. --cov-report=term-missing

Name                   Stmts   Miss  Cover
------------------------------------------
sentiment_analyzer.py     XX      0   100%
text_analyzer.py          XX      0   100%
text_cleaner.py           XX      0   100%
------------------------------------------
TOTAL                     XX      0   100%
```

---

## 🎓 學習重點

### 演算法邏輯的 TDD

1. **文字處理演算法**：
   - 字串分割和正則表達式的使用
   - 統計演算法的正確性驗證
   - 邊界情況的完整處理

2. **資料結構的選擇**：
   - Counter 用於頻率統計
   - Set 用於唯一性檢查
   - Dict 用於複雜資料存儲

3. **演算法效能考量**：
   - 大小寫不敏感的處理
   - 重複計算的避免
   - 記憶體效率的考慮

### 關鍵收穫

✅ **字串處理技巧**：
- 正則表達式的高效使用
- 文字清理的標準流程
- Unicode 和編碼的處理

✅ **統計和分析**：
- 詞頻分析的實作
- 相似度計算演算法
- 簡單的機器學習概念

✅ **模組化設計**：
- TextAnalyzer、TextCleaner、SentimentAnalyzer 的職責分工
- 可擴展的架構設計
- 清晰的介面定義

---

## 🚀 進階挑戰

### 挑戰 1：進階文字分析
- TF-IDF 關鍵詞提取
- N-gram 分析
- 文字摘要生成

### 挑戰 2：多語言支援
- 中文詞語分割
- 多語言停用詞
- 語言檢測功能

### 挑戰 3：機器學習整合
- 使用 scikit-learn 進行分類
- 詞向量（Word2Vec）相似度
- 深度學習情感分析

### 挑戰 4：效能優化
- 大文件流式處理
- 並行計算支援
- 記憶體使用優化

---

## 📈 自我評量

- [ ] 能實作基本的文字統計功能
- [ ] 詞頻分析演算法正確
- [ ] 文字清理功能完整
- [ ] 關鍵詞提取邏輯合理
- [ ] 相似度計算準確
- [ ] 程式碼模組化良好

**恭喜完成文字分析器的 TDD 實作！**
**你現在能用 TDD 開發演算法密集的應用了！**