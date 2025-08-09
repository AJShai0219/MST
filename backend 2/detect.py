import torch
import matplotlib.pyplot as plt
from minist import Net, get_data_loader, evaluate, device  # 直接复用你训练代码里的类和方法


def main():
    # 1. 加载模型
    net = Net()
    net.load_state_dict(torch.load("mnist_model.pth", map_location=device))
    net.to(device)
    net.eval()
    print("✅ 模型加载成功：mnist_model.pth")

    # 2. 测试集准确率
    test_data = get_data_loader(is_train=False)
    acc = evaluate(test_data, net)
    print(f"🎯 模型在测试集上的准确率: {acc:.4f}")

    # 3. 可视化几个预测结果
    plt.figure(figsize=(10, 5))
    for n, (x, _) in enumerate(test_data):
        if n > 3:  # 只显示前4个batch
            break
        x = x.to(device)
        outputs = net(x.view(-1, 28 * 28))
        prediction = torch.argmax(outputs, dim=1)  # 按行取最大
        plt.subplot(2, 2, n + 1)
        plt.imshow(x[0].view(28, 28).cpu().numpy(), cmap='gray')
        plt.title(f"Prediction: {prediction[0].item()}")
        plt.axis('off')
    plt.show()


if __name__ == "__main__":
    main()
