package cn.edu.shu;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.TableResult;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class small_task {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        env.setParallelism(1);

        // 创建small表，字段a、b，分隔符为空格
        String sourceDDL = "CREATE TABLE small ("
            + "a STRING,"
            + "b STRING"
            + ") WITH ("
            + " 'connector' = 'filesystem', "
            + " 'path' = 'file:///home/pioneer/small_relation', "
            + " 'format' = 'csv', "
            + " 'csv.field-delimiter' = ' ', "
            + " 'csv.ignore-parse-errors' = 'true' "
            + ")";
        tableEnv.executeSql(sourceDDL);

        // 创建输出表
        tableEnv.executeSql(
            "CREATE TABLE SinkTable(a STRING, b STRING) WITH ('connector' = 'print')");

        // 查询small表
        Table table = tableEnv.sqlQuery("SELECT * FROM small limit 100");
        TableResult tableResult = table.executeInsert("SinkTable");
    }
}