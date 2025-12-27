from experiment import Experiment
from visualizer import Visualizer
from features import FeatureVisualization
from data_augmentation import DataAugmentation
from model_ensemble import ModelEnsemble, AdvancedCNN, ResNetMNIST
from custom_dataset import CustomDigitDataset
from real_world_demo import RealWorldDemo
import torch
import matplotlib.pyplot as plt
import os
import sys
import argparse

# 创建结果目录
os.makedirs('results', exist_ok=True)

def parse_arguments():
    parser = argparse.ArgumentParser(description="MNIST手写数字识别项目")
    parser.add_argument('--mode', type=str, default='visualize',
                        choices=['train', 'visualize', 'augment', 'ensemble', 
                                'features', 'custom', 'demo'],
                        help='运行模式')
    parser.add_argument('--model', type=str, default='model_dict/mnist_model_cnn.pth', # 注意改名以调取相应模型
                        help='模型路径')
    parser.add_argument('--data_size', type=int, default=10000,
                        help='训练数据大小')
    parser.add_argument('--batch_size', type=int, default=64,
                        help='批次大小')
    parser.add_argument('--epochs', type=int, default=3,
                        help='训练轮次')
    parser.add_argument('--results', type=str, default='model_dict/training_results_gpu.json',
                        help='训练结果JSON文件路径')
    return parser.parse_args()

def main():

    args = parse_arguments()
    
    # 创建实验实例
    exp = Experiment(batch_size=args.batch_size, learning_rate=0.01, epochs=args.epochs)

    # 根据模式执行不同功能
    if args.mode == 'train':
        # 训练模型
        exp.run_tests()
    
    elif args.mode == 'visualize':
        # 可视化结果
        vis = Visualizer(filename=args.results)
        vis.plot_comprehensive_results()
        vis.plot_learning_curve()
    
    elif args.mode == 'augment':
        # 数据增强
        data_aug = DataAugmentation()
        # 获取一些样本
        samples = exp.show_data()
        # 可视化增强效果
        data_aug.visualize_augmentations(samples[0][0])
        data_aug.compare_original_vs_augmented(exp.full_train_dataset, 5)
    
    elif args.mode == 'ensemble':
        # 模型集成
        # 创建数据加载器
        if args.data_size < 60000:
            indices = torch.randperm(60000)[:args.data_size]
            train_subset = torch.utils.data.Subset(exp.full_train_dataset, indices)
            train_loader = torch.utils.data.DataLoader(train_subset, batch_size=args.batch_size, shuffle=True)
        else:
            train_loader = torch.utils.data.DataLoader(exp.full_train_dataset, batch_size=args.batch_size, shuffle=True)
        
        # 创建模型集成
        ensemble = ModelEnsemble(exp)
        
        # 添加不同的模型
        ensemble.add_model("CNN", exp.create_model("CNN"))
        ensemble.add_model("MLP", exp.create_model("MLP"))
        ensemble.add_model("AdvancedCNN", AdvancedCNN().to(exp.device))
        ensemble.add_model("ResNetMNIST", ResNetMNIST().to(exp.device))
        
        # 训练所有模型
        results = ensemble.train_all_models(train_loader, args.data_size)
        
        # 比较模型性能
        accuracies = ensemble.compare_models()
        
        # 可视化混淆矩阵
        ensemble.visualize_confusion_matrix()
    
    elif args.mode == 'features':
        # 特征可视化
        # 加载模型
        model = exp.create_model()
        model = exp.load_model(model, args.model)
        
        # 创建可视化器
        feature_vis = FeatureVisualization(model, exp.device)
        
        # 可视化滤波器
        feature_vis.visualize_filters('conv1')
        feature_vis.visualize_filters('conv2')
        
        # 可视化特征图
        # 获取一个样本
        sample, _ = next(iter(exp.test_loader))
        sample_img = sample[0].to(exp.device)
        
        # 可视化特征图
        feature_vis.visualize_feature_maps(sample_img, 'conv1')
        feature_vis.visualize_feature_maps(sample_img, 'conv2')
        
        # 可视化嵌入
        feature_vis.visualize_embeddings(exp.test_loader, n_samples=500)
        
        # GradCAM分析
        feature_vis.grad_cam(sample_img)
    
    elif args.mode == 'custom':
        # 自定义数据集测试
        # 检查是否存在自定义数据集
        if not os.path.exists('custom_data') or len(os.listdir('custom_data')) == 0:
            print("未找到自定义数据集，请先创建并标注数据")
            from custom_dataset import launch_drawing_app
            launch_drawing_app()
            return
            
        # 加载自定义数据集
        custom_dataset = CustomDigitDataset()
        
        # 可视化样本
        custom_dataset.visualize_samples()
        
        # 加载模型
        model = exp.create_model()
        model = exp.load_model(model, args.model)
        
        # 测试模型在自定义数据上的表现
        custom_dataset.test_model_on_custom(model, exp.device)
    
    elif args.mode == 'demo':
        # 实际应用演示
        demo = RealWorldDemo(args.model)
        demo.create_gui()
    
    else:
        print(f"未知模式: {args.mode}")
        return

if __name__ == "__main__":
    main()
    # exp = Experiment(batch_size=64, learning_rate=0.01, epochs=3)
    # exp.run_tests()
    # dict_file = 'model_dict/training_results_gpu.json'
    # vis = Visualizer(filename=dict_file)
    # vis.plot_from_saved_results(dict_file)
    # vis.plot_comprehensive_results()
    # vis.plot_learning_curve()
    # vis.compare_cpu_gpu_performance()
    
    # 其它可视化调用