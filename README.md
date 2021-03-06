# PINGJIAO tool for Sichuan University
> All of this project is based on **Django1.9.5+** and **Python3.5.1+**, and the completion of HFF is Web App for Fun
> So, if you like it, welcome to star it

## Download Realease
> how to run：[Method 2nd](#run)

[ScuPingjiao](https://pan.baidu.com/s/1pKD6nRP)

## Apps
> List all apps at here

1. **pingjiao**: *this app is used to make comments for our teachers convenient*

## Note

Website has been closed for no money!!! if you wanna know how to implement it, you can read `SCU_Pingjiao/HFF/pingjiao/pj_tools`.

## How to execute?

### Method 1st:

> If your computer has a `Python3` environment, and `httplib2`, `bs4` all has been installed in your environment, you can use this method

launch `SCU_Pingjiao/HFF/pingjiao/action.py` in command line.

help: `python3 action.py [username] [password]`

example: 

```shell
python3 action.py 2014141462345 123456
```

<h3 id="run">Method 2nd</h3>

> If your computer has not a `Python3` environment, you can run `ScuPingjiao` (locates at `SCU_Pingjiao/ScuPingjiao` ) in your command line like this:

```shell
./ScuPingjiao [username] [password]
```

example:

```shell
./ScuPingjiao 2014141462345 123456
```

## What will you see like

```bash
余方姝, 研究生助教评价, 编译原理 评教完成！
余方姝, 研究生助教评价, 编译原理课程设计 评教完成！
傅静涛, 学生评教, 网络工程 评教完成！
朱敏, 学生评教, 数据可视化 评教完成！
潘薇, 学生评教, 编译原理 评教完成！
潘薇, 学生评教, 编译原理课程设计 评教完成！
卢晓春, 学生评教, 模式识别引论 评教完成！
叶庆, 学生评教, 形势与政策-6 评教完成！
张磊, 学生评教, 云计算 评教完成！
游思兰, 研究生助教评价, 数据可视化 评教完成！
刘琪琪, 研究生助教评价, 云计算 评教完成！
===Done!===
```
