import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from models import SimpleCNN
from tqdm import tqdm
import matplotlib.pyplot as plt
from torchsummary import summary
from torchviz import make_dot

# 1. 数据加载与预处理
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

# 2. 模型、损失函数、优化器
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

def show_data():
    images, labels = next(iter(DataLoader(train_dataset, batch_size=10, shuffle=True)))
    plt.figure(figsize=(10, 4))
    for i in range(10):
        plt.subplot(2, 5, i+1)
        plt.imshow(images[i][0].cpu().numpy(), cmap='gray')
        plt.title(str(labels[i].item()))
        plt.axis('off')
    plt.suptitle("10 MNIST Samples")
    plt.tight_layout()
    plt.savefig("mnist_samples.svg")
    plt.show()

# 3. 训练
def train(model, device, train_loader, optimizer, criterion, epoch):
    model.train()
    total_loss = 0
    for batch_idx, (data, target) in tqdm(enumerate(train_loader), desc=f"Training Epoch {epoch}", total=len(train_loader)):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch}, Loss: {total_loss / len(train_loader):.4f}")

# 4. 测试
def test(model, device, test_loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for data, target in tqdm(test_loader, desc="Testing", total=len(test_loader)):
            data, target = data.to(device), target.to(device)
            output = model(data)
            pred = output.argmax(dim=1)
            correct += (pred == target).sum().item()
            total += target.size(0)
    acc = correct / total
    print(f"Test Accuracy: {acc * 100:.2f}%")
    return acc

def test_result(model, device):
    model.eval()
    images, labels = next(iter(DataLoader(test_dataset, batch_size=5, shuffle=True)))
    images, labels = images.to(device), labels.to(device)
    with torch.no_grad():
        outputs = model(images)
        preds = outputs.argmax(dim=1)
    plt.figure(figsize=(10, 2))
    for i in range(5):
        plt.subplot(1, 5, i+1)
        plt.imshow(images[i][0].cpu().numpy(), cmap='gray')
        if preds[i].item() == labels[i].item():
            color = 'green'
        else:
            color = 'red'
        plt.title(f"Pred:{preds[i].item()}\nTrue:{labels[i].item()}", color=color)
        plt.axis('off')
    plt.suptitle("Test 5 Images")
    plt.tight_layout()
    plt.savefig("test_results.svg")
    plt.show()
    

def load_model():
    model = SimpleCNN().to(device)
    model.load_state_dict(torch.load('best_model.pth'))
    model.eval()
    return model

def main():
    epochs = 5
    best_acc = 0.0  
    best_state_dict = None
    for epoch in tqdm(range(1, epochs + 1), desc="Epochs", total=epochs):
        train(model, device, train_loader, optimizer, criterion, epoch)
        acc = test(model, device, test_loader)
        if acc > best_acc:
            best_acc = acc
            best_state_dict = model.state_dict()
            print(f"New best model found with accuracy: {best_acc * 100:.2f}%")
    if best_state_dict is not None:
        torch.save(model.state_dict(), 'best_model.pth')
        print(f"Saved model with accuracy: {best_acc * 100:.2f}%")

def netron_viewer():
    # 创建模型实例并加载权重
    model = SimpleCNN().to(device)
    model.load_state_dict(torch.load('best_model.pth', map_location=device))
    model.eval()
    dummy_input = torch.randn(1, 1, 28, 28, device=device)
    torch.onnx.export(model, dummy_input, "advanced_cnn.onnx", 
                    verbose=True, input_names=['input'], 
                    output_names=['output'])
    print("模型已导出为 SimpleCNN.onnx")

    
def torchsummary_viewer():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleCNN().to(device)
    model.load_state_dict(torch.load('best_model.pth', map_location=device))
    model.eval()
    summary(model, (1, 28, 28))

def torchviz_viewer():
    model = SimpleCNN().to(device)
    model.load_state_dict(torch.load('best_model.pth', map_location=device))
    model.eval()
    x = torch.randn(2, 1, 28, 28, device=device)
    y = model(x)
    dot = make_dot(y)
    dot.render("output", format="svg")

if __name__ == '__main__':
    # show_data()
    main()
    
    # model = load_model()
    # netron_viewer()
    # torchsummary_viewer()
    # torchviz_viewer()
    # test_result(model, device)
    