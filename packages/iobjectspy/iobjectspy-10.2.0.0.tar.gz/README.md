# SuperMap iObjects Python ( iObjectsPy ) 10.2.0 版本      

## 1 简介

iObjectsPy 是 SuperMap iObjects Python 的简称。通过 iObjectsPy，用户可以直接使用 Python 语言操作 SuperMap 各种空间数据。

iObjectsPy 提供空间数据导入导出、投影转换、地图制图、矢栅数据处理与分析、空间统计分析、机器学习等功能，帮助用户使用脚本进行空间数据快速处理和分析。


## 2 功能模块结构
* `data` 模块支持数据创建、管理和组织，包括工作空间、数据源、数据集、记录集、要素对象、几何对象等的创建和管理。
* `enums` 模块提供基本的枚举对象，包括数据源引擎类型、数据集类型等。
* `env` 模块提供全局参数设置，包括空间分析和数据处理使用大内存模式, 设置并行线程数等。
* `conversion` 模块支持常用数据格式导入和导出操作，包括 shp、mif、cad等矢量数据，tif、img、png等栅格和影像数据。导入矢量数据和栅格数据到 SuperMap 数据源，以及将 SuperMap 数据源导出为外部矢量数据或栅格数据等功能。
* `analyst` 模块支持空间数据处理和分析的能力，包括缓冲区分析、叠加分析等矢量数据处理与分析方法，密度分析、插值分析等栅格数据处理与分析方法，空间自相关、空间热点、空间抽样、空间回归等空间统计分析方法，以及二维、三维网络分析方法等。

* `ml` 模块支持AI GIS相关能力，包括地址要素识别，倾斜摄影建筑物底面提取，影像数据目标检测、二元分类、地物分类、场景分类、对象提取，图片数据目标检测、图片分类，图时空回归功能；支持数据集（Dataset）与numpy、pandas的转换；支持基于深度学习的人工智能GIS完整工作流程，包括支持样本数据制作、模型训练、模型推理、模型评估。


## 3 产品包结构

### 3.1. iobjectspy 目录

库文件所在目录

### 3.2 examples 目录

范例程序源码，供用户了解熟悉接口使用方式，根据功能模块分别提供以下几部分示例：

`analyst`:矢量、栅格、空间统计等空间分析示例代码（包括地址匹配、密度聚类、栅格裁剪、密度分析、叠加分析等）。  
`data`：数据导入、导出等示例代码  
`map`：地图相关示例代码

### 3.3 data 目录

范例数据，供范例程序使用：  
`Address.udbx`：供范例程序地址匹配功能使用的UDBX数据源

`China400.udbx`：供范例程序密度聚类功能使用的UDBX数据源

`example_data.udbx`：供范例程序共用的UDBX数据源  

`example_dbscan.udbx`：供范例程序密度聚类功能使用的UDBX数据源

`mapmatching.udbx`：供范例程序地图匹配功能使用的UDBX数据源

`tracks.udbx`：供范例程序example_dataset_convertor.py 数据集类型转换功能使用的UDBX数据源

`world.udbx`：供范例程序拓扑构面功能使用的UDBX数据源

`County_p.shp`：供数据导入使用的矢量数据文件

`multibands.img`：供数据导入使用的影像数据文件

`dem.npy`：供NumPy数据交互使用的NumPy文件

### 3.4 doc 目录

Python接口说明，供开发人员查阅.

### 3.5 lib 目录

包含SuperMap iObjects Python 产品功能依赖的 SuperMap iObjects Java 组件包 objectsjava 。

### 3.6 licenses 目录

 提供机器学习功能开源代码的许可。

### 3.7 AI依赖文件

如需使用AI相关功能，需要通过conda建立虚拟环境在线安装相关依赖:

如需使用CPU进行深度学习（默认）:

    conda env create -f requirements-conda-cpu.yml

如需使用GPU进行深度学习（性能更优）, 需自行安装 CUDA 10.1 及对应 cuDNN，并建议安装（更新）最新显卡驱动:

    conda env create -f requirements-conda-gpu.yml



## 4 产品安装


## 4.1 支持环境
[Python](https://www.python.org/) 3.5+

[SuperMap iObjects Java](http://support.supermap.com.cn/DownloadCenter/ProductPlatform.aspx) 10.2.0

## 4.2 许可说明

### 4.2.1 普通许可
SuperMap iObjects Python 使用 SuperMap GIS 10i 系列产品许可用于验证产品的可用性。针对 Windows 平台，提供 SuperMap 许可中心（SuperMap License Center）对许可进行配置和管理；在 Linux 平台，提供命令行方式配置许可。

在 Windows 和 Linux 操作系统下，SuperMap GIS 10i 系列产品均提供两种许可：试用许可和正式许可，其中正式许可又分为软许可和硬件许可。

**试用许可**
SuperMap GIS 10i 系列产品默认提供了90天的试用许可，您也可以在线申请试用许可，申请地址：https://www.supermapol.com/web/pricing/triallicense

用户只要安装了 SuperMap GIS 10i 系列产品，并在 Windows 平台部署 SuperMap 许可中心，或在 Linux 平台安装许可驱动 ，就可以查看到对应的产品的试用许可状态。
　　

**正式许可**
正式许可的提供形式有两种：软许可和硬件许可。

1. 软许可，是以离线或在线方式获得合法的软件运行许可，激活到本机，即可生效。软许可分为单机软许可和网络软许可。如果激活单机软许可，则只能为本机提供许可服务；如果激活网络软许可，则可以为当前网络中的计算机提供许可服务。注意，在许可服务器上激活网络软许可后，无法转移该网络软许可。

2. 硬件许可，是以硬件加密锁（简称“硬件锁”）的形式获得合法的软件运行许可。

您可以联系相关销售人员购买正式许可。

### 4.2.2 Web许可
SuperMap GIS 产品从10i 系列开始支持 Web 许可，Web许可是一种适配云环境的许可方式。要使用 Web 许可，您需要连接到可用的 Web 版许可中心。在连接到 Web 版许可中心后，通过 Web 版许可中心授权获得许可。

**许可获取方式**
正式版 Web 许可请联系销售获取，试用版许可可以在线申请获取，申请地址：https://www.supermapol.com/web/pricing/triallicense。  

**使用 Web 许可**
1. 配置 Web 版许可中心
您可以从超图技术资源中心下载 Web 版许可中心的安装包，地址为 http://support.supermap.com.cn/DownloadCenter/ProductPlatform.aspx。
Web 版许可中心安装包中提供的 Readme 文档将为您介绍 Web 版许可中心安装和使用的流程，您可以参照该文档安装和使用 Web版许可中心。
2. 启用 Web 许可
Web 许可的激活在 Web 版许可中心进行，具体请参考 Web 版许可中心产品包中的 Readme 文档。
3. 配置许可环境
在环境变量中配置 BS_LICENSE_SERVER=[本机ip]:9183，如
Linux中
```bash
export BS_LICENSE_SERVER=192.168.3.3:9183
```
windows中
```bash
set BS_LICENSE_SERVER=192.168.3.3:9183
```
代码中
```bash
System.setProperty("BS_LICENSE_SERVER","192.168.3.3:9183")
```
> Note：  
> 1、 激活 Web 许可时，请确认 iObjects Python 所在机器上没有其他的许可（正式许可、试用许可)，如有其他许可将优先使用其他许可。
> 2、 按核许可的拆分/合并：
> 若您使用的是按核计算的运行许可，在连接到许可中心后，许可中心会校验 iObjects Python 所在机器的核数，如果机器的核心数小于/等于 Web 许可中心里可用的按核许可的核心数，则 Web 许可中心将为机器进行许可授权，按核许可的启用参见启用按核许可。授权后，许可中心的按核许可的可用核数会相应少：
> *授权后许可中心的按核许可的可用核数 = 许可中心的按核许可原有可用核数 - 机器核数。*

## 4.3 安装说明
(1) 安装 [Python 3.5.0](https://www.python.org/download) 或以上版本

(2) 执行安装包内的 setup.py 脚本，命令为： python setup.py install

(3) 如需使用AI相关功能，还需要配置机器学习资源包（Machine Learning Resources），并通过 conda 在线安装相关依赖：

- 在官网下载 SuperMap iObjects Python Machine Learning Resources 10i 机器学习资源包，解压到iobjectspy根目录即可。资源包内包含示例模型、示例程序、示例文件、训练配置文件及训练所需的主干网络模型等。

- conda 环境配置：使用`conda env create -f requirements-conda-cpu.yml`建立iobjectspy虚拟环境。
    
    - `requirements-conda-cpu.yml`: 如需使用CPU进行机器学习（默认）
    - `requirements-conda-gpu.yml`: 如需使用GPU进行机器学习（性能更优）

(4) 安装 Java 8 或以上版本

(5) 安装 SuperMap iObjects Java 组件，注意使用与产品包相对应的组件版本，依赖的最低版本为 10.2.0.18927.82297。

- Windows 用户，可以通过以下任一方式配置 SuperMap iObjects Python 使用的 SuperMap iObjects Java 组件（这里的E:\SuperMap\iObjects\Bin_x64可修改为你的java_bin目录）:
  1. 将 SuperMap iObjects Java 组件的 Bin 目录设置到 Path 变量。

  2. 在安装完 SuperMap iObjects Python 后，在 cmd 命令行中执行 "`iobjectspy set-iobjects-java E:\SuperMap\iObjects\Bin_x64`"，通过这种方式，必须确保 Python 的 Scripts 目录在 PATH 环境中，或者直接在 Scripts 目录下执行。

  3. 启动 python 窗口，执行以下代码:

    ```python
    import iobjectspy
    iobjectspy.set_iobjects_java_path(r'E:\SuperMap\iObjects\Bin_x64')
    ```

  
  需要注意的是，通过方式 2 和 3 配置 SuperMap iObjects Java 组件，会将指定的 SuperMap iObjects Java 组件目录配置到 iobjectspy 库目录下的 evn.json 文件中，这样，用户无需多次设置，但在升级 SuperMap iObjects Java 组件版本时，需要再次通过 2 或 3 执行。

- Linux 用户，可以通过以下方式配置 SuperMap iObjects Python 使用的 SuperMap iObjects Java 组件（这里的/home/user/iobjects-java/bin可修改为你的java_bin路径）:

  1. 将 SuperMap iObjects Java 组件的 Bin 直接设置到 `/opt/SuperMap/iobjects/1010/Bin`

  2. 将 SuperMap iObjects Java 组件的 Bin 设置在环境变量中

    - export LD_LIBRARY_PATH=/home/user/iobjects-java/bin:$LD_LIBRARY_PATH

  3. 在安装完 SuperMap iObjects Python 后，在 cmd 命令行中执行 `iobjectspy set-iobjects-java /home/user/iobjects-java/bin`

  4. 启动 python 窗口，执行以下代码::

    ```python
    import iobjectspy
    iobjectspy.set_iobjects_java_path('/home/user/iobjects-java/bin（可修改为你的java_bin路径）')
    ```
  需要注意的是，通过方式 3 和 4 配置 SuperMap iObjects Java 组件，会将指定的 SuperMap iObjects Java 组件目录配置到 iobjectspy 库目录下的 evn.json 文件中，这样，用户无需多次设置，但在升级 SuperMap iObjects Java 组件版本时，需要再次通过 3 或 4 执行。所以需要确保当前操作对 iobjectspy 安装目录有写入权限（可以通过使用 root 用户权限执行命令）。

(6) 完成后，可通过执行examples目录中的示例代码验证是否安装成功。
AI功能的介绍及操作可参考文档：`《SuperMap 10i空间机器学习技术与产品介绍》`

    
## 4.3 在线帮助

在线帮助文档，请参考[http://iobjectspy.supermap.io](http://iobjectspy.supermap.io)


## 5 版本历史

	10.2.0 - 2021-09
    10.1.2 - 2021-03
	10.1.1 - 2020-12
	10.1.0 - 2020-09 
	10.0.1 - 2019-12
	10.0.0 - 2019-10
 	9.1.2 - 2019-05 
	9.1.1 - 2018-12  
	9.1.0 - 2018-09
  