from models import *
import torch, time, json
from torch.utils.data import DataLoader, Subset
import numpy as np


'''
NOTE 创建模型测试类

1.创建模型
2.训练模型
3.测试模型
4.保存和加载模型
5.保存和加载训练结果
'''
class Experiment:
    def __init__(self, batch_size=64, learning_rate=0.01, epochs=3):
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.data_sizes = [1000, 5000, 10000, 20000, 30000, 40000, 50000, 60000]
        self.training_times = []
        self.accuracies = []
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f'Using device: {self.device}')
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        print('Loading MNIST dataset...')
        self.full_train_dataset = datasets.MNIST(
            root='./data', train=True, download=True, transform=transform)
        self.test_dataset = datasets.MNIST(
            root='./data', train=False, download=True, transform=transform)
        self.test_loader = DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=False)
        print('MNIST dataset loaded.')
        self.results = {
            'parameters': {
                'batch_size': batch_size,
                'learning_rate': learning_rate,
                'epochs': epochs,
                'device': str(self.device)
            },
            'experiments': []
        }

    def create_model(self, model_type='CNN'):
        if model_type == 'MLP':
            model = SimpleMLP()
        else:
            model = CNNModel()
        return model.to(self.device)

    def train_model(self, model, train_loader, data_size):
        start_time = time.time()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=self.learning_rate)
        epoch_metrics = []
        for epoch in tqdm(range(self.epochs), desc='Training Epochs', unit='epoch'):
            model.train()
            running_loss = 0.0
            process_bar = tqdm(train_loader, desc=f'Epoch {epoch + 1}/{self.epochs}', unit='batch')
            for batch_idx, (data, target) in enumerate(process_bar):
                data, target = data.to(self.device), target.to(self.device)
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
            epoch_loss = running_loss / len(train_loader)
            epoch_accuracy = self.test_model(model, show=False)
            epoch_metrics.append({
                'epoch': epoch + 1,
                'loss': round(epoch_loss, 3),
                'accuracy': round(epoch_accuracy, 2)
            })
            print(f'\nEpoch {epoch + 1}, LOss: {running_loss / len(train_loader):.3f}')
        end_time = time.time()
        training_time = end_time - start_time
        print(f'Training Time: {training_time:.3f} seconds')
        final_accuracy = max(metric['accuracy'] for metric in epoch_metrics)
        experiment_result = {
            'data_size': data_size,
            'training_time': round(training_time, 3),
            'final_accuracy': round(final_accuracy, 2),
            'epoch_metrics': epoch_metrics,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.results['experiments'].append(experiment_result)
        return model, training_time

    def test_model(self, model, show=True):
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data, target in self.test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = model(data)
                _, predicted = torch.max(output.data, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()
        accuracy = 100 * correct / total
        if show:
            print(f'Test Accuracy: {accuracy:.2f}%')
        return accuracy

    def run_tests(self):
        self.training_times = []
        self.accuracies = []
        best_model = None
        best_accuracy = 0.0
        for size in tqdm(self.data_sizes, desc='Running Tests', unit='dataset'):
            print(f'\nTraining with data size: {size} samples')
            if size < 60000:
                indices = np.random.choice(60000, size, replace=False)
                subset_dataset = Subset(self.full_train_dataset, indices)
                train_loader = DataLoader(subset_dataset, batch_size=self.batch_size, shuffle=True)
            else:
                train_loader = DataLoader(self.full_train_dataset, batch_size=self.batch_size, shuffle=True)
            model = self.create_model()
            model, training_time = self.train_model(model, train_loader, size)
            accuracy = self.test_model(model)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = model
            self.training_times.append(training_time)
            self.accuracies.append(accuracy)
        self.save_model(best_model)
        # self.save_results()

    def save_results(self, filename='model_dict/training_results.json'):
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f'训练结果已保存到 {filename}')

    def load_results(self, filename='model_dict/training_results.json'):
        try:
            with open(filename, 'r') as f:
                self.results = json.load(f)
            experiments = sorted(self.results['experiments'], key=lambda x: x['data_size'])
            self.data_sizes = [exp['data_size'] for exp in experiments]
            self.training_times = [exp['training_time'] for exp in experiments]
            self.accuracies = [exp['final_accuracy'] for exp in experiments]
            print(f'成功从{filename}加载训练结果')
            return self
        except Exception as e:
            print(f'加载结果时出错：{e}')
            return None

    def save_model(self, model, filename='model_dict/mnist_model_cnn.pth'):
        torch.save(model.state_dict(), filename)
        print(f'模型已保存为 {filename}')

    def load_model(self, model, filename='model_dict/mnist_model.pth', model_type='CNN'):
        if model_type == 'MLP':
            model = SimpleMLP()
        else:
            model = CNNModel()
        model.load_state_dict(torch.load(filename, weights_only=True))
        model.to(self.device)
        print(f'模型已加载 {filename}')
        return model

    def show_data(self):
        # 只负责返回数据，不绘图
        return [self.full_train_dataset[i] for i in range(10)]

    def show_result(self, model, train_loader):
        # 只负责返回预测结果，不绘图
        data, target = next(iter(train_loader))
        data, target = data.to(self.device), target.to(self.device)
        output = model(data)
        _, predicted = torch.max(output.data, 1)
        return data.cpu(), target.cpu(), predicted.cpu()
    