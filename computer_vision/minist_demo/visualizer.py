import matplotlib.pyplot as plt
import numpy as np
import json
from experiment import Experiment

# 设置plt中文字体
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

'''
NOTE 可视化类

3个功能：
1. 绘制全面的结果分析图
2. 绘制不同数据规模的学习曲线
3. 比较CPU和GPU的结果差异
'''
class Visualizer:
    def __init__(self, experiment: Experiment = None, filename: str = None): # 类型注解
        if experiment:
            # 从experiment实例获取
            self.results = experiment.results
            self.data_sizes = experiment.data_sizes
            self.training_times = experiment.training_times
            self.accuracies = experiment.accuracies
        elif filename:
            # 直接从json文件加载
            with open(filename, 'r', encoding='utf-8') as f:
                self.results = json.load(f)
            experiments = sorted(self.results['experiments'], key=lambda x: x['data_size'])
            self.data_sizes = [exp['data_size'] for exp in experiments]
            self.training_times = [exp['training_time'] for exp in experiments]
            self.accuracies = [exp['final_accuracy'] for exp in experiments]
        else:
            raise ValueError("请提供Experiment实例或json文件名")
        
    # 绘制全面的结果分析图
    def plot_comprehensive_results(self):
        fig, axs = plt.subplots(2,2, figsize=(18, 14))
        
        # 1.训练时间随数据规模变化
        axs[0, 0].plot(self.data_sizes, self.training_times, 'o-', linewidth=2, markersize=8, color='#1f77b4')
        axs[0, 0].set_xlabel('数据规模', fontsize=12)
        axs[0, 0].set_ylabel('训练时间(s)', fontsize=12)
        axs[0, 0].set_title('数据规模对训练时间的影响', fontsize=14)
        # 添加标签
        for i, txt in enumerate(self.training_times):
            axs[0, 0].annotate(f'{txt:.1f}s',
                               (self.data_sizes[i], self.training_times[i]),
                               textcoords='offset points',
                               xytext=(0, 10),
                               ha='center')
        axs[0, 0].grid(True, linestyle='--', alpha=0.7)
        
        # 2.准确率随数据规模变化曲线
        axs[0, 1].plot(self.data_sizes, self.accuracies, 'o-', linewidth=2, markersize=8, color='#2ca02c')
        axs[0, 1].set_xlabel('数据规模', fontsize=12)
        axs[0, 1].set_ylabel('准确率 (%)', fontsize=12)
        axs[0, 1].set_title('数据规模对准确率的影响', fontsize=14)
        # 添加标签
        for i, txt in enumerate(self.accuracies):
            axs[0, 1].annotate(f'{txt:.1f}%',
                               (self.data_sizes[i], self.accuracies[i]),
                               textcoords='offset points',
                               xytext=(0, 10),
                               ha='center')
        axs[0, 1].grid(True, linestyle='--', alpha=0.7)
        
        # 3.每个epoch的损失变化曲线（不同颜色表示不同数据规模）
        for i, exp in enumerate(self.results['experiments']):
            data_size = exp['data_size']
            epochs = [metric['epoch'] for metric in exp['epoch_metrics']]
            losses = [metric['loss'] for metric in exp['epoch_metrics']]
            axs[1, 0].plot(epochs, losses, 'o-', linewidth=2, label=f'{data_size} samples')
        
        axs[1, 0].set_xlabel('轮次', fontsize=12)
        axs[1, 0].set_ylabel('损失值', fontsize=12)
        axs[1, 0].set_title('不同数据规模下的损失值', fontsize=14)
        axs[1, 0].legend(loc='upper right')
        axs[1, 0].grid(True, linestyle='--', alpha=0.7)
        
        # 4.训练时间与准确率的散点图（泡泡大小表示数据规模）
        sc = axs[1, 1].scatter(self.training_times, self.accuracies, 
                           s=[size/300 for size in self.data_sizes], # 调整泡泡大小
                           c=self.data_sizes, 
                           cmap='viridis', 
                           alpha=0.7)
        
        # 为每个点添加标签
        for i, txt in enumerate(self.data_sizes):
            axs[1, 1].annotate(f'{txt}', 
                            (self.training_times[i], self.accuracies[i]),
                            textcoords="offset points", 
                            xytext=(5,5), 
                            ha='left')
        
        axs[1, 1].set_xlabel('训练时间(s)', fontsize=12)
        axs[1, 1].set_ylabel('准确率(%)', fontsize=12)
        axs[1, 1].set_title('训练时间与准确率的关系', fontsize=14, fontweight='bold')
        plt.colorbar(sc, ax=axs[1, 1], label='数据规模')
        axs[1, 1].grid(True, linestyle='--', alpha=0.7)
        
        # 设置整体布局
        plt.tight_layout()
        plt.savefig('comprehensive_results.svg')
        plt.show()
        
        # 额外绘制训练效果图
        plt.figure(figsize=(10, 6))
        efficiency = [acc/time for acc, time in zip(self.accuracies, self.training_times)]
        plt.bar(range(len(self.data_sizes)), efficiency, color='#5F9EA0')
        plt.xticks(range(len(self.data_sizes)), [str(size) for size in self.data_sizes])
        plt.xlabel('数据规模', fontsize=12)
        plt.ylabel('训练效率(准确率/训练时间)', fontsize=12)
        plt.title('不同数据规模下的训练效率', fontsize=14, fontweight='bold')
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # 添加数值标签
        for i, v in enumerate(efficiency):
            plt.text(i, v + 0.01, f'{v:.3f}', ha='center')
        
        plt.tight_layout()
        plt.savefig('training_efficiency.svg')
        plt.show()
    
    # 绘制不同数据规模的学习曲线
    def plot_learning_curve(self):
        plt.figure(figsize=(12, 8))
    
        # 为每个数据规模绘制学习曲线
        for exp in self.results['experiments']:
            data_size = exp['data_size']
            epochs = [metric['epoch'] for metric in exp['epoch_metrics']]
            accuracies = [metric['accuracy'] for metric in exp['epoch_metrics']]
            
            plt.plot(epochs, accuracies, 'o-', linewidth=2, markersize=8, label=f'{data_size}样本')
        
        plt.xlabel('训练轮次', fontsize=12)
        plt.ylabel('准确率(%)', fontsize=12)
        plt.title('不同数据规模的学习曲线', fontsize=14, fontweight='bold')
        plt.legend(loc='lower right')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # 设置y轴范围，使差异更明显
        plt.ylim(min([min([metric['accuracy'] for metric in exp['epoch_metrics']]) 
                    for exp in self.results['experiments']]) - 5, 100)
        
        plt.tight_layout()
        plt.savefig('learning_curves.svg')
        plt.show()
    
    # 读json文件绘图
    def plot_from_saved_results(self, filename='model_dict/training_results.json'):
            
        if self.experiment.load_results(filename):
            print('绘制综合结果图...')
            self.plot_comprehensive_results()
            print('绘制学习曲线...')
            self.plot_learning_curve()
            
    # 比较CPU和GPU的结果差异绘图
    def compare_cpu_gpu_performance(self, cpu_file='training_results_cpu.json', gpu_file='training_results_gpu.json'):
        try:
            # 加载CPU和GPU的结果
            with open(cpu_file, 'r') as f:
                cpu_results = json.load(f)
            with open(gpu_file, 'r') as f:
                gpu_results = json.load(f)
                
            # 提取CPU时间和准确率
            cpu_sizes = [exp['data_size'] for exp in cpu_results['experiments']]
            cpu_times = [exp['training_time'] for exp in cpu_results['experiments']]
            cpu_accuracies = [exp['final_accuracy'] for exp in cpu_results['experiments']]
            
            gpu_sizes = [exp['data_size'] for exp in gpu_results['experiments']]
            gpu_times = [exp['training_time'] for exp in gpu_results['experiments']]
            gpu_accuracies = [exp['final_accuracy'] for exp in gpu_results['experiments']]
                        
            # 创建一个包含6个子图的大图表
            plt.figure(figsize=(20, 18))
             
            # 1. 训练时间比较 - 折线图
            plt.subplot(3, 2, 1)
            plt.plot(cpu_sizes, cpu_times, 'o-', linewidth=2, label='CPU', color='#ff7f0e')
            plt.plot(gpu_sizes, gpu_times, 'o-', linewidth=2, label='GPU', color='#1f77b4')
            plt.xlabel('数据规模', fontsize=12)
            plt.ylabel('训练时间(s)', fontsize=12)
            plt.title('CPU vs GPU: 训练时间比较', fontsize=14, fontweight='bold')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            
            # 添加具体数值标签
            for i in range(len(cpu_sizes)):
                plt.text(cpu_sizes[i], cpu_times[i] + 2, f'{cpu_times[i]:.1f}s', 
                        ha='center', va='bottom', color='#ff7f0e')
                plt.text(gpu_sizes[i], gpu_times[i] + 2, f'{gpu_times[i]:.1f}s', 
                        ha='center', va='bottom', color='#1f77b4')
            
            # 2. 准确率比较 - 折线图
            plt.subplot(3, 2, 2)
            plt.plot(cpu_sizes, cpu_accuracies, 'o-', linewidth=2, label='CPU', color='#ff7f0e')
            plt.plot(gpu_sizes, gpu_accuracies, 'o-', linewidth=2, label='GPU', color='#1f77b4')
            plt.xlabel('数据规模', fontsize=12)
            plt.ylabel('最终准确率(%)', fontsize=12)
            plt.title('CPU vs GPU: 准确率比较', fontsize=14, fontweight='bold')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            
            # 3. 加速比分析 - 折线图和柱状图结合
            plt.subplot(3, 2, 3)
            speedup = [cpu/gpu for cpu, gpu in zip(cpu_times, gpu_times)]
            
            # 双轴图
            ax1 = plt.gca()
            ax1.bar(gpu_sizes, speedup, alpha=0.6, color='#d62728', width=1000)
            ax1.set_xlabel('数据规模', fontsize=12)
            ax1.set_ylabel('加速比(CPU时间/GPU时间)', fontsize=12, color='#d62728')
            ax1.tick_params(axis='y', colors='#d62728')
            
            # 添加数值标签
            for i, sp in enumerate(speedup):
                ax1.text(gpu_sizes[i], sp + 0.1, f'{sp:.2f}x', 
                        ha='center', va='bottom', fontweight='bold')
            
            # 添加第二个Y轴：时间减少百分比
            ax2 = ax1.twinx()
            time_reduction = [(cpu - gpu)/cpu * 100 for cpu, gpu in zip(cpu_times, gpu_times)]
            ax2.plot(gpu_sizes, time_reduction, 'o-', color='#2ca02c', linewidth=2)
            ax2.set_ylabel('时间减少百分比(%)', fontsize=12, color='#2ca02c')
            ax2.tick_params(axis='y', colors='#2ca02c')
            
            plt.title('GPU加速比和时间节省分析', fontsize=14, fontweight='bold')
            
            # 4. 训练效率比较 (准确率/时间)
            plt.subplot(3, 2, 4)
            cpu_efficiency = [acc/time for acc, time in zip(cpu_accuracies, cpu_times)]
            gpu_efficiency = [acc/time for acc, time in zip(gpu_accuracies, gpu_times)]
            
            x = np.arange(len(cpu_sizes))
            width = 0.35
            
            plt.bar(x - width/2, cpu_efficiency, width, label='CPU', color='#ff7f0e', alpha=0.7)
            plt.bar(x + width/2, gpu_efficiency, width, label='GPU', color='#1f77b4', alpha=0.7)
            plt.xlabel('数据规模', fontsize=12)
            plt.ylabel('训练效率(准确率/秒)', fontsize=12)
            plt.title('CPU vs GPU: 训练效率比较', fontsize=14, fontweight='bold')
            plt.xticks(x, [str(size) for size in cpu_sizes])
            plt.grid(True, axis='y', linestyle='--', alpha=0.7)
            plt.legend()
            
            # 5. 数据规模对加速比的影响 - 散点图
            plt.subplot(3, 2, 5)
            plt.scatter(cpu_sizes, speedup, s=80, c=time_reduction, cmap='viridis', alpha=0.8)
            z = np.polyfit(cpu_sizes, speedup, 1)
            p = np.poly1d(z)
            plt.plot(cpu_sizes, p(cpu_sizes), "r--", alpha=0.7)
            
            plt.colorbar(label='时间减少百分比(%)')
            plt.xlabel('数据规模', fontsize=12)
            plt.ylabel('加速比', fontsize=12)
            plt.title('数据规模与GPU加速比关系', fontsize=14, fontweight='bold')
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # 添加拟合线方程
            plt.text(np.mean(cpu_sizes), max(speedup)*0.9, 
                    f'拟合线: y = {z[0]:.6f}x + {z[1]:.2f}', 
                    ha='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
            
            # 6. 每轮准确率提升比较
            plt.subplot(3, 2, 6)
            
            # CPU每轮准确率提升
            for i, exp in enumerate(cpu_results['experiments']):
                if i % 2 == 0:  # 只显示部分数据，避免图表太拥挤
                    data_size = exp['data_size']
                    epochs = [metric['epoch'] for metric in exp['epoch_metrics']]
                    accuracies = [metric['accuracy'] for metric in exp['epoch_metrics']]
                    plt.plot(epochs, accuracies, 'o--', alpha=0.7, linewidth=1.5, 
                            label=f'CPU {data_size}样本')
            
            # GPU每轮准确率提升
            for i, exp in enumerate(gpu_results['experiments']):
                if i % 2 == 0:  # 只显示部分数据，避免图表太拥挤
                    data_size = exp['data_size']
                    epochs = [metric['epoch'] for metric in exp['epoch_metrics']]
                    accuracies = [metric['accuracy'] for metric in exp['epoch_metrics']]
                    plt.plot(epochs, accuracies, 's-', alpha=0.7, linewidth=1.5, 
                            label=f'GPU {data_size}样本')
            
            plt.xlabel('训练轮次', fontsize=12)
            plt.ylabel('准确率(%)', fontsize=12)
            plt.title('CPU vs GPU: 每轮准确率提升比较', fontsize=14, fontweight='bold')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend(fontsize=8)
            
            plt.tight_layout()
            plt.savefig('cpu_gpu_comparison_all.svg')
            plt.show()
            
            # 额外图表：时间-准确率权衡分析
            plt.figure(figsize=(12, 8))
            
            # 散点图：训练时间 vs 准确率
            plt.scatter(cpu_times, cpu_accuracies, s=[size/200 for size in cpu_sizes], 
                    alpha=0.7, label='CPU', color='#ff7f0e')
            plt.scatter(gpu_times, gpu_accuracies, s=[size/200 for size in gpu_sizes], 
                    alpha=0.7, label='GPU', color='#1f77b4')
            
            # 添加标签
            for i, size in enumerate(cpu_sizes):
                plt.annotate(f'{size}', (cpu_times[i], cpu_accuracies[i]), 
                            xytext=(5, 0), textcoords='offset points')
                plt.annotate(f'{size}', (gpu_times[i], gpu_accuracies[i]), 
                            xytext=(5, 0), textcoords='offset points')
            
            # 绘制连接线
            for i in range(len(cpu_sizes)):
                plt.plot([cpu_times[i], gpu_times[i]], 
                        [cpu_accuracies[i], gpu_accuracies[i]], 
                        '--', color='gray', alpha=0.5)
            
            plt.xlabel('训练时间(s)', fontsize=12)
            plt.ylabel('最终准确率(%)', fontsize=12)
            plt.title('训练时间与准确率权衡分析', fontsize=14, fontweight='bold')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend()
            
            plt.tight_layout()
            plt.savefig('time_accuracy_tradeoff.svg')
            plt.show()
            
            # 额外图表：每个epoch的损失比较 (选择一个特定数据规模如20000样本)
            plt.figure(figsize=(10, 6))
            
            # 找到20000样本的实验
            cpu_exp_20k = next((exp for exp in cpu_results['experiments'] if exp['data_size'] == 20000), None)
            gpu_exp_20k = next((exp for exp in gpu_results['experiments'] if exp['data_size'] == 20000), None)
            
            if cpu_exp_20k and gpu_exp_20k:
                cpu_epochs = [metric['epoch'] for metric in cpu_exp_20k['epoch_metrics']]
                cpu_losses = [metric['loss'] for metric in cpu_exp_20k['epoch_metrics']]
                
                gpu_epochs = [metric['epoch'] for metric in gpu_exp_20k['epoch_metrics']]
                gpu_losses = [metric['loss'] for metric in gpu_exp_20k['epoch_metrics']]
                
                plt.plot(cpu_epochs, cpu_losses, 'o-', linewidth=2, label='CPU', color='#ff7f0e')
                plt.plot(gpu_epochs, gpu_losses, 'o-', linewidth=2, label='GPU', color='#1f77b4')
                plt.xlabel('训练轮次', fontsize=12)
                plt.ylabel('损失值', fontsize=12)
                plt.title('CPU vs GPU: 20000样本的损失下降曲线', fontsize=14, fontweight='bold')
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.legend()
                
                plt.tight_layout()
                plt.savefig('loss_comparison.svg')
                plt.show()
            
            # 打印概要统计信息
            avg_speedup = sum(speedup) / len(speedup)
            max_speedup = max(speedup)
            max_speedup_idx = speedup.index(max_speedup)
            
            avg_time_reduction = sum(time_reduction) / len(time_reduction)
            
            print("\n==== CPU vs GPU 性能对比概要 ====")
            print(f"平均加速比: {avg_speedup:.2f}x")
            print(f"最大加速比: {max_speedup:.2f}x (数据规模: {cpu_sizes[max_speedup_idx]})")
            print(f"平均训练时间减少: {avg_time_reduction:.2f}%")
            print(f"CPU总训练时间: {sum(cpu_times):.2f}秒")
            print(f"GPU总训练时间: {sum(gpu_times):.2f}秒")
            print(f"CPU最终平均准确率: {sum(cpu_accuracies)/len(cpu_accuracies):.2f}%")
            print(f"GPU最终平均准确率: {sum(gpu_accuracies)/len(gpu_accuracies):.2f}%")
            
        except Exception as e:
            print(f"对比分析时出错: {e}")
            import traceback
            traceback.print_exc()