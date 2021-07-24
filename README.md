ORC人機界面與excel資料處理（GUI of Organic Rankine Cycle experiment）
===

# ORC簡介【LAB429】
ORC（Organic Rankine Cycle，有機朗肯循環）發電技術，是利用低溫沸點有機工作流體的熱機循環系統，將工廠廢熱、地熱、太陽等低溫熱能轉換為電力或軸功率輸出的一種作功裝置。

# 開發人機界面的動機
在實驗室內，我們需要利用溫度感測器、壓力傳感器、流量計等感測器，已觀察系統內部發生的變化。在熱力學中，我們只要知道兩個獨立的熱力性質，便能推估該點的其他性質，並藉此推估系統元件的作功以及系統效率等等，並在實驗結束後分析數據。

以往本實驗室量測設備採用的是 keysight agilent 多功能數據擷取器(型號:34972A)，雖然keysight公司的數據擷取器本身付有 BenchLink DataLogger 數據擷取軟體。但其軟體本身並無法幫助本實驗室分析熱力方面的資訊。因此敝人我決定自己寫一個。

BenchLink DataLogger 界面

<img src="https://about.keysight.com/en/newsroom/imagelibrary/2007/27nov-em07182/image002.jpg" width=600>

# 開法想法
開發的概念是利用 coolprop 進行熱力性質的參照，接著利用 matplotlib 可繪製溫度-熵圖，並將此類資訊整合至 tkinter 中，並顯示給實驗人員或客戶知曉。並且將系統的訊系以 excel儲存下來，並自動計算其結果，以便實驗人員的後續分析。



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
* [Requirements](#Requirements)
  * [Install](#Install)
  * [Run GUI](#Run-GUI)
* [Other](#Other)
  * [How to pack executable file by yourself](#How to pack executable file by yourself)

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
$ pipenv install Pipfile
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
