# X-ray Void Calculator v4.0 (AOI 氣泡空洞率檢測分析軟體)

![Language](https://img.shields.io/badge/Language-Python-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![UI](https://img.shields.io/badge/UI-Modern_Dark-orange.svg)

[繁體中文](#繁體中文) | [English](#english)

---

## 繁體中文

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
    python Void4.0.py
    ```

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
2.  **Otsu's Binarization**: Automatically determines the mathematical optimal threshold by maximizing intra-class variance.
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
    python Void4.0.py
    ```

### 軟體截圖 (Screenshots)
![英文主介面](./screenshots/main_ui1.png)
![英文文主介面](./screenshots/main_ui2.png)
![中文主介面](./screenshots/main_ui3.png)
![報表範例](./screenshots/report_sample.jpg)