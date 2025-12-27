package cn.edu.shu;

import org.apache.flink.table.api.EnvironmentSettings;
import org.apache.flink.table.api.TableEnvironment;

public class show {
    public static void main(String[] args) throws Exception {
        EnvironmentSettings settings = EnvironmentSettings.newInstance().inBatchMode().build();
        TableEnvironment tableEnv = TableEnvironment.create(settings);

        tableEnv.executeSql("CREATE TABLE ResultFile ("
            + "  web1 INT, web2 INT, similarity DOUBLE"
            + ") WITH ("
            + "  'connector' = 'filesystem',"
            + "  'path' = 'file:///home/ubuntu/tableapp/output/medium_result/medium_output',"
            + "  'format' = 'csv',"
            + "  'csv.field-delimiter' = ','"
            + ")");

        // 3. 创建 print 输出表
        tableEnv.executeSql("CREATE TABLE PrintTable ("
            + "  web1 INT, web2 INT, similarity DOUBLE"
            + ") WITH ('connector' = 'print')");

        // 4. 只输出前50行
        tableEnv.executeSql("INSERT INTO PrintTable SELECT * FROM ResultFile LIMIT 100");
    }
}