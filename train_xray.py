import subprocess


def train():
    log_path = "train_log.txt"

    with open(log_path, "w") as f:
        f.write("Starting training...\n")

    with open("train_log.txt", "w") as f:
        subprocess.run([
            "python", "-u", "train.py",  # 执行 Python 脚本 train.py
            "--dataroot", "./datasets/xray_gen",  # 数据集路径，CycleGAN 会从这个文件夹读取 trainA/trainB/testA/testB
            "--name", "xray_patch_model",  # 模型名称，保存模型和日志时用这个名字作为子文件夹
            "--model", "cycle_gan",  # 使用的模型类型：cycle_gan（或 pix2pix 等）
            "--preprocess", "resize",  # 预处理方式：resize 表示先缩放后处理，none 表示不变形
            "--gpu_ids", "-1",  # 使用第几块 GPU：0 表示使用第 0 号 GPU，-1 表示使用 CPU
            "--display_id", "0",  # Visdom 的显示窗口 ID（必须启动 visdom 才生效）
            "--display_freq", "5",  # 每训练多少次显示一次图像（用于 Visdom 可视化）
            "--update_html_freq", "10",  # 每训练多少次更新一次 HTML 网页日志
            "--print_freq", "1",  # 每训练多少次在终端打印一次训练日志
            "--num_threads", "0",  # 数据加载线程数，0 表示不使用多线程（Windows 建议设为 0）
            "--batch_size", "1",  # 每批训练图像数（CycleGAN 默认是 1）
            "--load_size", "1024",  # 加载图像尺寸（宽或高），图像将被 resize 到此尺寸（然后再裁剪）
            # "--crop_size", "768",                         # 裁剪尺寸（关闭此项表示不裁剪）
            "--n_epochs", "50",  # 初始学习率训练多少 epoch（第一阶段）
            "--n_epochs_decay", "50",  # 开始衰减学习率的 epoch 数（第二阶段）
            "--save_epoch_freq", "5"  # 每隔几个 epoch 保存一次模型
        ], stdout=f, stderr=subprocess.STDOUT, check=True)


if __name__ == "__main__":
    train()
