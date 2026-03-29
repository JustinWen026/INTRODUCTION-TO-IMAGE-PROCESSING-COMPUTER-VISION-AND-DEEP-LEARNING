# INTRODUCTION-TO-IMAGE-PROCESSING-COMPUTER-VISION-AND-DEEP-LEARNING
1141_影像處理、電腦視覺及深度學習概論HW1
影像處理、電腦視覺與深度學習 - 作業一

開發環境：Python 3.8 / OpenCV 4.10 / PyQt5 

這作業基於 PyQt5 開發的互動式影像處理工具箱，整合了從基礎色彩轉換到進階邊緣檢測與幾何變換的多項功能 。

功能展示 (Features)

1. 基礎影像處理(Image Processing)

色彩分離 (Color Separation)：使用 cv2.split() 提取 BGR 通道，並透過 cv2.merge() 重建單一色彩通道影像。

色彩轉換 (Color Transformation)：實作 OpenCV 官方 cvtColor 與平均加權法兩種灰階轉換公式。

色彩提取 (Color Extraction)：將影像轉為 HSV 空間，利用 cv2.inRange() 製作遮罩以提取特定顏色區域（如黃綠色）。

2. 影像平滑化 (Image Smoothing)透過互動式 Trackbar 即時調整濾波器參數

高斯濾波 (Gaussian Blur)：基礎降噪處理

雙邊濾波 (Bilateral Filter)：在降噪的同時，考慮像素值差異以有效保留邊緣資訊。

中值濾波 (Median Filter)：針對椒鹽雜訊 (Salt-and-pepper noise) 的有效處理方案。

3. 邊緣檢測 (Edge Detection)手寫 Sobel 算子：不調用 OpenCV 內建函數，自行實作 $3 \times 3$ 的 Sobel X 與 Sobel Y 卷積運算。
  
組合與閾值化：結合雙向梯度強度並進行正規化處理。

梯度角度過濾：計算 $\theta = \arctan(\frac{Sobel_y}{Sobel_x})$，並根據特定角度範圍（如 $170^\circ \sim 190^\circ$）提取邊緣線條。

4. 幾何變換 (Transforms)實作仿射變換 (Affine Transformation)，在單一操作中同時完成旋轉（30度）、縮放（0.9倍）與平移（535, 335 像素）。確保旋轉與縮放時，物體中心座標正確映射 。

5. 自適應閾值 (Adaptive Threshold)

全域閾值 (Global)：設定固定閾值 (80) 進行二值化，但在光照不均的情況下效果有限。

局部自適應閾值 (Local)：根據鄰域像素平均值動態計算閾值，成功處理非均勻光照下的 QR Code 影像 。

使用工具 (Tech Stack)程式語言：Python 影像處理：OpenCV (opencv-contrib-python 4.10.0), Numpy 圖形介面：PyQt5 (UI framework) 資料視覺化：Matplotlib 
