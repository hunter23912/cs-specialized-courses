-- 实验四
object: |A ^ B| / |A U B|

|A ^ B| + | A U B| = |A| + |B|

1. |A|
R(a, b)
SELECT a , COUNT(DISTINCT b)
from R
GROUP BY a;

2. |B|
SELECT b, COUNT(DISTINCT a)
from R
GROUP BY b;

3. |A ^ B|
-- 连接查询
SELECT r1.a, r2.b
from R r1, R r2
where r1.b = r2.b and r1.a <>r2.a
GROUP BY r1.a, r2.b

-- 嵌套查询，时间复杂度是连接查询一半，十几分钟
select r1.a, r2.b
from R r1
where r2.b in { -- 先from拿表，然后where选择，最后group by分组
    select r2.a
    from R r2
    where r1.a != r2.a
}
GROUP BY r1.a, r2.b

4.解法
-- 视图方式，一次性计算
create view A_collect as {
select a, count(DISTINCT b) as a_num
from R
GROUP BY a
}

create view B_collect as {
select b, count(DISTINCT a) as b_num
from R
GROUP BY b
}

create view Common as {
SELECT r1.a, r2.b count(*) as common_num
from R r1, R r2
where r1.b = r2.b and r1.a <>r2.a 
GROUP BY r1.a, r2.a
}

select A_collect.a, B_collect.b,
case when a_num + b_num - common_num > 0 
then common_num / (a_num + b_num - common_num)
else 0
from A_collect, B_collect, Common
where A_collect.a = Common.A
and B_collect.b = Common.b


-- 临时表方式，多次计算
with A_collect as {
select a, count(DISTINCT b) as a_num
from R
GROUP BY a
}
with B_collect as {
select a, count(DISTINCT b) as b_num
from R
GROUP BY b
}
with Common as {
SELECT r1.a, r2.b, count(*) as common_num
from R r1, R r2
where r1.b = r2.b and r1.a <>r2.a 
GROUP BY r1.a, r2.a  
}
select A_collect.a, B_collect.a,
case when a_num + b_num - common_num > 0 
then common_num / (a_num + b_num - common_num)
else 0
from A_collect, B_collect, Common
where A_collect.a = Common.a
and B_collect.a = Common.b
