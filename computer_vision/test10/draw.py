import torch
from models import SimpleCNN
from torchsummary import summary
from torchviz import make_dot

# netron advanced__cnn.onnx
def netron_viewer():
    # 创建模型实例
    model = SimpleCNN()

    # 创建样本输入
    dummy_input = torch.randn(1, 1, 28, 28)

    # 导出为ONNX格式
    torch.onnx.export(model, dummy_input, "advanced_cnn.onnx", 
                    verbose=True, input_names=['input'], 
                    output_names=['output'])

    print("模型已导出为 advanced_cnn.onnx")
    
def torchsummary_viewer():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # 创建模型实例
    model = SimpleCNN().to(device)

    # 打印模型摘要
    summary(model, (1, 28, 28))

def torchviz_viewer():
    model = SimpleCNN()
    x = torch.randn(2, 1, 28, 28)
    y = model(x)
    dot = make_dot(y)
    dot.render("output", format="svg")
    
if __name__ == "__main__":
    # netron_viewer()
    # torchsummary_viewer()
    torchviz_viewer()
