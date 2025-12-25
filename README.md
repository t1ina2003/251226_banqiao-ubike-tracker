# 板橋車站 YouBike 2.0 追蹤器

這個專案主要用於追蹤板橋車站附近的 YouBike 2.0 站點即時車況，並將歷史數據記錄下來，透過網頁圖表呈現趨勢。

## 功能

- 自動抓取新北市 Open Data API 的 YouBike 2.0 即時資料。
- 篩選板橋車站周邊的特定站點（如：板橋車站、捷運板橋站等）。
- 將數據儲存為 JSON 格式，保留歷史紀錄。
- 提供 `index.html` 網頁介面，使用 Chart.js 繪製剩餘車位趨勢圖。

## 檔案說明

- `fetch_ubike_data.py`: 主程式，負責抓取與更新數據。
- `ubike_data.json`: 儲存歷史數據的資料檔。
- `index.html`: 顯示數據圖表的網頁。
- `requirements.txt`: Python 套件需求清單。

## 使用方式

### 1. 安裝環境

請確保已安裝 Python 3，並安裝所需套件：

```bash
pip install -r requirements.txt
```

### 2. 抓取數據

執行 Python 腳本來抓取最新數據：

```bash
python fetch_ubike_data.py
```

執行後會更新 `ubike_data.json` 檔案。

### 3. 查看圖表

直接用瀏覽器打開 `index.html` 檔案即可查看最新的車位趨勢圖。

## 自動化建議

若要長期追蹤，建議使用 Windows 的「工作排程器」或 Linux 的 `cron`，設定每 30 分鐘執行一次 `fetch_ubike_data.py`。
