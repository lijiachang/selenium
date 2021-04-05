
use Supermarket
/* 商品表 */
create table Commodity(
commodity_no varchar(10) primary key,/*商品编号*/
commodity__name varchar(20),/*商品名称*/
commodity__type1 varchar(10),/*商品类型*/
commodity__size varchar(5),/*商品规格*/
commodity__sprice float,/*售价*/
commodity__mdate datetime,/*生产日期*/
commodity__edate datetime,/*保质期*/
commodity__quantity int,/*库存数量*/
)

insert into Commodity values('0000000001','奶香曲奇饼干','饼干','袋',7,'2020-12-23 00:00:00.000','2023-02-04 00:00:00.000','150')
insert into Commodity values('002','旺仔小牛奶','饮料','瓶',2,'2020-12-23 00:00:00.000','2023-02-04 00:00:00.000','150')
insert into Commodity values('003','红牛功能饮料','饮料','瓶',5,'2020-12-23 00:00:00.000','2023-02-04 00:00:00.000','150')

go
/*教育背景表*/
CREATE TABLE EducationInfo(
education_id int primary key,/*教育背景编号*/
diploma varchar(20),/*学历*/
)

insert into EducationInfo values(1,'初中')
insert into EducationInfo values(2,'高中')
insert into EducationInfo values(3,'大专')
insert into EducationInfo values(4,'本科')
insert into EducationInfo values(5,'研究生')


go
/*销售员.售货员*/
CREATE TABLE Cashier(
cashier_no varchar(10) primary key,/*员工编号*/
cashier_name varchar(10),
cashier_pwd varchar(10),
cashier_sex char(2),
cashier_age int,
cashier_hourse varchar(50),
cashier_salary float,
cashier_phone varchar(11),
employee_education_id int,
foreign key(employee_education_id ) references EducationInfo(education_id ) on delete set null,
)

insert into Cashier values('000001','小琳','111','女',18,'beijing',3600,10086,4)
insert into Cashier values('000002','小王','12345678','男',14,'beijing',3600,10086,2)
insert into Cashier values('000004','小红','12345678','女',20,'tianjing',2500,10010,2)

go 
/*采购员*/
create table Purchaser(
purchaser_no varchar(10) primary key,/*员工编号*/
purchaser_name varchar(10),
purchaser_pwd varchar(10),
purchaser_sex char(2),
purchaser_age int,
purchaser_salary float,
purchaser_phone varchar(11),
purchaser_entrytime datetime,
employee_education_id int,
foreign key(employee_education_id ) references EducationInfo(education_id ) on delete set null,
)

insert into Purchaser values('001','张麻子','123','男',22,3500,17600208888,'2021-01-23 00:00:00.000',4)

go
/* 进货记录表 */
create table Stock(
purchaser_no varchar(10),
commodity_no varchar(10),
stock_no varchar(20),
stock_sprice float,
stock_quantity int,
stock_date datetime,
primary key(stock_no),
foreign key(purchaser_no ) references purchaser(purchaser_no ) on delete set null,
foreign key(commodity_no ) references commodity(commodity_no ) on delete set null,
)
go
/* 销售记录表 */
create table Sell(
cashier_no varchar(10),
commodity_no varchar(10),
sell_no varchar(20),/* 交易流水号 */
sell_quantity int,/* 售卖数量 */
sell_price float,/*应收金额*/
/* sell_rmoney float,/*实收金额*/ */
sell_date datetime,
primary key(sell_no),
foreign key(cashier_no ) references cashier(cashier_no ) on delete set null,
foreign key(commodity_no ) references commodity(commodity_no ) on delete set null,
)

/* 管理员表 */
create table Administrator(
admin_no varchar(10),
admin_pwd varchar(10),
admin_name varchar(20),
admin_phone varchar(15),
admin_addres varchar(200),
primary key (admin_no)
)



insert into Administrator values('001','123456','张琳鑫','110','北京市海淀区大同路6号')
insert into Administrator values('ljc','123456','李嘉诚','110','北京市海淀区大同路5号')


/*Sell表级联删除触发器*/
CREATE TRIGGER Delete_sellcommodity
ON Commodity
FOR DELETE
AS
DELETE Sell
FROM deleted
WHERE Sell.commodity_no=deleted.commodity_no

/*Sell表级联删除触发器*/
CREATE TRIGGER Delete_sellcashier
ON Cashier
FOR DELETE
AS
DELETE Sell
FROM deleted
WHERE Sell.cashier_no=deleted.cashier_no


/*Stock表级联删除触发器*/
CREATE TRIGGER Delete_stockCommodity
ON Commodity
FOR DELETE
AS
DELETE Stock
FROM deleted
WHERE Stock.commodity_no=deleted.commodity_no


/*Stock表级联删除触发器*/
CREATE TRIGGER Delete_stockpurchaser
ON Purchaser
FOR DELETE
AS
DELETE Stock
FROM deleted
WHERE Stock.purchaser_no=deleted.purchaser_no
