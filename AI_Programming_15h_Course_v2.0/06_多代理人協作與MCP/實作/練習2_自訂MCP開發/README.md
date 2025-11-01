# 練習 2：自訂 MCP 開發 - 建立你的第一個 MCP Server

## 📋 練習概述

**目標**：從零開始開發一個自訂 MCP Server，實作 Weather API MCP，讓 Claude Code 能夠查詢天氣資訊。

**時間**：4-5 小時

**難度**：★★★★☆

**學習重點**：
- 理解 MCP 協議架構
- 實作 MCP Server
- 測試與除錯 MCP
- 整合到 Claude Code

---

## 🎯 專案目標

### 你將建立的 MCP Server

**Weather MCP Server**：提供天氣查詢功能

**核心功能**：
1. 查詢指定城市的當前天氣
2. 查詢未來 7 天天氣預報
3. 查詢多個城市的天氣比較
4. 天氣警報通知

**技術棧**：
- 語言：TypeScript / Python（擇一）
- MCP SDK：`@modelcontextprotocol/sdk`（TypeScript）或 `mcp` (Python)
- 外部 API：OpenWeatherMap API（免費）

---

## 🏗️ MCP 架構理解

### MCP 基本概念

```
┌─────────────────┐          ┌──────────────────┐
│  Claude Code    │          │  Your MCP Server │
│  (Host/Client)  │  ←MCP→   │  (Weather API)   │
└─────────────────┘          └──────────────────┘
                                      ↓
                             ┌──────────────────┐
                             │ OpenWeatherMap   │
                             │ API              │
                             └──────────────────┘
```

### MCP Server 的核心組件

1. **Tools**（工具）：Claude 可以調用的功能
   ```typescript
   {
     name: "get_current_weather",
     description: "Get current weather for a city",
     inputSchema: {
       type: "object",
       properties: {
         city: { type: "string" },
         units: { type: "string", enum: ["metric", "imperial"] }
       }
     }
   }
   ```

2. **Resources**（資源）：Claude 可以讀取的資料
   ```typescript
   {
     uri: "weather://beijing/current",
     mimeType: "application/json",
     description: "Current weather in Beijing"
   }
   ```

3. **Prompts**（提示模板）：預定義的提示詞
   ```typescript
   {
     name: "weather_analysis",
     description: "Analyze weather data",
     arguments: [
       { name: "city", description: "City name", required: true }
     ]
   }
   ```

---

## 📝 實作步驟

### Step 1：環境準備（30 分鐘）

**1.1 取得 OpenWeatherMap API Key**

1. 前往 https://openweathermap.org/api
2. 註冊免費帳號
3. 生成 API Key（免費版足夠，每分鐘 60 次請求）
4. 測試 API：
   ```bash
   curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"
   ```

**1.2 初始化專案**

選擇你熟悉的語言：

**TypeScript 版本**：
```bash
mkdir weather-mcp-server
cd weather-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk typescript @types/node
npm install axios dotenv
npx tsc --init
```

**Python 版本**：
```bash
mkdir weather-mcp-server
cd weather-mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install mcp requests python-dotenv
```

**1.3 環境變數設定**

創建 `.env` 檔案：
```bash
OPENWEATHER_API_KEY=your_api_key_here
```

創建 `.gitignore`：
```gitignore
node_modules/
.env
*.log
dist/
venv/
__pycache__/
```

---

### Step 2：實作基礎 MCP Server（1.5 小時）

**2.1 建立 Server 骨架**

**TypeScript 版本** (`src/index.ts`)：
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios from "axios";
import * as dotenv from "dotenv";

dotenv.config();

const API_KEY = process.env.OPENWEATHER_API_KEY;
const BASE_URL = "https://api.openweathermap.org/data/2.5";

// 創建 MCP Server
const server = new Server(
  {
    name: "weather-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// 稍後在這裡添加 tools

// 啟動 server
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Python 版本** (`server.py`)：
```python
import os
import asyncio
import requests
from mcp.server.models import InitializationOptions
from mcp.server.server import Server
from mcp.server.stdio import stdio_server
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# 創建 MCP Server
server = Server("weather-mcp-server")

# 稍後在這裡添加 tools

# 啟動 server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather-mcp-server",
                server_version="1.0.0",
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
```

**2.2 實作第一個 Tool：`get_current_weather`**

**任務**：
```
User: "台北現在天氣如何？"

Claude 應該能夠：
1. 調用 get_current_weather tool
2. 傳入 city="Taipei"
3. 返回當前天氣資訊
```

**TypeScript 實作**：
```typescript
server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "get_current_weather",
        description: "Get current weather for a city",
        inputSchema: {
          type: "object",
          properties: {
            city: {
              type: "string",
              description: "City name (e.g., 'London', 'Taipei')",
            },
            units: {
              type: "string",
              enum: ["metric", "imperial"],
              description: "Temperature units (metric for Celsius, imperial for Fahrenheit)",
              default: "metric",
            },
          },
          required: ["city"],
        },
      },
    ],
  };
});

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "get_current_weather") {
    const { city, units = "metric" } = request.params.arguments;

    try {
      const response = await axios.get(`${BASE_URL}/weather`, {
        params: {
          q: city,
          appid: API_KEY,
          units: units,
        },
      });

      const data = response.data;
      const weather = {
        city: data.name,
        temperature: data.main.temp,
        feels_like: data.main.feels_like,
        humidity: data.main.humidity,
        description: data.weather[0].description,
        wind_speed: data.wind.speed,
      };

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(weather, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error fetching weather: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});
```

**測試**：
```bash
# 編譯（TypeScript）
npx tsc

# 測試執行
node dist/index.js
```

---

### Step 3：添加更多功能（1.5 小時）

**3.1 實作 `get_forecast` Tool**

**功能**：查詢未來 7 天天氣預報

**API 端點**：
```
https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}
```

**Tool 定義**：
```typescript
{
  name: "get_forecast",
  description: "Get 7-day weather forecast for a city",
  inputSchema: {
    type: "object",
    properties: {
      city: { type: "string", description: "City name" },
      days: {
        type: "number",
        description: "Number of days (1-7)",
        default: 7,
        minimum: 1,
        maximum: 7,
      },
    },
    required: ["city"],
  },
}
```

**實作重點**：
- API 返回每 3 小時的預報
- 需要分組為每日預報
- 提取最高/最低溫度

**3.2 實作 `compare_weather` Tool**

**功能**：比較多個城市的天氣

**範例使用**：
```
User: "比較台北、東京、首爾的天氣"

返回：
- 三個城市的當前溫度
- 天氣描述
- 溫差分析
```

**實作提示**：
- 並行調用 OpenWeatherMap API（多個城市）
- 聚合結果
- 提供比較分析

**3.3 實作 `weather_alert` Resource**

**功能**：提供天氣警報資訊（如極端天氣）

**Resource 定義**：
```typescript
{
  uri: "weather://alerts",
  mimeType: "application/json",
  description: "Current weather alerts",
}
```

---

### Step 4：整合到 Claude Code（30 分鐘）

**4.1 更新 MCP 配置**

編輯 `.claude/mcp-config.json`：

**TypeScript 版本**：
```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["/path/to/weather-mcp-server/dist/index.js"],
      "env": {
        "OPENWEATHER_API_KEY": "${OPENWEATHER_API_KEY}"
      }
    }
  }
}
```

**Python 版本**：
```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/weather-mcp-server/server.py"],
      "env": {
        "OPENWEATHER_API_KEY": "${OPENWEATHER_API_KEY}"
      }
    }
  }
}
```

**4.2 測試整合**

1. 重啟 Claude Code
2. 測試指令：
   ```
   User: "台北現在天氣如何？"
   User: "未來一週台北的天氣預報"
   User: "比較台北、東京、首爾的天氣"
   ```

**預期結果**：
- Claude Code 應該能調用你的 MCP
- 正確返回天氣資訊
- 錯誤處理正常

---

### Step 5：錯誤處理與優化（1 小時）

**5.1 錯誤處理**

**常見錯誤**：
1. **城市名稱錯誤**
   ```typescript
   if (response.data.cod === "404") {
     return {
       content: [{
         type: "text",
         text: `City '${city}' not found. Please check the spelling.`
       }],
       isError: true,
     };
   }
   ```

2. **API Key 無效**
   ```typescript
   if (response.data.cod === 401) {
     return {
       content: [{
         type: "text",
         text: "Invalid API key. Please check your OPENWEATHER_API_KEY."
       }],
       isError: true,
     };
   }
   ```

3. **Rate Limit 超限**
   ```typescript
   if (response.data.cod === 429) {
     return {
       content: [{
         type: "text",
         text: "API rate limit exceeded. Please try again later."
       }],
       isError: true,
     };
   }
   ```

**5.2 快取機制**

**問題**：相同城市頻繁查詢浪費 API 配額

**解決**：實作簡單快取
```typescript
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 分鐘

function getCachedWeather(city: string) {
  const cached = cache.get(city);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }
  return null;
}

function setCachedWeather(city: string, data: any) {
  cache.set(city, { data, timestamp: Date.now() });
}
```

**5.3 日誌記錄**

```typescript
function log(level: string, message: string, data?: any) {
  const timestamp = new Date().toISOString();
  console.error(`[${timestamp}] [${level}] ${message}`, data || "");
}

// 使用
log("INFO", "Fetching weather for city", { city });
log("ERROR", "API request failed", { error: error.message });
```

---

## ✅ 評量標準

### 基礎功能（60 分）

- [ ] `get_current_weather` 正確實作（20 分）
- [ ] `get_forecast` 正確實作（20 分）
- [ ] 成功整合到 Claude Code（20 分）

### 進階功能（25 分）

- [ ] `compare_weather` 實作（10 分）
- [ ] 快取機制實作（10 分）
- [ ] 完善的錯誤處理（5 分）

### 代碼品質（15 分）

- [ ] TypeScript types / Python type hints（5 分）
- [ ] 日誌記錄（5 分）
- [ ] 程式碼結構清晰（5 分）

**總分**：100 分
**及格標準**：70 分

---

## 💡 提示與技巧

### 提示 1：除錯 MCP Server

**問題**：MCP Server 無反應

**除錯步驟**：
1. 檢查 server 是否正常啟動：
   ```bash
   node dist/index.js
   # 應該不報錯，等待輸入
   ```

2. 檢查 Claude Code 日誌：
   ```bash
   # 查看 Claude Code 的 MCP 日誌
   # 位置視作業系統而定
   ```

3. 手動測試 tool：
   ```bash
   # 發送測試請求（使用 MCP 協議格式）
   echo '{"method":"tools/list"}' | node dist/index.js
   ```

### 提示 2：API 配額管理

**免費版 OpenWeatherMap**：
- 每分鐘 60 次請求
- 每月 100 萬次請求

**節省配額**：
- 實作快取（5 分鐘 TTL）
- 批次查詢（一次查多個城市）
- 避免不必要的重複查詢

### 提示 3：增強用戶體驗

**溫度單位**：
```typescript
function formatTemperature(temp: number, units: string): string {
  const unit = units === "metric" ? "°C" : "°F";
  return `${Math.round(temp)}${unit}`;
}
```

**天氣描述本地化**：
```typescript
const translations = {
  "clear sky": "晴朗",
  "few clouds": "少雲",
  "scattered clouds": "多雲",
  "broken clouds": "陰天",
  "shower rain": "陣雨",
  "rain": "雨",
  "thunderstorm": "雷雨",
  "snow": "雪",
  "mist": "霧",
};
```

---

## 🎓 學習檢查點

完成練習後，你應該能夠：

- [ ] 理解 MCP 協議的基本架構
- [ ] 知道如何定義 Tools, Resources, Prompts
- [ ] 能夠實作 MCP Server 的請求處理
- [ ] 理解 MCP 與 Claude Code 的互動方式
- [ ] 知道如何整合外部 API
- [ ] 能夠實作錯誤處理和快取
- [ ] 知道如何除錯 MCP Server

---

## 🚀 擴展挑戰

完成基礎功能後，可以挑戰：

### 挑戰 1：多語言支援

**目標**：支援多種語言的天氣描述

**實作**：
- 添加 `language` 參數（`zh-TW`, `en`, `ja`）
- OpenWeatherMap API 支援 `lang` 參數
- 返回本地化的天氣描述

### 挑戰 2：天氣圖表

**目標**：生成天氣趨勢圖

**實作**：
- 使用 Chart.js 或 Matplotlib
- 生成溫度趨勢圖
- 返回圖表 URL 或 Base64

### 挑戰 3：智能建議

**目標**：根據天氣提供建議

**實作**：
- 下雨 → 建議帶傘
- 高溫 → 建議多喝水
- 低溫 → 建議添衣
- 空氣品質差 → 建議戴口罩

### 挑戰 4：多 API 支援

**目標**：整合多個天氣 API

**實作**：
- OpenWeatherMap + Weather.com
- 比較不同來源的預報
- 提供更準確的預測

### 挑戰 5：Webhook 通知

**目標**：天氣變化時自動通知

**實作**：
- 監控特定城市天氣
- 溫度變化 > 5°C → 通知
- 預報下雨 → 提前通知
- 整合 Slack MCP 發送通知

---

## 📚 參考資源

### MCP 官方文檔

- MCP 協議規範：https://modelcontextprotocol.io/
- TypeScript SDK：https://github.com/modelcontextprotocol/typescript-sdk
- Python SDK：https://github.com/modelcontextprotocol/python-sdk

### OpenWeatherMap API

- API 文檔：https://openweathermap.org/api
- 當前天氣 API：https://openweathermap.org/current
- 預報 API：https://openweathermap.org/forecast5

### 範例參考

- 官方 MCP Server 範例：https://github.com/modelcontextprotocol/servers
- GitHub MCP Server：參考其架構設計
- Database MCP Server：參考錯誤處理

---

## 🎯 完成後的下一步

1. **分享你的 MCP Server**
   - 發布到 npm / PyPI
   - 分享給團隊使用
   - 貢獻到 MCP 社群

2. **開發更多 MCP**
   - News MCP（新聞查詢）
   - Finance MCP（股票資訊）
   - Translation MCP（翻譯服務）
   - 任何你需要的 API 整合

3. **深入學習**
   - MCP 進階功能（Sampling, Completion）
   - MCP 效能優化
   - MCP 安全最佳實踐

---

**開始建立你的第一個 MCP Server！** 🚀

**記住**：
> MCP 的強大之處在於
> 讓 Claude 能夠與任何服務互動
> 你的創意就是極限
