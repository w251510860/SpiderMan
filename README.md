# 医疗爬虫


## 项目介绍
本爬虫包含: 
- 医院招标采购爬虫(/SpiderMan/procurement)
- 医疗保障局通知公告(/SpiderMan/medical)
- 领导人简历(/SpiderMan/redume) 

## 开发环境
> Window、Linux、OSx、Python3.6+

## 部署环境
> Ubuntu、CentOs

## 环境配置
```shell
# 下载python包
pip install -r requirements.txt

# 配置环境变量(根据本机数据库配置)
echo ENVIRONMENT=prod >> .env
echo LOG_LEVEL=WARNING >> .env
echo MONGO_HOST=127.0.0.1 >> .env
echo MONGO_PORT=27017 >> .env
echo MONGO_DB=Spider >> .env
echo MONGO_COLL=treasure >> .env
echo MONGO_USER=admin >> .env
echo MONGO_PSW=123456 >> .env
```

## 测试
> 文件内启动: /SpiderMan/debug.py
> 
> 命令行启动: scrapy crawl [SpiderName]

## 文件介绍
> medical、procurement、resume ———— 爬虫文件
> 
> pipeline、pipelines.py  ———— 管道文件
> 
> utils   ———— 一些杂项，脚手架
> 
> items.py   ———— 用于声明进入管道的数据（暂时未用到）
> 
> middlewares.py   ———— 中间件
> 
> settings.py   ———— 配置文件
> 


## 抓取字段
```
crawl_time # 抓取时间
hospital_name  # 医院名称
title  # 标题
ori_url  # 源文连接
release_date  # 发布时间
annex_link  # 附件链接（正文包含附件时）
annex_title  # 附件标题（正文包含附件时）
img_link  # 图片链接（正文是一张图片时）
img_title  # 图片标题（正文是一张图片时）
mainbody  # 内容主题（正文时文本时）
mainbody_table  # 内容表格（正文时文本时）
others  # 其他
```