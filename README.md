ORC人機界面（GUI of Organic Rankine Cycle experiment）
===

# ORC簡介【LAB429】

ORC（Organic Rankine Cycle，有機朗肯循環）是一種利用低溫熱能發電的技術。它使用有機流體來轉換低溫熱能為電力或軸功率。ORC常用於處理工廠廢熱、地熱、太陽能等低溫熱能資源。它具有高效能的能源回收和幾乎無環境污染的特點。

通俗地說，ORC是一種將低溫熱能轉化為電力的小型發電裝置。它的發電量一般可以達到幾十KW到數MW左右。而我們實驗室的機組為實驗性機組，發電量約為300W到30KW。

# 開發人機界面的動機

在實驗室內，我們需要使用溫度感測器、壓力傳感器、流量計等感測器，來觀察系統內部的變化。在熱力學中，只要我們知道兩個獨立的熱力性質，便能推估該點的其他性質，並藉此推估系統原件的熱量、作功以及系統效率等等，並在實驗結束後進行數據分析。

過去我們實驗室所使用的量測設備是Keysight Agilent多功能數據擷取器（型號：34972A）。雖然Keysight公司的數據擷取器本身附帶BenchLink DataLogger數據擷取軟體，但該軟體本身並無法直接幫助我們分析熱力相關資訊。

# 開發人機界面的目標

為了滿足我們的需求，決定自行開發一個專用的軟體。（其實是懶得做實驗，所以想開發一個自動記錄數據的軟體。

這個軟體將能夠有效地分析溫度、壓力和流量等感測器所收集的數據，並根據熱力學原理計算出系統原件的功率輸出和系統效率等重要指標。透過這個軟體，我們能夠更準確地評估系統的性能，優化能源使用並進行實驗數據的深入分析。

此外，這個軟體還能幫助我們更輕鬆地了解系統的運作情況。當系統可能出現異常時，它能提供告警通知甚至自動化控制系統，從而降低實驗的危險性。

P.s. 儘管我們製造的是小型實驗機組，但在實驗的過程中，系統壓力會超過10 bar，可以說其實具有一定危險性。

→ 如果想看系統分析圖，您可以查看doc底下的SA文件，這裡有最終系統的目標。

BenchLink DataLogger 界面

<img src="https://about.keysight.com/en/newsroom/imagelibrary/2007/27nov-em07182/image002.jpg" width=600>

# 開法想法
開發的概念是利用CoolProp作為熱力性質的參考工具，透過該函數庫可以快速且準確地獲取各種熱力學參數。接著，使用Matplotlib繪製溫度-熵圖，以視覺化方式展示系統的熱力狀態和變化趨勢。這些資訊將整合至Tkinter界面中，提供給實驗人員或客戶便捷的查看和分析功能。

同時，系統的數據將以Excel或資料庫的方式儲存，以確保資料的保存和追蹤。軟體將自動計算並記錄系統的性能指標，方便實驗人員進行後續的數據分析和評估。

# 人機界面的演化
## 文字人機界面
<img src="https://i.imgur.com/WkaT3ie.gif" width=600>

---

## 圖形化人機界面
<img src="https://i.imgur.com/xjsiQjV.gif" width=600>

----

### 功能演示

#### 圖形縮放(確認熱力性質)
<img src="https://i.imgur.com/eCM2ihM.gif" width=600>

#### 回到預設窗格
<img src="https://i.imgur.com/z0DgOoR.gif" width=600>

#### 圖形拖曳
<img src="https://i.imgur.com/MdPVlBO.gif" width=600>


#### 圖片儲存
<img src="https://i.imgur.com/KnF5pWO.gif" width=600>

#### 人機界面概況(系統關機操作)
<img src="https://i.imgur.com/RWtwKMi.gif" width=600>

---

# refprop 嵌入 excel 

以下影片時長過長，使用youtube上傳影片，須點擊播放。


## 利用excel查熱力性質
{%youtube erQ5wYSyNTs %}
https://youtu.be/erQ5wYSyNTs

## excel vba 擷取實驗穩態數據 (自動化)

### Part A
{%youtube ZjbVMBE1Hzk %}
https://youtu.be/ZjbVMBE1Hzk

### Part B
{%youtube WznF8XCsUu0 %}
https://youtu.be/WznF8XCsUu0

---

# Installing / Getting started
* [Requirements](#requirements)
* [Install](#install)
* [Run GUI](#run-gui)
* [Other](#other)
  * [How to pack executable file by yourself](#how-to-pack-executable-file-by-yourself)

## Requirements
**Using pipenv(I use it!)**
* Python 3.x
* pipenv

Do not use pipenv(you can check the pipfile, what package you should install)
* Python 3.x
* pyvisa = 1.11.3
* matplotlib = 3.3.3
* coolprop = 6.4.1
* tabulate = 0.8.7

BTW, the Operating System and Python I use, as shown in the table below.
Of course you can also try other environments.
OS           | Python |
-------------|:------:|
Windows 10   | 3.6.8  |
Ubuntu 18.04 | 3.6.9  |

## Install
* clone the project
* Enter the `GUI-of-Organic-Rankine-Cycle-experiment` folder
* Use pipenv install package from pipfile

```
$ git clone https://github.com/t104306033/GUI-of-Organic-Rankine-Cycle-experiment.git
$ cd GUI-of-Organic-Rankine-Cycle-experiment
$ pipenv install 
OR
$ pipenv install --ignore-pipfile
```

Check whether the installation is successful, you can try to execute the following command.

```
$ pipenv run pip list
Package            Version
------------------ --------
CoolProp           6.4.1
cycler             0.10.0
dataclasses        0.8
importlib-metadata 4.6.1
kiwisolver         1.3.1
matplotlib         3.3.4
numpy              1.19.5
Pillow             8.3.1
pip                21.1.3
pipfile            0.0.2
pyparsing          2.4.7
python-dateutil    2.8.2
PyVISA             1.11.3
setuptools         57.0.0
six                1.16.0
tabulate           0.8.9
toml               0.10.2
typing-extensions  3.10.0.0
wheel              0.36.2
zipp               3.5.0
```

## Run GUI
Run GUI.py via python in pipenv, you can getting started.

```
$ pipenv run python GUI.py
```

**If you get a runtime error, you can try to modify config.json**

## Setup config.json(待補！)

# Other
## How to pack executable file by yourself
* Follow the steps of the installation guide
* Install pyinstaller via pip
* Using pyinstaller to pack GUI.spec
* Enter into pack folder
* run executable file

```
$ pipenv run pip install pyinstaller
$ pipenv run pyinstaller GUI.spec
$ cd dist
$ ./GUI.exe
```
