# Tibet_Spider
爬取西藏相关网站的新闻信息。
## 更新
### 2018-09-26
* 新增进度表格，及时更新抓取进度
* 修正爬虫的逻辑错误，目前运行稳定
### 2018-09-27
* 表格中的抓取时间表示的是爬虫启动的时间，有的可能所需时间较长超过一天
## 进度

| 网站名 | 当前状态 | 抓取时间 | 数据量 | 安全机制 |
| :---: | :---: | :---: | :--: | :--: |
| 山南网(snw-spider) | 抓取中 | 2018-09-26 | 未知 | 有 |
| 西藏工会新闻网(xzgh_spider) | 完成 | 2018-10-13 | 8MB | 无 |
| 中国西藏网(xzw_spider) | 完成 | 2018-10-11 | 20MB | 无 |
| 中国西藏新闻网(xzxw_spider) | 完成 | 2018-10-13 | 436MB | 无 |
| 西藏之声(xzzs_spider) | 完成 | 2018-10-11 | 87MB | 无 |
| 西藏在线(xzzx_spider) | 完成 | 2018-10-12 | 48MB | 无 |

## 映射表
记录网站的各字段和对应保存的表情名

### [西藏工会新闻网](http://xz.workercn.cn/)(xzgh_spider)
| 分类 | 链接 | 标签 |
| :--: | :--: | :--: |
| 时政要闻 | [链接](http://xz.workercn.cn/10930/10930.shtml) | 政治 |
| 工会动态 | [链接](http://xz.workercn.cn/10850/10850.shtml) | 保留 |
| 基层工会 | [链接](http://xz.workercn.cn/10858/10858.shtml) | 保留 |
| 西藏风情 | [链接](http://xz.workercn.cn/29369/29369.shtml) | 文化 |
| 社会民生 | [链接](http://xz.workercn.cn/10864/10864.shtml) | 社会 |
| 职工文化 | [链接](http://xz.workercn.cn/29556/29556.shtml) | 保留 |

### [中国西藏网](http://www.tibet.cn/)(xzw_spider)
| 分类 | 目录名 | 链接 | 标签 |
| :--: | :--: | :--: | :--: |
| 新闻 | 原创 | [链接](http://www.tibet.cn/cn/news/yc/) |	保留 |
|     | 资讯 | [链接](http://www.tibet.cn/cn/news/zx/) | 保留 |
|     | 藏区动态 | [链接](http://www.tibet.cn/cn/news/zcdt/) | 保留 |
| 时政 | 时政 | [链接](http://www.tibet.cn/cn/politics/) | 政治 |
| 文化 | 民俗 | [链接](http://www.tibet.cn/cn/culture/ms/) | 文化 |
|     | 工艺 | [链接](http://www.tibet.cn/cn/culture/gy/) | 文化 |
|     | 藏学 | [链接](http://www.tibet.cn/cn/culture/zx/) | 文化 |
|     | 资讯 | [链接](http://www.tibet.cn/cn/culture/wx/) | 保留 |
| 援藏 | 资讯 | [链接](http://www.tibet.cn/cn/aid_tibet/news/) | 保留 |
|     | 人物 | [链接](http://www.tibet.cn/cn/aid_tibet/rw/) |	 保留 |
| 藏医药 | 行业动态 | [链接](http://www.tibet.cn/cn/medicine/news/) | 社会 |
|     | 疾病诊疗 | [链接](http://www.tibet.cn/cn/medicine/jbzl/) | 文化 |
|     | 四季养生 | [链接](http://www.tibet.cn/cn/medicine/sjys/) | 保留 |
| 宗教 | 宗教 | [链接](http://www.tibet.cn/cn/religion/) | 政治 |
| 生态 | 生态 | [链接](http://www.tibet.cn/cn/ecology/) |	保留 |

### [中国西藏新闻网](http://www.xzxw.com/)(xzxw_spider)
| 分类 | 目录名 | 链接 | 标签 |
| :--: | :--: | :--: | :--: |
| 西藏新闻 | 西藏要闻 | [链接](http://www.xzxw.com/xw/xzyw/) |	保留 |
|     | 民生新闻 | [链接](http://www.xzxw.com/xw/msxw/) |	社会 |
|     | 财经新闻 | [链接](http://www.xzxw.com/xw/cjxw/) |	保留 |
|     | 法制西藏 | [链接](http://www.xzxw.com/xw/fzxz/) |	社会 |
|     | 科教文卫 | [链接](http://www.xzxw.com/xw/kjww/) |	保留 |
| 政务要闻 | 政务要闻 | [链接](http://www.xzxw.com/zw/zwyw/) |	政治 |
|     | 新闻发布会 | [链接](http://www.xzxw.com/zw/xwfbh/) |	保留 |
|     | 权威发布 | [链接](http://www.xzxw.com/zw/qwfb/) |	保留 |
|     | 人事任免 | [链接](http://www.xzxw.com/zw/rsrm/) |	保留 |
|     | 政府公告 | [链接](http://www.xzxw.com/zw/zfgg/) |	保留 |
| 九眼时评 | 西藏日报评论 | [链接](http://www.xzxw.com/jysp/xzrbpl/) |	保留 |
|     | 西藏观察 | [链接](http://www.xzxw.com/jysp/xzgc/) | 保留 |
|     | 珠峰快见 | [链接](http://www.xzxw.com/jysp/zfkj/) | 保留 |
| 教育文化 | 教育要闻 | [链接](http://www.xzxw.com/wh/jyyw/) |	文化 |
|     | 考试中心 | [链接](http://www.xzxw.com/wh/kszx/) |	文化 |
|     | 培训导学 | [链接](http://www.xzxw.com/wh/pxdx/) |	文化 |
|     | 人才就业 | [链接](http://www.xzxw.com/wh/rcjy/) |	文化 |
|     | 西藏班 | [链接](http://www.xzxw.com/wh/xzb/) |	文化 |
| 旅游人文 | 资讯空间 | [链接](http://www.xzxw.com/lyrw/zxkj/) | 文化 |
|     | 触摸西藏 | [链接](http://www.xzxw.com/lyrw/cmxz/) | 文化 |
|     | 旅游伴侣 | [链接](http://www.xzxw.com/lyrw/lybl/) | 文化 |
|     | 藏地生活 | [链接](http://www.xzxw.com/lyrw/zdsh/) | 文化 |
|     | 人文笔记 | [链接](http://www.xzxw.com/lyrw/rwbj/) | 文化 |
|     | 西藏艺术 | [链接](http://www.xzxw.com/lyrw/xzys/) | 文化 |
|     | 高原视野 | [链接](http://www.xzxw.com/lyrw/gysy/) | 文化 |
| 公益 | 公益新闻 | [链接](http://www.xzxw.com/gongyi_5554/gyxw/) | 社会 |
|     | 公益动态 | [链接](http://www.xzxw.com/gongyi_5554/dongtai/) | 社会 |
|     | 公益救助 | [链接](http://www.xzxw.com/gongyi_5554/help/) | 社会 |
| 生态环保 | 生态环保 | [链接](http://www.xzxw.com/xw/shengthb/) |	保留 |

### [西藏之声](http://www.vtibet.com/)(xzzs_spider)
| 分类 | 链接 | 标签 |
| :--: | :--: | :--: |
| 要闻 | [链接](http://www.vtibet.com/xw_702/yw_705/) | 保留 |
| 时政 | [链接](http://www.vtibet.com/xw_702/sz_704/) | 政治 |
| 社会 | [链接](http://www.vtibet.com/xw_702/sh_709/) | 社会 |
| 经济 | [链接](http://www.vtibet.com/xw_702/jj_710/) | 保留 |

### [西藏在线](http://www.tibetol.cn/)(xzzx_spider)
| 分类 | 目录名 | 链接 | 标签 |
| :--: | :--: | :--: | :--: |
| 资讯 | 本网原创 | [链接](http://www.tibetol.cn/html/zixun/bwyc/) | 保留 |
|     | 其他藏区 | [链接](http://www.tibetol.cn/html/zixun/qitazangqu/) | 保留 |
|     | 西藏要闻 | [链接](http://www.tibetol.cn/html/zixun/xizangyaowen/) | 保留 |
|     | 相关报道 | [链接](http://www.tibetol.cn/html/zixun/xgbd/) | 文化 |
| 文库 | 藏地往事 | [链接](http://www.tibetol.cn/html/wenzhai/zdws/) | 文化 |
|     | 人与自然 | [链接](http://www.tibetol.cn/html/wenzhai/ryzr/) | 文化 |
|     | 高原民俗 | [链接](http://www.tibetol.cn/html/wenzhai/gyms/) | 文化 |
|     | 雪域文化 | [链接](http://www.tibetol.cn/html/wenzhai/yxwh/) | 文化 |
|     | 圣地之旅 | [链接](http://www.tibetol.cn/html/wenzhai/sdzl/) | 文化 |
|     | 文物考古 | [链接](http://www.tibetol.cn/html/wenzhai/wwkg/) | 文化 |
|     | 学术理论 | [链接](http://www.tibetol.cn/html/wenzhai/wxxs/) | 文化 |
|     | 古今人物 | [链接](http://www.tibetol.cn/html/wenzhai/gjrw/) | 文化 |
| 读书 | 书讯 | [链接](http://www.tibetol.cn/html/dushu/sx/) | 文化 |
|     | 书评 | [链接](http://www.tibetol.cn/html/dushu/sp/) | 文化 |


## 当前任务
文化、政治、社会-> train.json

保留-不需要的：
* 西藏工会网：工会动态、基层工会、职工文化
* 中国西藏新闻网：人事任免、权威发布、新闻发布会、政府公告、生态环保
* 中国西藏网：生态
* 西藏之声：经济

关键字需要一个合集（无重复的