
开发环境： Anaconda3(64-bit) Scrapy

IDE :PyCharm

参考网文:

http://studyai.site/2016/11/30/%E6%88%BF%E4%BB%B7%E9%A2%84%E6%B5%8B%EF%BC%881%EF%BC%89-%E6%90%9C%E6%88%BF%E7%BD%91%E6%95%B0%E6%8D%AE%E7%88%AC%E5%8F%96/

http://studyai.site/2016/11/30/%E6%88%BF%E4%BB%B7%E9%A2%84%E6%B5%8B%EF%BC%881%EF%BC%89-%E6%90%9C%E6%88%BF%E7%BD%91%E6%95%B0%E6%8D%AE%E7%88%AC%E5%8F%96/

http://studyai.site/2016/12/15/%E6%88%BF%E4%BB%B7%E9%A2%84%E6%B5%8B%EF%BC%883%EF%BC%89-%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96/

代码执行:

crapy crawl degreeroom

R 展现:

library(mongolite)

con <- mongo("soufang",url="mongodb://192.168.59.105:27017/soufang")

mydata <- con$find()

barplot(table(x<-as.numeric(mydata$total)))

plot(x<-as.numeric(mydata$mian_ji),y<-as.numeric(mydata$total_price),xlab = "面积",ylab = "总价")

pie(table(mydata$hu_xin))

pie(table(mydata$xiao_qu))

pie(table(mydata$xue_xiao))

barplot(table(mydata$publish_date))

boxplot(as.numeric(mydata$total_price)/as.numeric(mydata$mian_ji),ylim=c(0.7,2.5))

con_gb_publis_time <- mongo("soufang_gb_publish_time", url = "mongodb://192.168.59.105:27017/soufang")

myGbData <- con_gb_publis_time$find(sort='{"publish_date":-1}')

barplot(height=as.numeric(myGbData$avg),table(myGbData$publish_date))

plot(x<-as.numeric(gsub('-','',myGbData$publish_date)),y<-as.numeric(myGbData$avg),type="o")

library(sqldf)
newdata2 <-sqldf::sqldf("select * from mydata where xue_xiao='市桥中心小学'")

newdata3 <-sqldf::sqldf("select xue_xiao,avg(total_price/mian_ji) from mydata group by xue_xiao")
newdata3

newdata4 <-sqldf::sqldf("select xue_xiao,count(*) from mydata group by xue_xiao")
newdata4


#write.csv(mydata, file="D:/bear.csv")

#mydata$unit_price=as.numeric(mydata$total_price)/as.numeric(mydata$mian_ji)

mydata$hu_xin_new=substr(mydata$hu_xin,1,4) 

attach(mydata)

tapply(unit_price,list(xiao_qu,hu_xin),mean)

detach(mydata)



---阿里云建表脚本----------------------------------------------------------------------------------------
CREATE TABLE t_degreeroom

(

id STRING COMMENT 'id',

url STRING COMMENT 'url'    ,

title STRING COMMENT '标题',

total_price STRING COMMENT '总价(单位:万)',

hu_xin STRING COMMENT '户型',

mian_ji STRING COMMENT '面积',

unit_price STRING COMMENT '单价',

chao_xiang STRING COMMENT '朝向',

lou_ceng STRING COMMENT '楼层',

zhuang_xiu STRING COMMENT '装修',

xiao_qu STRING COMMENT '小区',

qu_yu STRING COMMENT '区域',

xue_xiao STRING COMMENT '小学',

jianzu_year STRING COMMENT '建筑年份',

houseid STRING COMMENT '搜房房屋ID',

publish_date STRING COMMENT '发布日期',

core_maidian STRING COMMENT '核心卖点',

imgs STRING COMMENT '图片'

)

COMMENT '学位房'
;

----上传到阿里云
tunnel upload xxx t_degreeroom -fd '","' -rd '\n' -c 'utf-8';

最近在给小朋友找学位房, 主要是先看看广州番禺市桥附近的省级小学.具体小学排名Google了一下：

番禺区：

　　第一梯队：中心小学、东城小学;

　　第二梯队：南阳里小学、德兴小学、北城小学;

接下来就是找数据了, 哪个楼盘对口哪个学校,说实话网上找了半天没有一个对应关系，初期打算从房屋介绍中截取学校信息,但是肯定不全,安居客和链家都没发现通过学校名称找房的地方，真弱鸡，这么个基本的功能都木有还做什么房产网。偶然间看到一篇搜房网的爬虫中介绍搜房有一个地图搜索入口，进去看了看竟然可以通过搜索找房.

爬虫篇：

      https://github.com/keisuo/degreeroom 

      实现了爬取代理IP(主要用于爬取搜房信息时,对抗反爬)，爬取搜房网学位房数据.

      可以简单修改代码实现爬取其他学位的数据.

数据篇:

     直接上爬取的数据了

     https://github.com/keisuo/degreeroom/blob/master/data/degreeroom.csv

数据上云：

     手动建表,手动上传资源，然后通过tunnel上传的ODPS表中

     tunnel upload http://schedule@{env}inside.cheetah.alibaba-inc.com/scheduler/res?id=100835743 t_degreeroom -fd '","' -rd '\n' -c 'utf-8';

极简分析：

     中心小学的房源还是比较多的.
     单价最近几个月波动较小.现在市场趋稳。
     小户型很小，老房子较多.
     不同户型面积价格趋势，户型越大单价越便宜.

综合实际线下调研：

     链家的房产相对准确，实际市桥二手学位房在2万出头，中心小学无论地理位置，交通，资质都是最好的，价格也是最高的.
     且都是9几年的老房子. 小户型很少放出，大部分都是2房和3房的.由于中心小学丽地铁站很近，对应的小区租房市场很好出租。
     已2房为选房目标的话，平均面积70平米左右，单价假设2.2万左右,总价154万左右,3成首付46万左右，7成首付108左右.
    根据此标准去准备首付把.买房才发现钱不是自己的钱，钱总是不够的：）
    从搜房爬取数据，本身假信息较多. 通过对比链接和搜房的平均单价差异在1.3～1.5左右，所以在搜房上看到的资源不要看得便宜，实际上需要乘以1.3～1.5才是真实的价格.，
     链家的房子数据量少很多，听说是必须三证齐全才能对外发布，只有链家内部网才可以看到刚刚登记但还没发布的房子信息.
     建议实际线下找中介套套路，问问大体情况，比自己看数据来得更直接一些.
