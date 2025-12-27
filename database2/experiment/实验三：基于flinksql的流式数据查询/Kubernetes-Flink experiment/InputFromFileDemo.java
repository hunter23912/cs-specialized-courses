package cn.edu.shu;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.TableResult;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

public class InputFromFileDemo {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        env.setParallelism(1);
        // 创建一个输入表SourceTable
        String sourceDDL = "create table stockPriceTable ("
            + "stockId STRING,"
            + "price DOUBLE"
            + ") with ("
            + " 'connector' = 'filesystem', "
            + " 'path' = 'file:///home/ubuntu/stockprice.csv', "
            + " 'format' = 'csv', "
            + " 'csv.field-delimiter' = ',', "
            + " 'csv.ignore-parse-errors' = 'true' "
            + " )";
        tableEnv.executeSql(sourceDDL);
        // 使用SQL语句创建一个输出表SinkTable
        tableEnv.executeSql("CREATE TEMPORARY TABLE SinkTable(stockId STRING,price DOUBLE) WITH "
            + "('connector' = 'print')");
        // 使用Table API创建一个Table对象table1
        Table table1 = tableEnv.from("stockPriceTable");

        Table table2 = tableEnv.sqlQuery("SELECT * FROM stockPriceTable");
        // 把Table对象table1写入到输出表SinkTable中
        TableResult tableResult = table2.executeInsert("SinkTable");
    }
}
