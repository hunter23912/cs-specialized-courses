# 连接方式,临时表分步计算
create table result2 as (
with ref_count as (select referrer, count(distinct referree) as web_count
                    from relation
                      group by referrer),
 common as (select a.referrer as web1, b.referrer as web2, count(*) as com_cnt
             from relation a,
                  relation b
             where a.referree = b.referree
               and a.referrer < b.referrer
             group by a.referrer, b.referrer)
select common.web1 as web1, common.web2 as web2,
case when r1.web_count + r2.web_count - common.com_cnt > 0
then common.com_cnt / (r1.web_count + r2.web_count - common.com_cnt)
else 0
end as similarity
from ref_count r1, ref_count r2, common
where r1.referrer = common.web1
and r2.referrer = common.web2 order by similarity desc);

# 嵌套相关子查询
WITH ref_count AS (
    SELECT referrer, COUNT(DISTINCT referree) AS web_count
    FROM relation
    GROUP BY referrer
),
common AS (
    SELECT
        a.referrer AS web1,
        b.referrer AS web2,
        COUNT(*) AS com_cnt,
        min((SELECT web_count FROM ref_count WHERE referrer = a.referrer)) AS web1_count,
        min((SELECT web_count FROM ref_count WHERE referrer = b.referrer)) AS web2_count
    FROM relation a
    JOIN relation b ON a.referree = b.referree
    WHERE a.referrer < b.referrer
    GROUP BY a.referrer, b.referrer
)
SELECT
    common.web1,
    common.web2,
    CASE
        WHEN common.web1_count + common.web2_count - common.com_cnt > 0
        THEN common.com_cnt / (common.web1_count + common.web2_count - common.com_cnt)
        ELSE 0
    END AS similarity
FROM common
ORDER BY similarity DESC
LIMIT 20;

# 嵌套查询
WITH ref_count AS (
    SELECT referrer, COUNT(DISTINCT referree) AS web_count
    FROM relation
    GROUP BY referrer
),
common AS (
    SELECT a.referrer AS web1, b.referrer AS web2, COUNT(*) AS com_cnt
    FROM relation a
    JOIN relation b ON a.referree = b.referree
    WHERE a.referrer < b.referrer
    GROUP BY a.referrer, b.referrer
)
SELECT common.web1, common.web2,
CASE WHEN r1.web_count + r2.web_count - common.com_cnt > 0
THEN common.com_cnt / (r1.web_count + r2.web_count - common.com_cnt)
ELSE 0 END AS similarity
FROM common JOIN (
    SELECT referrer, web_count
    FROM ref_count
    WHERE referrer IN (SELECT web1 FROM common)
) r1 ON common.web1 = r1.referrer
JOIN (
    SELECT referrer, web_count
    FROM ref_count
    WHERE referrer IN (SELECT web2 FROM common)
) r2 ON common.web2 = r2.referrer order by similarity desc limit 20;

# 使用集合操作实现
WITH ref_count AS (
    SELECT referrer, COUNT(DISTINCT referree) AS web_count
    FROM relation GROUP BY referrer),
 common as (select a.referrer as web1, b.referrer as web2, count(*) as com_cnt
             from relation a, relation b
             where a.referree = b.referree
               and a.referrer < b.referrer
             group by a.referrer, b.referrer)
SELECT common.web1, common.web2,
CASE WHEN r1.web_count + r2.web_count - common.com_cnt > 0
THEN common.com_cnt / (r1.web_count + r2.web_count - common.com_cnt)
ELSE 0 END AS similarity
FROM common JOIN (
    SELECT referrer, web_count FROM ref_count
    WHERE referrer IN (
        SELECT web1 FROM common
        INTERSECT
        SELECT referrer FROM ref_count)
) r1 ON common.web1 = r1.referrer
JOIN (
    SELECT referrer, web_count
    FROM ref_count
    WHERE referrer IN (
        SELECT web2 FROM common
        INTERSECT
        SELECT referrer FROM ref_count)
) r2 ON common.web2 = r2.referrer order by similarity desc limit 20;

# 使用exists方式
WITH ref_count AS (
    SELECT referrer, COUNT(DISTINCT referree) AS web_count
    FROM relation
    GROUP BY referrer
),
common AS (
    SELECT a.referrer AS web1, b.referrer AS web2, COUNT(*) AS com_cnt
    FROM relation a
    JOIN relation b ON a.referree = b.referree
    WHERE a.referrer < b.referrer
    GROUP BY a.referrer, b.referrer
)
SELECT
    common.web1,
    common.web2,
    CASE
        WHEN r1.web_count + r2.web_count - common.com_cnt > 0
        THEN common.com_cnt / (r1.web_count + r2.web_count - common.com_cnt)
        ELSE 0
    END AS similarity
FROM common JOIN (
    SELECT referrer, web_count
    FROM ref_count r
    WHERE EXISTS (SELECT 1 FROM common c WHERE c.web1 = r.referrer)
) r1 ON common.web1 = r1.referrer
JOIN (
    SELECT referrer, web_count
    FROM ref_count r
    WHERE EXISTS (SELECT 1 FROM common c WHERE c.web2 = r.referrer)
) r2 ON common.web2 = r2.referrer
ORDER BY similarity DESC LIMIT 20;

# select p1.a, p2.a, count(*)
# from (
#     select p1.a, p2.a
#     from P p1, P p2
#     where p1.b = p2.b and p1.a != p2.a
#     intersect
#     select p1.a, p2.a
#     from P p1, P p2
#     where p1.b = p2.b and p1.a != p2.a
#      ) as subquery
# group by p1.a, p2.a;


# 大数据集实验
create table tmp_ref_count AS (
    SELECT referrer, COUNT(DISTINCT referree) AS web_count
    FROM relation
    GROUP BY referrer
);

create table tmp_common AS (
    SELECT a.referrer AS web1, b.referrer AS web2, COUNT(*) AS com_cnt
    FROM relation a
    JOIN relation b ON a.referree = b.referree
    WHERE a.referrer < b.referrer
    GROUP BY a.referrer, b.referrer
);

CREATE TABLE result AS
SELECT
    common.web1 AS web1,
    common.web2 AS web2,
    CASE
        WHEN r1.web_count + r2.web_count - common.com_cnt > 0
        THEN common.com_cnt / (r1.web_count + r2.web_count - common.com_cnt)
        ELSE 0
    END AS similarity
FROM tmp_ref_count r1, tmp_ref_count r2, tmp_common common
where r1.referrer = common.web1
AND r2.referrer = common.web2
ORDER BY similarity DESC;