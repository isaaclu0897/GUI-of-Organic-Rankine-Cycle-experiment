ORC人機界面與excel資料處理
===

# ORC簡介
ORC（Organic Rankine Cycle，有機朗肯循環）發電技術，是利用低溫沸點有機工作流體的熱機循環系統，將工廠廢熱、地熱、太陽等低溫熱能轉換為電力或軸功率輸出的一種作功裝置。

# 開發人機界面的動機
在實驗室內，我們需要利用溫度感測器、壓力傳感器、流量計等感測器，已觀察系統內部發生的變化。在熱力學中，我們只要知道兩個獨立的熱力性質，便能推估該點的其他性質，並藉此推估系統元件的作功以及系統效率等等，並在實驗結束後分析數據。

以往本實驗室量測設備採用的是 keysight agilent 多功能數據擷取器(型號:34972A)，雖然keysight公司的數據擷取器本身付有 BenchLink DataLogger 數據擷取軟體。但其軟體本身並無法幫助本實驗室分析熱力方面的資訊。因此敝人我決定自己寫一個。

# 開法想法
開發的概念是利用 coolprop 進行熱力性質的參照，接著利用 matplotlib 可繪製溫度-熵圖，並將此類資訊整合至 tkinter 中，並顯示給實驗人員或客戶知曉。並且將系統的訊系以 excel儲存下來，並自動計算其結果，以便實驗人員的後續分析。



# 人機界面的演化
文字人機界面

<img src="https://i.imgur.com/WkaT3ie.gif" width=500>

---

圖形化人機界面

<img src="https://i.imgur.com/xjsiQjV.gif" width=500>

----

功能演示

圖形縮放(確認熱力性質)

<img src="https://i.imgur.com/eCM2ihM.gif" width=500>

回到預設窗格

<img src="https://i.imgur.com/z0DgOoR.gif" width=500>

圖形拖曳

<img src="https://i.imgur.com/MdPVlBO.gif" width=500>


圖片儲存

<img src="https://i.imgur.com/GQlgyDj.gif" width=500>

人機界面概況(系統關機操作)

<img src="https://i.imgur.com/RWtwKMi.gif" width=500>

---

refprop嵌入excel


excel vba 巨集自動化(擷取實驗穩態數據)
