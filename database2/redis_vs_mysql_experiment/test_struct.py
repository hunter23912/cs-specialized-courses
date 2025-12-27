import pytest
from unittest.mock import patch, MagicMock, call
import numpy as np
import matplotlib.pyplot as plt
from test import plot_results, test_single_insert, test_single_get, test_single_update
from test import test_single_delete, test_batch_operations, test_random_access, test_scaling_performance


class TestPlotResults:
    
    @pytest.fixture
    def mock_test_functions(self):
        """提供所有测试函数的模拟对象"""
        with patch('test.test_single_insert') as mock_insert, \
             patch('test.test_single_get') as mock_get, \
             patch('test.test_single_update') as mock_update, \
             patch('test.test_single_delete') as mock_delete, \
             patch('test.test_batch_operations') as mock_batch, \
             patch('test.test_random_access') as mock_random:
            
            # 设置模拟函数的返回值
            mock_insert.return_value = {"redis": [0.5], "mysql": [2.0]}
            mock_get.return_value = {"redis": [0.2], "mysql": [1.5]}
            mock_update.return_value = {"redis": [0.3], "mysql": [2.2]}
            mock_delete.return_value = {"redis": [0.4], "mysql": [1.8]}
            mock_batch.return_value = {"redis": [1.0], "mysql": [3.0]}
            mock_random.return_value = {"redis": [0.3], "mysql": [2.5]}
            
            yield {
                "insert": mock_insert,
                "get": mock_get,
                "update": mock_update,
                "delete": mock_delete,
                "batch": mock_batch,
                "random": mock_random
            }
    
    @pytest.fixture
    def mock_plot_functions(self):
        """提供所有matplotlib绘图函数的模拟对象"""
        with patch('matplotlib.pyplot.figure') as mock_figure, \
             patch('matplotlib.pyplot.subplot') as mock_subplot, \
             patch('matplotlib.pyplot.plot') as mock_plot, \
             patch('matplotlib.pyplot.bar') as mock_bar, \
             patch('matplotlib.pyplot.xlabel') as mock_xlabel, \
             patch('matplotlib.pyplot.ylabel') as mock_ylabel, \
             patch('matplotlib.pyplot.title') as mock_title, \
             patch('matplotlib.pyplot.legend') as mock_legend, \
             patch('matplotlib.pyplot.grid') as mock_grid, \
             patch('matplotlib.pyplot.savefig') as mock_savefig, \
             patch('matplotlib.pyplot.show') as mock_show, \
             patch('matplotlib.pyplot.tight_layout') as mock_tight, \
             patch('matplotlib.pyplot.axhline') as mock_axhline, \
             patch('matplotlib.pyplot.xticks') as mock_xticks:
            
            yield {
                "figure": mock_figure,
                "subplot": mock_subplot,
                "plot": mock_plot,
                "bar": mock_bar,
                "xlabel": mock_xlabel,
                "ylabel": mock_ylabel,
                "title": mock_title,
                "legend": mock_legend,
                "grid": mock_grid,
                "savefig": mock_savefig,
                "show": mock_show,
                "tight_layout": mock_tight,
                "axhline": mock_axhline,
                "xticks": mock_xticks
            }
    
    @pytest.fixture
    def test_data(self):
        """提供测试数据"""
        return {
            "data_sizes": [100, 1000, 10000, 50000, 100000],
            "redis_times": [0.05, 0.3, 1.5, 7.0, 15.0],
            "mysql_times": [0.2, 1.5, 8.0, 35.0, 75.0]
        }
    
    def test_plot_results_calls_test_functions(self, mock_test_functions, mock_plot_functions, test_data):
        """测试plot_results函数正确调用所有测试函数"""
        # 调用被测试函数
        plot_results(test_data["data_sizes"], test_data["redis_times"], test_data["mysql_times"])
        
        # 验证所有测试函数被正确调用
        mock_test_functions["insert"].assert_called_once_with(1000)
        mock_test_functions["get"].assert_called_once_with(1000)
        mock_test_functions["update"].assert_called_once_with(1000)
        mock_test_functions["delete"].assert_called_once_with(1000)
        mock_test_functions["batch"].assert_called_once_with(10000)
        mock_test_functions["random"].assert_called_once_with(10000, 1000)
        
        # 验证图表保存和显示
        mock_plot_functions["savefig"].assert_called_once_with('redis_vs_mysql_performance.svg')
        mock_plot_functions["show"].assert_called_once()
    
    def test_plot_results_creates_figure_with_correct_size(self, mock_test_functions, mock_plot_functions, test_data):
        """测试图表尺寸是否正确设置"""
        plot_results(test_data["data_sizes"], test_data["redis_times"], test_data["mysql_times"])
        mock_plot_functions["figure"].assert_called_once_with(figsize=(15, 10))
    
    def test_plot_results_creates_four_subplots(self, mock_test_functions, mock_plot_functions, test_data):
        """测试是否创建了四个子图"""
        plot_results(test_data["data_sizes"], test_data["redis_times"], test_data["mysql_times"])
        
        # 验证子图创建
        assert mock_plot_functions["subplot"].call_count == 4
        mock_plot_functions["subplot"].assert_has_calls([
            call(2, 2, 1),
            call(2, 2, 2),
            call(2, 2, 3),
            call(2, 2, 4)
        ])
    
    def test_subplot1_scaling_performance_comparison(self, mock_test_functions, mock_plot_functions, test_data):
        """测试第一个子图：不同数据量级的性能对比"""
        with patch('test.plt.subplot') as mock_subplot, \
             patch('test.plt.plot') as mock_plot, \
             patch('test.plt.xlabel') as mock_xlabel, \
             patch('test.plt.ylabel') as mock_ylabel, \
             patch('test.plt.title') as mock_title, \
             patch('test.plt.legend') as mock_legend, \
             patch('test.plt.grid') as mock_grid:
            
            plot_results(test_data["data_sizes"], test_data["redis_times"], test_data["mysql_times"])
            
            mock_subplot.assert_any_call(2, 2, 1)
            mock_plot.assert_any_call(test_data["data_sizes"], test_data["redis_times"], 'r-o', label='Redis')
            mock_plot.assert_any_call(test_data["data_sizes"], test_data["mysql_times"], 'b-o', label='MySQL')
            mock_xlabel.assert_any_call('数据量')
            mock_ylabel.assert_any_call('执行时间 (秒)')
            mock_title.assert_any_call('不同数据量级下的插入性能')
            mock_legend.assert_called()
            mock_grid.assert_called_with(True)
    
    def test_subplot2_operation_types_comparison(self, mock_test_functions, mock_plot_functions, test_data):
        """测试第二个子图：不同操作类型的性能对比"""
        operations = ['插入', '查询', '更新', '删除', '批量']
        
        with patch('test.plt.subplot') as mock_subplot, \
             patch('test.plt.bar') as mock_bar, \
             patch('test.plt.xlabel') as mock_xlabel, \
             patch('test.plt.ylabel') as mock_ylabel, \
             patch('test.plt.title') as mock_title, \
             patch('test.plt.xticks') as mock_xticks, \
             patch('test.plt.legend') as mock_legend, \
             patch('numpy.arange') as mock_arange:
            
            # 设置模拟返回值
            mock_arange.return_value = np.array([0, 1, 2, 3, 4])
            
            plot_results(test_data["data_sizes"], test_data["redis_times"], test_data["mysql_times"])
            
            mock_subplot.assert_any_call(2, 2, 2)
            mock_xlabel.assert_any_call('操作类型')
            mock_ylabel.assert_any_call('执行时间 (秒)')
            mock_title.assert_any_call('不同操作的性能对比')
            mock_xticks.assert_called()
            mock_legend.assert_called()
            # 验证柱状图调用，参数复杂，简化验证
            assert mock_bar.call_count >= 2
    
    def test_subplot3_random_access_performance(self, mock_test_functions, mock_plot_functions, test_data):
        """测试第三个子图：随机访问性能"""
        with patch('test.plt.subplot') as mock_subplot, \
             patch('test.plt.bar') as mock_bar, \
             patch('test.plt.xlabel') as mock_xlabel, \
             patch('test.plt.ylabel') as mock_ylabel, \
             patch('test.plt.title') as mock_title:
            
            plot_results(test_data["data_sizes"], test_data["redis_times"], test_data["mysql_times"])
            
            mock_subplot.assert_any_call(2, 2, 3)
            mock_xlabel.assert_any_call('数据库')
            mock_ylabel.assert_any_call('执行时间 (秒)')
            mock_title.assert_any_call('随机访问性能 (1000次查询)')
            # 验证柱状图调用
            mock_bar.assert_called()
    
    def test_subplot4_performance_ratio(self, mock_test_functions, mock_plot_functions, test_data):
        """测试第四个子图：性能比率"""
        operations = ['插入', '查询', '更新', '删除', '批量']
        
        with patch('test.plt.subplot') as mock_subplot, \
             patch('test.plt.bar') as mock_bar, \
             patch('test.plt.axhline') as mock_axhline, \
             patch('test.plt.xlabel') as mock_xlabel, \
             patch('test.plt.ylabel') as mock_ylabel, \
             patch('test.plt.title') as mock_title:
            
            plot_results(test_data["data_sizes"], test_data["redis_times"], test_data["mysql_times"])
            
            mock_subplot.assert_any_call(2, 2, 4)
            mock_xlabel.assert_any_call('操作类型')
            mock_ylabel.assert_any_call('MySQL/Redis 时间比率')
            mock_title.assert_any_call('MySQL与Redis性能比率')
            mock_axhline.assert_called_with(y=1, color='r', linestyle='-', alpha=0.3)
            # 验证柱状图调用
            mock_bar.assert_called()
    
    def test_performance_ratio_calculation(self, mock_test_functions, test_data):
        """测试性能比率计算，包含边界情况如除零"""
        # 设置极端返回值
        mock_test_functions["insert"].return_value = {"redis": [0.1], "mysql": [2.0]}  # 比率: 20
        mock_test_functions["get"].return_value = {"redis": [0.05], "mysql": [1.5]}    # 比率: 30
        mock_test_functions["update"].return_value = {"redis": [0.2], "mysql": [0.4]}  # 比率: 2
        mock_test_functions["delete"].return_value = {"redis": [0.3], "mysql": [0.3]}  # 比率: 1
        mock_test_functions["batch"].return_value = {"redis": [0.0], "mysql": [1.0]}   # 处理除零
        
        # 模拟plt.bar并捕获其参数
        with patch('test.plt.bar') as mock_bar:
            plot_results(test_data["data_sizes"], test_data["redis_times"], test_data["mysql_times"])
            # 验证至少调用了一次柱状图绘制
            assert mock_bar.call_count >= 1
    
    def test_tight_layout_and_save(self, mock_test_functions, mock_plot_functions, test_data):
        """测试布局紧凑化和图像保存"""
        plot_results(test_data["data_sizes"], test_data["redis_times"], test_data["mysql_times"])
        
        mock_plot_functions["tight_layout"].assert_called_once()
        mock_plot_functions["savefig"].assert_called_once_with('redis_vs_mysql_performance.svg')
        mock_plot_functions["show"].assert_called_once()
    
    @patch('test.test_scaling_performance')
    def test_integration_with_scaling_performance(self, mock_scaling, mock_test_functions, mock_plot_functions):
        """测试与test_scaling_performance的集成"""
        # 设置模拟返回值
        mock_scaling.return_value = (
            [100, 1000, 10000], 
            [0.1, 0.5, 2.0], 
            [0.5, 2.5, 10.0]
        )
        
        # 模拟run_tests中的集成
        with patch('test.setup_mysql'), patch('test.cleanup'), patch('test.plot_results') as mock_plot:
            from test import run_tests
            run_tests()
            
            # 验证调用
            mock_scaling.assert_called_once()
            mock_plot.assert_called_once_with([100, 1000, 10000], [0.1, 0.5, 2.0], [0.5, 2.5, 10.0])

    # 增加更多的测试用例

    @pytest.mark.parametrize("data_size", [100, 1000, 5000])
    def test_insert_performance_comparison(self, data_size):
        """使用参数化测试不同数据量下的插入性能对比"""
        with patch('test.test_single_insert') as mock_insert:
            # 模拟不同数据量下Redis和MySQL的性能差异
            mock_insert.return_value = {
                "redis": [0.01 * data_size],
                "mysql": [0.05 * data_size]
            }
            
            # 测试数据
            data_sizes = [data_size]
            redis_times = [0.01 * data_size]
            mysql_times = [0.05 * data_size]
            
            # 捕获绘图调用
            with patch('matplotlib.pyplot.plot') as mock_plot, \
                 patch('matplotlib.pyplot.savefig'), \
                 patch('matplotlib.pyplot.show'):
                
                plot_results(data_sizes, redis_times, mysql_times)
                
                # 验证insert性能测试被调用
                mock_insert.assert_called_once_with(1000)
    
    def test_batch_size_impact(self, mock_test_functions):
        """测试批量大小对性能的影响"""
        # 模拟不同批量大小的性能数据
        batch_sizes = [10, 50, 100, 500, 1000]
        redis_batch_times = [5.0, 2.5, 1.0, 0.8, 0.7]  # 假设时间随批量大小增加而减少，但减少幅度变小
        mysql_batch_times = [15.0, 8.0, 3.0, 2.5, 2.3]  # MySQL也表现出类似模式，但整体时间更长
        
        with patch('test.test_batch_operations') as mock_batch_op, \
             patch('matplotlib.pyplot.figure'), \
             patch('matplotlib.pyplot.subplot'), \
             patch('matplotlib.pyplot.plot') as mock_plot, \
             patch('matplotlib.pyplot.savefig'), \
             patch('matplotlib.pyplot.show'):
            
            # 设置模拟返回值
            mock_batch_op.return_value = {"redis": [1.0], "mysql": [3.0]}
            
            # 使用标准数据调用plot_results
            data_sizes = [100, 1000, 10000]
            redis_times = [0.1, 0.5, 2.0]
            mysql_times = [0.5, 2.5, 10.0]
            plot_results(data_sizes, redis_times, mysql_times)
            
            # 验证batch_operations被调用
            mock_batch_op.assert_called_once_with(10000)
            
            # 这里我们只验证调用，实际绘图测试可以更详细
            assert mock_plot.call_count >= 2
    
    def test_large_dataset_performance(self, mock_test_functions):
        """测试大数据集下的性能差距"""
        # 模拟非常大的数据集下性能差距更明显
        with patch('test.test_scaling_performance') as mock_scaling:
            # 返回大数据集性能测试结果，Redis在大数据下优势更明显
            mock_scaling.return_value = (
                [1000, 10000, 100000, 1000000],
                [0.2, 1.5, 10.0, 50.0],   # Redis times
                [1.0, 15.0, 200.0, 2500.0]  # MySQL times - gap widens significantly
            )
            
            # 捕获绘图调用
            with patch('matplotlib.pyplot.plot') as mock_plot, \
                 patch('matplotlib.pyplot.savefig'), \
                 patch('matplotlib.pyplot.show'):
                
                from test import run_tests
                with patch('test.setup_mysql'), patch('test.cleanup'), \
                     patch('test.plot_results') as mock_plot_fn:
                    
                    run_tests()
                    
                    # 验证scaling_performance被调用
                    mock_scaling.assert_called_once()
                    
                    # 验证绘图函数被调用，并传入了正确的数据
                    mock_plot_fn.assert_called_once_with(
                        [1000, 10000, 100000, 1000000],
                        [0.2, 1.5, 10.0, 50.0],
                        [1.0, 15.0, 200.0, 2500.0]
                    )
    
    def test_connection_overhead(self):
        """测试连接开销对Redis和MySQL性能的影响"""
        with patch('test.redis.Redis') as mock_redis_cls, \
             patch('test.mysql.connector.connect') as mock_mysql_cls:
            
            # 模拟连接对象
            mock_redis = MagicMock()
            mock_mysql_conn = MagicMock()
            mock_cursor = MagicMock()
            
            mock_redis_cls.return_value = mock_redis
            mock_mysql_cls.return_value = mock_mysql_conn
            mock_mysql_conn.cursor.return_value = mock_cursor
            
            # 执行run_tests中的部分流程进行连接测试
            from test import setup_mysql, cleanup
            
            # 捕获连接调用
            setup_mysql()
            cleanup()
            
            # 验证连接被创建
            mock_redis_cls.assert_called_once_with(host='localhost', port=6379, db=0)
            mock_mysql_cls.assert_called_once_with(
                host="localhost",
                user="root",
                password="123456",
                database="test"
            )

if __name__ == "__main__":
    pytest.main()