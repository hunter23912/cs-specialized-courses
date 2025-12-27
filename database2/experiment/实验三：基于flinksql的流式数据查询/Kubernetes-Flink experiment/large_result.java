package cn.edu.shu;

import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class large_result {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setRuntimeMode(RuntimeExecutionMode.BATCH);
        // env.setParallelism(32);
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);

        String sourceDDL = "CREATE TABLE large_relation ("
            + "referrer INT,"
            + "referree INT"
            + ") WITH ("
            + " 'connector' = 'filesystem', "
            + " 'path' = 'file:///opt/flink/largejob/large_relation.csv', "
            + " 'format' = 'csv', "
            + " 'csv.field-delimiter' = ',', "
            + " 'csv.ignore-parse-errors' = 'true'"
            + ")";
        tableEnv.executeSql(sourceDDL);

        // 结果输出到文件系统
        tableEnv.executeSql("CREATE TABLE SinkTable ("
            + "web1 INT, "
            + "web2 INT, "
            + "similarity DOUBLE"
            + ") WITH ("
            + " 'connector' = 'filesystem',"
            + " 'path' = 'file:///opt/flink/largejob/large_result',"
            + " 'format' = 'csv',"
            + " 'csv.field-delimiter' = ',',"
            + " 'sink.rolling-policy.file-size' = '256MB',"
            + " 'sink.rolling-policy.rollover-interval' = '30 min'"
            + ")");

        // 创建临时视图 ref_count
        tableEnv.executeSql("CREATE TEMPORARY VIEW tmp_ref_count AS "
            + "SELECT referrer, COUNT(DISTINCT referree) AS web_count "
            + "FROM large_relation "
            + "GROUP BY referrer");

        // 创建临时视图 common
        tableEnv.executeSql("CREATE TEMPORARY VIEW tmp_common AS "
            + "SELECT a.referrer AS web1, b.referrer AS web2, COUNT(*) AS com_cnt "
            + "FROM large_relation a "
            + "JOIN large_relation b ON a.referree = b.referree "
            + "WHERE a.referrer < b.referrer "
            + "GROUP BY a.referrer, b.referrer");

        // 计算相似度并插入结果表
        String insertSQL = "INSERT INTO SinkTable "
            + "SELECT "
            + "    common.web1 AS web1, "
            + "    common.web2 AS web2, "
            + "    CASE "
            + "        WHEN r1.web_count + r2.web_count - common.com_cnt > 0 "
            + "        THEN common.com_cnt * 1.0 / (r1.web_count + r2.web_count - common.com_cnt) "
            + "        ELSE 0 "
            + "    END AS similarity "
            + "FROM tmp_common common "
            + "JOIN tmp_ref_count r1 ON common.web1 = r1.referrer "
            + "JOIN tmp_ref_count r2 ON common.web2 = r2.referrer";
        tableEnv.executeSql(insertSQL);
    }
}