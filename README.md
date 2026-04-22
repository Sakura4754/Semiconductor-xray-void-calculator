# X-ray Void Calculator v4.0 (AOI 氣泡空洞率檢測分析軟體)

![Language](https://img.shields.io/badge/Language-Python-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![UI](https://img.shields.io/badge/UI-Modern_Dark-orange.svg)
![License](https://img.shields.io/badge/License-GPLv3-green.svg)

[繁體中文](#繁體中文-traditional-chinese) | [简体中文](#简体中文-simplified-chinese) | [English](#english) | [日本語](#日本語-japanese) | [한국어](#한국어-korean) | [Français](#français-french) | [Deutsch](#deutsch-german)

---

## 軟體截圖 (Screenshots)
![英文主介面](./screenshots/main_ui1.png)
![英文文主介面](./screenshots/main_ui2.png)
![中文主介面](./screenshots/main_ui3.png)
![報表範例](./screenshots/report_sample.jpg)

---

## 繁體中文 (Traditional Chinese)

這是一款專為半導體封裝、SMT 銲錫點及工業 X-ray 影像設計的 **AOI (自動光學檢測)** 輔助軟體。它能自動辨識影像中的氣泡空洞，並精確計算其佔比 (Void Rate)。

### ✨ 核心功能
* **AI 智能最佳化**：整合 **Otsu (大津演算法)**，一鍵自動分析影像背景並設定最完美的氣泡切割閾值。
* **像素級邊界防護**：導入 **Bilateral Filter (雙邊濾波)**，在消除雜訊的同時，完美保留氣泡最銳利的真實物理輪廓。
* **無死角攝影機系統**：支援極致順暢的縮放 (Zoom) 與平移 (Pan)，輕鬆觀察微小瑕疵。
* **全方位編修工具**：提供框選 ROI、手動補點、橡皮擦，以及智慧油漆桶填滿功能。
* **專業報表匯出**：一鍵產生包含氣泡編號、各別佔比、總空洞率及時間浮水印的高畫質報表。

### 🧠 演算法原理
1.  **黑帽特徵提取 (Blackhat)**：有效排除曝光不均的背景，僅提取比周圍暗的孔洞特徵。
2.  **大津演算法 (Otsu's Method)**：透過數學統計像素直方圖，自動尋找最佳類間變異數作為閾值。
3.  **雙邊濾波邊緣防護**：取代傳統形態學，避免邊緣被過度磨圓導致空洞率失真。
4.  **連通域分析**：對氣泡進行幾何過濾 (面積與圓形度)，排除非瑕疵雜訊。

### 🛠️ 安裝與執行
1.  **環境要求**：Python 3.8+ (建議使用 3.12 以獲得最佳效能)。
2.  **安裝套件**：
    ```bash
    pip install opencv-python pillow numpy
    ```
3.  **執行程式**：
    ```bash
    python main.py
    ```

### 📜 開源宣告與致謝 (Acknowledgments)
本專案的開發與執行依賴於以下優秀的開源社群專案，特此致謝：
* **[OpenCV](https://opencv.org/)** - 影像處理與電腦視覺核心 (Licensed under Apache License 2.0)
* **[NumPy](https://numpy.org/)** - 矩陣與科學計算 (Licensed under BSD 3-Clause License)
* **[Pillow](https://python-pillow.org/)** - 影像格式轉換與處理 (Licensed under HPND License)

本軟體採用 **GPLv3 License** 授權，您可以自由使用、修改與散佈，但衍生作品必須採用相同授權開源。詳情請參閱 `LICENSE.md`。

---

## 简体中文 (Simplified Chinese)

这是一款专为半导体封装、SMT 焊锡点及工业 X-ray 影像设计的 **AOI (自动光学检测)** 辅助软件。它能自动识别影像中的气泡空洞，并精确计算其占比 (Void Rate)。

### ✨ 核心功能
* **AI 智能优化**：整合 **Otsu (大津算法)**，一键自动分析影像背景并设定最完美的气泡切割阈值。
* **像素级边界防护**：导入 **Bilateral Filter (双边滤波)**，在消除噪点的同时，完美保留气泡最锐利的真实物理轮廓。
* **无死角摄影机系统**：支持极致顺畅的缩放 (Zoom) 与平移 (Pan)，轻松观察微小瑕疵。
* **全方位编修工具**：提供框选 ROI、手动补点、橡皮擦，以及智能油漆桶填满功能。
* **专业报表导出**：一键生成包含气泡编号、个别占比、总空洞率及时间水印的高画质报表。

### 🧠 算法原理
1.  **黑帽特征提取 (Blackhat)**：有效排除曝光不均的背景，仅提取比周围暗的孔洞特征。
2.  **大津算法 (Otsu's Method)**：通过数学统计像素直方图，自动寻找最佳类间方差作为阈值。
3.  **双边滤波边缘防护**：取代传统形态学，避免边缘被过度磨圆导致空洞率失真。
4.  **连通域分析**：对气泡进行几何过滤 (面积与圆形度)，排除非瑕疵噪点。

### 🛠️ 安装与运行
1.  **环境要求**：Python 3.8+ (建议使用 3.12 以获得最佳性能)。
2.  **安装依赖**：
    ```bash
    pip install opencv-python pillow numpy
    ```
3.  **运行程序**：
    ```bash
    python main.py
    ```

### 📜 开源宣告与致谢 (Acknowledgments)
本项目依赖于以下优秀的开源项目：OpenCV (Apache 2.0), NumPy (BSD 3-Clause), Pillow (HPND)。本软件采用 **GPLv3 License** 授权。

---

## English

A specialized **AOI (Automated Optical Inspection)** assistant software designed for semiconductor packaging, SMT solder joints, and industrial X-ray imaging. It automatically detects voids and accurately calculates the **Void Rate**.

### ✨ Key Features
* **AI Optimization**: Integrated **Otsu's Method** for one-click automatic analysis of imaging background and optimal thresholding.
* **Pixel-Perfect Edge Protection**: Implements **Bilateral Filtering** to eliminate noise while preserving sharp physical boundaries.
* **Smooth Camera Engine**: Seamless zooming and panning to inspect microscopic defects effortlessly.
* **Comprehensive Editing Tools**: Includes ROI selection, manual drawing, erasing, and smart flood-fill tools.
* **Professional Report Export**: Generates high-resolution reports with bubble numbering, individual percentages, total void rate, and timestamps.

### 🧠 Principles & Algorithms
1.  **Morphological Blackhat**: Extracts dark features (voids) while effectively ignoring uneven background illumination.
2.  **Otsu's Binarization**: Automatically determines the mathematically optimal threshold by maximizing intra-class variance.
3.  **Bilateral Edge Guard**: Prevents edge "bloating" or "rounding" typical in traditional morphology, ensuring accurate calculations.
4.  **Geometric Filtering**: Filters detections based on area and circularity to eliminate non-defect noise.

### 🛠️ Installation & Usage
1.  **Prerequisites**: Python 3.8+ (Python 3.12 recommended).
2.  **Required Libraries**:
    ```bash
    pip install opencv-python pillow numpy
    ```
3.  **Run Application**:
    ```bash
    python main.py
    ```

### 📜 Open Source Acknowledgments & License
This project relies on the following excellent open-source projects:
* **[OpenCV](https://opencv.org/)** (Apache License 2.0)
* **[NumPy](https://numpy.org/)** (BSD 3-Clause License)
* **[Pillow](https://python-pillow.org/)** (HPND License)

This software is licensed under the **GPLv3 License**. You are free to use, modify, and distribute it, but derivative works must also be open-source under the same license. See `LICENSE.md` for details.

---

## 日本語 (Japanese)

半導体パッケージング、SMTはんだ接合部、および産業用X線画像向けに設計された **AOI（自動光学検査）** 支援ソフトウェアです。画像内のボイド（気泡）を自動的に検出し、そのボイド率（Void Rate）を正確に計算します。

### ✨ 主な機能
* **AI 自動最適化**: **大津の2値化 (Otsu's Method)** を統合し、背景を分析して最適な閾値をワンクリックで設定します。
* **ピクセルレベルのエッジ保護**: **バイラテラルフィルタ (Bilateral Filter)** を導入し、ノイズを除去しつつ、物理的な境界を鋭く保ちます。
* **スムーズなカメラエンジン**: シームレスなズームとパンで微小な欠陥を簡単に観察できます。
* **充実した編集ツール**: ROI選択、手動描画、消しゴム、スマート塗りつぶしツールを提供します。
* **プロフェッショナルなレポート出力**: ボイド番号、個別の割合、全体のボイド率、透かしを含む高解像度レポートを生成します。

### 🛠️ インストールと実行
```bash
pip install opencv-python pillow numpy
python main.py