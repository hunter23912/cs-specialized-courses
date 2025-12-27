create table tmp_ref_count AS (
    SELECT referrer, COUNT(DISTINCT referree) AS web_count
    FROM small_relation
    GROUP BY referrer
);

create table tmp_common AS (
    SELECT a.referrer AS web1, b.referrer AS web2, COUNT(*) AS com_cnt
    FROM small_relation a
    JOIN small_relation b ON a.referree = b.referree
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
FROM tmp_common common join tmp_ref_count r1 on common.web1 = r1.referrer
JOIN tmp_ref_count r2 on common.web2 = r2.referrer;