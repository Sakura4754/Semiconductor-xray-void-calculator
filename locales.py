def get_i18n_dict():
    # ================= 說明文件變數宣告 =================
    zh_tw_guide = (
        "【 檢測流程與基本操作 】\n\n"
        "1. 檔案載入：從左上角「檔案」讀取 X-ray 影像檔或專案檔 (.vod)。\n"
        "2. 縮放與平移：\n"
        "   • 畫面內捲動滑鼠滾輪可「無死角縮放」。\n"
        "   • 按住滑鼠中鍵 (或切換至平移模式按左鍵) 可「拖曳平移」畫面。\n"
        "3. 右鍵選單：在影像區域點擊右鍵，可快速呼叫工具列切換模式。\n\n"
        "【 參數分析與氣泡框選 】\n\n"
        "1. 框選晶片 (ROI)：切換至「📌 框選」模式，在畫面上拖曳定義檢測範圍。\n"
        "   • 將游標移至框線邊緣即可拖曳調整大小；移至框內可移動整個區塊。\n"
        "2. AI 自動最佳化：點擊面板「🤖 自動最佳化」，系統會啟動 Otsu 演算法分析背景，自動為您找到數學上最完美的氣泡切割閾值。\n"
        "3. 強制疊加遮罩：若畫面有多個亮度落差極大的區塊，可調好一區的參數後點擊「➕ 鎖定並疊加」，再調整參數抓下一區。\n\n"
        "【 手動編修工具 】\n\n"
        "1. 手動補點/擦除：切換至「🖌️ 補點」或「🧼 擦除」，可手動塗抹遺漏的氣泡或擦去雜訊。滾輪可調整畫筆尺寸。\n"
        "2. 智慧填滿 (油漆桶)：切換至「🪣 油漆」，點擊氣泡內部可自動偵測邊界並填滿。滾輪可調整填滿寬容度。\n"
        "3. 孔洞強制密合：勾選「✨ 強制填補內部孔洞」，可自動將所有甜甜圈狀、C字型的氣泡內部破洞填為實心。\n\n"
        "【 報表匯出 】\n\n"
        "1. 勾選「顯示各氣泡編號與佔比」，即可在畫面上標示所有氣泡排名與其個別空洞率。\n"
        "2. 點選「檔案 -> 匯出報表」，即可將目前的檢測框與計算數據打包儲存為高畫質 JPG 報表。"
    )

    zh_cn_guide = (
        "【 检测流程与基本操作 】\n\n"
        "1. 文件载入：从左上角「文件」读取 X-ray 图像文件或项目文件 (.vod)。\n"
        "2. 缩放与平移：\n"
        "   • 画面内滚动鼠标滚轮可「无死角缩放」。\n"
        "   • 按住鼠标中键 (或切换至平移模式按左键) 可「拖曳平移」画面。\n"
        "3. 右键菜单：在图像区域点击右键，可快速呼叫工具栏切换模式。\n\n"
        "【 参数分析与气泡框选 】\n\n"
        "1. 框选芯片 (ROI)：切换至「📌 框选」模式，在画面上拖曳定义检测范围。\n"
        "   • 将光标移至框线边缘即可拖曳调整大小；移至框内可移动整个区块。\n"
        "2. AI 自动优化：点击面板「🤖 自动优化」，系统会启动 Otsu (大津) 算法分析背景，自动为您找到数学上最完美的气泡切割阈值。\n"
        "3. 强制叠加遮罩：若画面有多个亮度落差极大的区块，可调好一区的参数后点击「➕ 锁定并叠加」，再调整参数抓下一区。\n\n"
        "【 手动编修工具 】\n\n"
        "1. 手动补点/擦除：切换至「🖌️ 补点」或「🧼 擦除」，可手动涂抹遗漏的气泡或擦去噪点。滚轮可调整画笔尺寸。\n"
        "2. 智能填满 (油漆桶)：切换至「🪣 油漆」，点击气泡内部可自动检测边界并填满。滚轮可调整填满宽容度。\n"
        "3. 孔洞强制密合：勾选「✨ 强制填补内部孔洞」，可自动将所有甜甜圈状、C字型的气泡内部破洞填为实心。\n\n"
        "【 报表导出 】\n\n"
        "1. 勾选「显示各气泡编号与占比」，即可在画面上标示所有气泡排名与其个别空洞率。\n"
        "2. 点击「文件 -> 导出报表」，即可将目前的检测框与计算数据打包保存为高画质 JPG 报表。"
    )

    en_guide = (
        "[ Basic Operations ]\n\n"
        "1. File Loading: Open images or project files (.vod) via the 'File' menu.\n"
        "2. Zoom & Pan:\n"
        "   • Scroll the mouse wheel to zoom dynamically.\n"
        "   • Hold the middle mouse button (or left-click in Pan mode) to drag and pan the view.\n"
        "3. Context Menu: Right-click on the image to quickly switch between tools.\n\n"
        "[ Detection & ROI ]\n\n"
        "1. Select ROI: Switch to '📌 ROI' mode and drag to define the detection area.\n"
        "   • Drag edges to resize, or drag inside the box to move the entire ROI.\n"
        "2. AI Optimization: Click '🤖 Auto Optimize'. The system utilizes Otsu's method to analyze background and automatically determines the optimal void threshold.\n"
        "3. Mask Accumulation: For unevenly exposed chips, set parameters for one region, click '➕ Lock & Add', and proceed to adjust parameters for the next region.\n\n"
        "[ Manual Editing Tools ]\n\n"
        "1. Draw / Erase: Use '🖌️ Draw' or '🧼 Erase' to manually patch missing voids or remove noise. Scroll to adjust brush size.\n"
        "2. Smart Fill: In '🪣 Fill' mode, click inside a void to fill it automatically. Scroll to adjust flood-fill tolerance.\n"
        "3. Solidify Holes: Enable '✨ Solidify Holes' to automatically fill internal gaps within doughnut-shaped or c-shaped voids.\n\n"
        "[ Exporting ]\n\n"
        "1. Enable 'Show Void Labels & %' to visualize the ranking and specific void rate of each individual bubble.\n"
        "2. Go to 'File -> Export Report' to save the current ROI and calculated data as a high-resolution JPG report."
    )

    ja_guide = (
        "[ 検出フローと基本操作 ]\n\n"
        "1. ファイルの読み込み: 左上の「ファイル」からX線画像またはプロジェクトファイル (.vod) を読み込みます。\n"
        "2. ズームとパン (移動):\n"
        "   • 画面内でマウスホイールをスクロールすると「無段階ズーム」が可能です。\n"
        "   • マウスの中ボタンを長押し (またはパンモードで左クリック) してドラッグすると画面を移動できます。\n"
        "3. 右クリックメニュー: 画像エリアで右クリックすると、ツール切り替えメニューを素早く呼び出せます。\n\n"
        "[ パラメータ分析とROI選択 ]\n\n"
        "1. チップの範囲選択 (ROI): 「📌 選択」モードに切り替え、画面上をドラッグして検出範囲を指定します。\n"
        "   • 枠の端にカーソルを合わせるとサイズ調整、枠内をドラッグすると全体を移動できます。\n"
        "2. AI自動最適化: 「🤖 自動最適化」をクリックすると、Otsu (大津の2値化) アルゴリズムが背景を分析し、数学的に最適な閾値を自動的に見つけ出します。\n"
        "3. マスクのロックと追加: 明暗差が極端に大きい複数の領域がある場合、1つの領域のパラメータを調整してから「➕ ロックして追加」をクリックし、次の領域を調整してください。\n\n"
        "[ 手動編集ツール ]\n\n"
        "1. 手動描画/消去: 「🖌️ 描画」または「🧼 消去」に切り替え、検出漏れのボイドを塗りつぶしたり、ノイズを消したりできます。ホイールでブラシサイズを調整できます。\n"
        "2. スマート塗りつぶし: 「🪣 塗りつぶし」に切り替え、ボイドの内部をクリックすると境界を自動検出し塗りつぶします。ホイールで許容誤差を調整できます。\n"
        "3. 内部の穴の強制密着: 「✨ 内部の穴を強制的に埋める」にチェックを入れると、ドーナツ状やC字型のボイド内部の隙間を自動的に実線に変換します。\n\n"
        "[ レポート出力 ]\n\n"
        "1. 「各ボイドの番号と割合を表示」にチェックを入れると、すべてのボイドの順位と個別のボイド率(%)を画面上に表示します。\n"
        "2. 「ファイル -> レポート出力」をクリックすると、現在の検出枠と計算データを高画質なJPGレポートとして保存します。"
    )

    ko_guide = (
        "[ 감지 흐름 및 기본 작업 ]\n\n"
        "1. 파일 불러오기: 왼쪽 상단 '파일'에서 X-ray 이미지 또는 프로젝트 파일(.vod)을 불러옵니다.\n"
        "2. 확대/축소 및 이동:\n"
        "   • 화면 내에서 마우스 휠을 스크롤하여 동적으로 확대/축소할 수 있습니다.\n"
        "   • 마우스 가운데 버튼을 누른 상태로(또는 이동 모드에서 왼쪽 클릭) 드래그하여 화면을 이동할 수 있습니다.\n"
        "3. 우클릭 메뉴: 이미지 영역에서 우클릭하여 도구를 빠르게 전환할 수 있습니다.\n\n"
        "[ 매개변수 분석 및 영역(ROI) 선택 ]\n\n"
        "1. 영역 선택 (ROI): '📌 영역 선택' 모드로 전환하고 화면을 드래그하여 감지 범위를 지정합니다.\n"
        "   • 테두리를 드래그하여 크기를 조정하거나, 상자 내부를 드래그하여 전체 영역을 이동할 수 있습니다.\n"
        "2. AI 자동 최적화: '🤖 자동 최적화'를 클릭하면 시스템이 오츠(Otsu) 알고리즘을 시작하여 배경을 분석하고 가장 완벽한 보이드 분할 임계값을 자동으로 찾습니다.\n"
        "3. 마스크 잠금 및 추가: 밝기 차이가 큰 영역이 여러 개 있는 경우 한 영역의 매개변수를 조정한 후 '➕ 잠금 및 추가'를 클릭하고 다음 영역을 조정합니다.\n\n"
        "[ 수동 편집 도구 ]\n\n"
        "1. 수동 그리기/지우기: '🖌️ 그리기' 또는 '🧼 지우기'로 전환하여 누락된 보이드를 칠하거나 노이즈를 지웁니다. 마우스 휠로 브러시 크기를 조절할 수 있습니다.\n"
        "2. 스마트 채우기: '🪣 채우기'로 전환하고 보이드 내부를 클릭하면 경계를 자동 감지하여 채웁니다. 휠로 허용 오차를 조정할 수 있습니다.\n"
        "3. 내부 구멍 강제 채우기: '✨ 내부 구멍 강제 채우기'를 선택하면 도넛 모양이나 C자형 보이드의 내부 빈 공간을 자동으로 채웁니다.\n\n"
        "[ 보고서 내보내기 ]\n\n"
        "1. '각 보이드 번호 및 비율 표시'를 선택하면 화면에 모든 보이드의 순위와 개별 비율(%)이 표시됩니다.\n"
        "2. '파일 -> 보고서 내보내기'를 클릭하면 현재 감지 영역 및 계산 데이터가 고해상도 JPG 보고서로 저장됩니다."
    )

    fr_guide = (
        "[ Opérations de base ]\n\n"
        "1. Charger un fichier : Ouvrez les images X-ray ou les projets (.vod) via le menu 'Fichier'.\n"
        "2. Zoomer et Déplacer :\n"
        "   • Faites défiler la molette de la souris pour zoomer de manière dynamique.\n"
        "   • Maintenez le bouton central (ou clic gauche en mode Déplacer) pour déplacer la vue.\n"
        "3. Menu Contextuel : Faites un clic droit sur l'image pour basculer rapidement entre les outils.\n\n"
        "[ Détection et Sélection ROI ]\n\n"
        "1. Sélection ROI : Passez en mode '📌 Sélection (ROI)' et glissez pour définir la zone de détection.\n"
        "   • Faites glisser les bords pour redimensionner, ou à l'intérieur pour déplacer toute la zone.\n"
        "2. Optimisation IA : Cliquez sur '🤖 Optimisation Auto'. Le système utilise l'algorithme d'Otsu pour analyser le fond et trouver automatiquement le seuil optimal.\n"
        "3. Verrouiller et Ajouter : S'il y a des différences d'éclairage extrêmes, réglez une zone, cliquez sur '➕ Verrouiller & Ajouter', puis passez à la zone suivante.\n\n"
        "[ Outils d'édition manuelle ]\n\n"
        "1. Dessiner/Effacer : Utilisez '🖌️ Dessiner' ou '🧼 Effacer' pour corriger les vides manquants ou supprimer le bruit. La molette ajuste la taille du pinceau.\n"
        "2. Remplissage intelligent : En mode '🪣 Remplir', cliquez à l'intérieur d'un vide pour le remplir. La molette ajuste la tolérance.\n"
        "3. Remplir les trous internes : Activez '✨ Remplir les trous internes' pour combler automatiquement les espaces dans les vides en forme d'anneau ou de C.\n\n"
        "[ Exporter ]\n\n"
        "1. Cochez 'Afficher numéros et pourcentages' pour visualiser le classement et le taux de vide spécifique de chaque bulle.\n"
        "2. Cliquez sur 'Fichier -> Exporter le rapport' pour enregistrer la zone actuelle et les données sous forme de rapport JPG haute résolution."
    )

    de_guide = (
        "[ Grundlegende Bedienung ]\n\n"
        "1. Datei laden: Öffnen Sie X-Ray-Bilder oder Projektdateien (.vod) über das Menü 'Datei'.\n"
        "2. Zoomen & Verschieben:\n"
        "   • Drehen Sie das Mausrad, um stufenlos zu zoomen.\n"
        "   • Halten Sie die mittlere Maustaste (oder Linksklick im Verschieben-Modus), um das Bild zu verschieben.\n"
        "3. Kontextmenü: Klicken Sie mit der rechten Maustaste auf das Bild, um schnell zwischen den Werkzeugen zu wechseln.\n\n"
        "[ Erkennung und ROI-Auswahl ]\n\n"
        "1. ROI-Auswahl: Wechseln Sie in den Modus '📌 Auswahl (ROI)' und ziehen Sie einen Rahmen über den Erkennungsbereich.\n"
        "   • Ziehen Sie die Ränder, um die Größe zu ändern, oder in der Mitte, um alles zu verschieben.\n"
        "2. KI-Auto-Optimierung: Klicken Sie auf '🤖 Auto-Optimierung'. Das System nutzt den Otsu-Algorithmus, um den Hintergrund zu analysieren und den optimalen Schwellenwert zu finden.\n"
        "3. Sperren & Hinzufügen: Bei Bereichen mit stark unterschiedlicher Helligkeit passen Sie zuerst einen Bereich an, klicken auf '➕ Sperren & Hinzufügen' und bearbeiten dann den nächsten.\n\n"
        "[ Manuelle Bearbeitung ]\n\n"
        "1. Zeichnen/Radieren: Verwenden Sie '🖌️ Zeichnen' oder '🧼 Radieren', um fehlende Hohlräume (Voids) auszubessern oder Rauschen zu entfernen. Das Mausrad ändert die Pinselgröße.\n"
        "2. Intelligentes Füllen: Im Modus '🪣 Füllen' klicken Sie in einen Hohlraum, um ihn zu füllen. Das Mausrad ändert die Toleranz.\n"
        "3. Interne Löcher füllen: Aktivieren Sie '✨ Interne Löcher füllen', um Hohlräume in Ring- oder C-Form automatisch massiv zu füllen.\n\n"
        "[ Exportieren ]\n\n"
        "1. Aktivieren Sie 'Nummern & Prozentsätze anzeigen', um die Rangfolge und die spezifische Void-Rate jedes einzelnen Hohlraums auf dem Bildschirm zu sehen.\n"
        "2. Klicken Sie auf 'Datei -> Bericht exportieren', um den aktuellen Bereich und die Berechnungsdaten als hochauflösenden JPG-Bericht zu speichern."
    )

    # ================= 介面字典檔宣告 =================
    i18n = {
        "zh-TW": {
            "title_default": "X-ray void cal v4.0",
            "m_file": "檔案 (F)", "m_lang": "語言 (L)", "m_help": "說明 (H)",
            "m_open": "選擇圖檔...", "m_load": "讀取專案 (.vod)...", "m_save": "儲存專案 (.vod)...", "m_export": "匯出報表 (.jpg)...", "m_close": "關閉", "m_guide": "操作說明",
            "tab_img": "影像", "tab_void": "氣泡", "tab_edit": "編修",
            "p1_title": "影像狀態與預處理", "p2_title": "智能氣泡檢測參數", "p3_title": "手動編修與檢視控制", "p4_title": "檢測數據分析",
            "chk_inv": "影像正負片反轉", "chk_clahe": "強化對比 (CLAHE)",
            "sl_destripe": "去紋平滑度 (Bilateral)", "sl_clahe_limit": "CLAHE 強度",
            "sl_zoom": "畫面縮放", "sl_sharp": "對焦銳化", "sl_alpha": "亮度/對比", "sl_gamma": "Gamma 校正",
            "sl_kernel": "提取範圍 (Kernel)", "sl_thresh": "擷取靈敏度", "sl_morph": "邊緣平滑", "sl_area": "最小氣泡面積", "sl_circ": "最小圓形度",
            "btn_ai": "自動最佳化", "btn_acc": "鎖定並疊加",
            "tb_pan": "平移", "tb_roi": "框選", "tb_draw": "補點", "tb_erase": "擦除", "tb_fill": "油漆",
            "rm_pan": "平移畫面", "rm_roi": "框選晶片", "rm_draw": "繪製補點", "rm_erase": "擦除修改", "rm_fill": "智慧填滿",
            "sl_brush": "畫筆尺寸", "chk_solid": "強制填補內部孔洞", "sl_gap": "縫隙密合度", 
            "chk_labels": "顯示各氣泡編號與佔比",
            "btn_undo": "復原", "btn_clear": "清空所有修改",
            "chk_mask": "顯示紅光", "sl_opacity": "遮罩透明度", "chk_wm": "存檔加入浮水印",
            "status_ready": "✔️ 系統就緒", "void_lbl": "Void Rate : {0:.2f} %",
            "guide_txt": zh_tw_guide
        },
        "zh-CN": {
            "title_default": "X-ray void cal v4.0",
            "m_file": "文件 (F)", "m_lang": "语言 (L)", "m_help": "说明 (H)",
            "m_open": "选择图档...", "m_load": "读取项目 (.vod)...", "m_save": "保存项目 (.vod)...", "m_export": "导出报表 (.jpg)...", "m_close": "关闭", "m_guide": "操作说明",
            "tab_img": "图像", "tab_void": "气泡", "tab_edit": "编修",
            "p1_title": "图像状态与预处理", "p2_title": "智能气泡检测参数", "p3_title": "手动编修与检视控制", "p4_title": "检测数据分析",
            "chk_inv": "图像正负片反转", "chk_clahe": "强化对比 (CLAHE)",
            "sl_destripe": "去纹平滑度 (Bilateral)", "sl_clahe_limit": "CLAHE 强度",
            "sl_zoom": "画面缩放", "sl_sharp": "对焦锐化", "sl_alpha": "亮度/对比", "sl_gamma": "Gamma 校正",
            "sl_kernel": "提取范围 (Kernel)", "sl_thresh": "提取灵敏度", "sl_morph": "边缘平滑", "sl_area": "最小气泡面积", "sl_circ": "最小圆形度",
            "btn_ai": "自动优化", "btn_acc": "锁定并叠加",
            "tb_pan": "平移", "tb_roi": "框选", "tb_draw": "补点", "tb_erase": "擦除", "tb_fill": "油漆",
            "rm_pan": "平移画面", "rm_roi": "框选芯片", "rm_draw": "绘制补点", "rm_erase": "擦除修改", "rm_fill": "智能填满",
            "sl_brush": "画笔尺寸", "chk_solid": "强制填补内部孔洞", "sl_gap": "缝隙密合度", 
            "chk_labels": "显示各气泡编号与占比",
            "btn_undo": "撤销", "btn_clear": "清空所有修改",
            "chk_mask": "显示红光", "sl_opacity": "遮罩透明度", "chk_wm": "存档加入水印",
            "status_ready": "✔️ 系统就绪", "void_lbl": "Void Rate : {0:.2f} %",
            "guide_txt": zh_cn_guide
        },
        "en": {
            "title_default": "X-ray void cal v4.0",
            "m_file": "File (F)", "m_lang": "Language (L)", "m_help": "Help (H)",
            "m_open": "Open Image...", "m_load": "Load Project...", "m_save": "Save Project...", "m_export": "Export Report...", "m_close": "Exit", "m_guide": "User Guide",
            "tab_img": "Image", "tab_void": "Detect", "tab_edit": "Edit",
            "p1_title": "Image Preprocessing", "p2_title": "Detection Parameters", "p3_title": "Edit & Masking Controls", "p4_title": "Data Analysis",
            "chk_inv": "Invert (Negative)", "chk_clahe": "Enhance (CLAHE)",
            "sl_destripe": "De-stripe (Bilateral)", "sl_clahe_limit": "CLAHE Limit",
            "sl_zoom": "Zoom", "sl_sharp": "Sharpen", "sl_alpha": "Contrast", "sl_gamma": "Gamma",
            "sl_kernel": "Kernel Size", "sl_thresh": "Sensitivity", "sl_morph": "Smooth Edges", "sl_area": "Min Area", "sl_circ": "Min Circularity",
            "btn_ai": "Auto Optimize", "btn_acc": "Lock & Add",
            "tb_pan": "Pan", "tb_roi": "ROI", "tb_draw": "Draw", "tb_erase": "Erase", "tb_fill": "Fill",
            "rm_pan": "Pan View", "rm_roi": "Select ROI", "rm_draw": "Draw (+)", "rm_erase": "Erase (-)", "rm_fill": "Smart Fill",
            "sl_brush": "Brush Size", "chk_solid": "Solidify Holes", "sl_gap": "Close Gaps",
            "chk_labels": "Show Void Labels & %",
            "btn_undo": "Undo", "btn_clear": "Clear All",
            "chk_mask": "Show Mask", "sl_opacity": "Opacity", "chk_wm": "Add Watermark",
            "status_ready": "✔️ Ready", "void_lbl": "Void Rate : {0:.2f} %",
            "guide_txt": en_guide
        },
        "ja": {
            "title_default": "X-ray void cal v4.0",
            "m_file": "ファイル (F)", "m_lang": "言語 (L)", "m_help": "ヘルプ (H)",
            "m_open": "画像を開く...", "m_load": "プロジェクト読込 (.vod)...", "m_save": "プロジェクト保存 (.vod)...", "m_export": "レポート出力 (.jpg)...", "m_close": "閉じる", "m_guide": "操作ガイド",
            "tab_img": "画像", "tab_void": "ボイド", "tab_edit": "編集",
            "p1_title": "画像状態と前処理", "p2_title": "ボイド検出パラメータ", "p3_title": "手動編集と表示制御", "p4_title": "検出データ分析",
            "chk_inv": "ネガポジ反転", "chk_clahe": "コントラスト強調 (CLAHE)",
            "sl_destripe": "平滑化 (Bilateral)", "sl_clahe_limit": "CLAHE 強度",
            "sl_zoom": "ズーム", "sl_sharp": "シャープネス", "sl_alpha": "明るさ/コントラスト", "sl_gamma": "ガンマ補正",
            "sl_kernel": "抽出範囲 (Kernel)", "sl_thresh": "検出感度", "sl_morph": "エッジ平滑化", "sl_area": "最小ボイド面積", "sl_circ": "最小円形度",
            "btn_ai": "自動最適化", "btn_acc": "ロックして追加",
            "tb_pan": "パン", "tb_roi": "選択枠", "tb_draw": "描画", "tb_erase": "消去", "tb_fill": "塗りつぶし",
            "rm_pan": "画面をパン", "rm_roi": "チップを選択", "rm_draw": "ボイドを描画", "rm_erase": "編集を消去", "rm_fill": "スマート塗りつぶし",
            "sl_brush": "ブラシサイズ", "chk_solid": "内部の穴を強制的に埋める", "sl_gap": "隙間密着度", 
            "chk_labels": "各ボイドの番号と割合を表示",
            "btn_undo": "元に戻す", "btn_clear": "すべての変更をクリア",
            "chk_mask": "マスクを表示", "sl_opacity": "不透明度", "chk_wm": "透かしを保存",
            "status_ready": "✔️ システム準備完了", "void_lbl": "Void Rate : {0:.2f} %",
            "guide_txt": ja_guide
        },
        "ko": {
            "title_default": "X-ray void cal v4.0",
            "m_file": "파일 (F)", "m_lang": "언어 (L)", "m_help": "도움말 (H)",
            "m_open": "이미지 열기...", "m_load": "프로젝트 불러오기 (.vod)...", "m_save": "프로젝트 저장 (.vod)...", "m_export": "보고서 내보내기 (.jpg)...", "m_close": "닫기", "m_guide": "사용자 가이드",
            "tab_img": "이미지", "tab_void": "보이드", "tab_edit": "편집",
            "p1_title": "이미지 상태 및 전처리", "p2_title": "보이드 감지 매개변수", "p3_title": "수동 편집 및 뷰 제어", "p4_title": "감지 데이터 분석",
            "chk_inv": "이미지 반전", "chk_clahe": "대비 강화 (CLAHE)",
            "sl_destripe": "줄무늬 평활화 (Bilateral)", "sl_clahe_limit": "CLAHE 강도",
            "sl_zoom": "확대/축소", "sl_sharp": "선명도", "sl_alpha": "밝기/대비", "sl_gamma": "감마 보정",
            "sl_kernel": "추출 범위 (Kernel)", "sl_thresh": "감지 감도", "sl_morph": "가장자리 평활화", "sl_area": "최소 보이드 면적", "sl_circ": "최소 원형도",
            "btn_ai": "자동 최적화", "btn_acc": "잠금 및 추가",
            "tb_pan": "이동", "tb_roi": "영역 선택", "tb_draw": "그리기", "tb_erase": "지우기", "tb_fill": "채우기",
            "rm_pan": "화면 이동", "rm_roi": "칩 영역 선택", "rm_draw": "보이드 그리기", "rm_erase": "편집 지우기", "rm_fill": "스마트 채우기",
            "sl_brush": "브러시 크기", "chk_solid": "내부 구멍 강제 채우기", "sl_gap": "틈새 닫기", 
            "chk_labels": "각 보이드 번호 및 비율 표시",
            "btn_undo": "실행 취소", "btn_clear": "모든 변경 지우기",
            "chk_mask": "마스크 표시", "sl_opacity": "불투명도", "chk_wm": "워터마크 저장",
            "status_ready": "✔️ 시스템 준비 완료", "void_lbl": "Void Rate : {0:.2f} %",
            "guide_txt": ko_guide
        },
        "fr": {
            "title_default": "X-ray void cal v4.0",
            "m_file": "Fichier (F)", "m_lang": "Langue (L)", "m_help": "Aide (H)",
            "m_open": "Ouvrir l'image...", "m_load": "Charger le projet (.vod)...", "m_save": "Enregistrer le projet (.vod)...", "m_export": "Exporter le rapport (.jpg)...", "m_close": "Fermer", "m_guide": "Guide de l'utilisateur",
            "tab_img": "Image", "tab_void": "Vides", "tab_edit": "Édition",
            "p1_title": "Prétraitement de l'image", "p2_title": "Paramètres de détection", "p3_title": "Contrôles d'édition manuelle", "p4_title": "Analyse des données",
            "chk_inv": "Inverser l'image", "chk_clahe": "Améliorer le contraste (CLAHE)",
            "sl_destripe": "Lissage (Bilateral)", "sl_clahe_limit": "Limite CLAHE",
            "sl_zoom": "Zoom", "sl_sharp": "Netteté", "sl_alpha": "Luminosité/Contraste", "sl_gamma": "Correction Gamma",
            "sl_kernel": "Taille du noyau", "sl_thresh": "Sensibilité", "sl_morph": "Lisser les bords", "sl_area": "Surface min.", "sl_circ": "Circularité min.",
            "btn_ai": "Optimisation Auto", "btn_acc": "Verrouiller & Ajouter",
            "tb_pan": "Déplacer", "tb_roi": "Sélection", "tb_draw": "Dessiner", "tb_erase": "Effacer", "tb_fill": "Remplir",
            "rm_pan": "Déplacer la vue", "rm_roi": "Sélectionner la puce", "rm_draw": "Dessiner des vides", "rm_erase": "Effacer l'édition", "rm_fill": "Remplissage intelligent",
            "sl_brush": "Taille du pinceau", "chk_solid": "Remplir les trous internes", "sl_gap": "Fermer les espaces", 
            "chk_labels": "Afficher numéros et pourcentages",
            "btn_undo": "Annuler", "btn_clear": "Tout effacer",
            "chk_mask": "Afficher le masque", "sl_opacity": "Opacité", "chk_wm": "Ajouter un filigrane",
            "status_ready": "✔️ Système prêt", "void_lbl": "Void Rate : {0:.2f} %",
            "guide_txt": fr_guide
        },
        "de": {
            "title_default": "X-ray void cal v4.0",
            "m_file": "Datei (F)", "m_lang": "Sprache (L)", "m_help": "Hilfe (H)",
            "m_open": "Bild öffnen...", "m_load": "Projekt laden (.vod)...", "m_save": "Projekt speichern (.vod)...", "m_export": "Bericht exportieren (.jpg)...", "m_close": "Schließen", "m_guide": "Benutzerhandbuch",
            "tab_img": "Bild", "tab_void": "Hohlräume", "tab_edit": "Bearbeiten",
            "p1_title": "Bildvorverarbeitung", "p2_title": "Erkennungsparameter", "p3_title": "Manuelle Bearbeitung", "p4_title": "Datenanalyse",
            "chk_inv": "Bild umkehren", "chk_clahe": "Kontrast verbessern (CLAHE)",
            "sl_destripe": "Glättung (Bilateral)", "sl_clahe_limit": "CLAHE Limit",
            "sl_zoom": "Zoom", "sl_sharp": "Schärfen", "sl_alpha": "Helligkeit/Kontrast", "sl_gamma": "Gamma-Korrektur",
            "sl_kernel": "Kernelgröße", "sl_thresh": "Empfindlichkeit", "sl_morph": "Kanten glätten", "sl_area": "Min. Fläche", "sl_circ": "Min. Zirkularität",
            "btn_ai": "Auto-Optimierung", "btn_acc": "Sperren & Hinzufügen",
            "tb_pan": "Verschieben", "tb_roi": "Auswahl", "tb_draw": "Zeichnen", "tb_erase": "Radieren", "tb_fill": "Füllen",
            "rm_pan": "Ansicht verschieben", "rm_roi": "Chip auswählen", "rm_draw": "Hohlräume zeichnen", "rm_erase": "Bearbeitung löschen", "rm_fill": "Intelligentes Füllen",
            "sl_brush": "Pinselgröße", "chk_solid": "Interne Löcher füllen", "sl_gap": "Lücken schließen", 
            "chk_labels": "Nummern & Prozentsätze anzeigen",
            "btn_undo": "Rückgängig", "btn_clear": "Alles löschen",
            "chk_mask": "Maske anzeigen", "sl_opacity": "Deckkraft", "chk_wm": "Wasserzeichen speichern",
            "status_ready": "✔️ System bereit", "void_lbl": "Void Rate : {0:.2f} %",
            "guide_txt": de_guide
        }
    }
    
    return i18n