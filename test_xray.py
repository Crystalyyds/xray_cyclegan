import os
import subprocess
import shutil


def run_test():
    log_path = "test_log.txt"

    with open(log_path, "w") as f:
        f.write("Starting test...\n")

    with open(log_path, "a") as f:
        subprocess.run([
            "python", "-u", "test.py",
            "--dataroot", "./datasets/xray_gen",  # 测试数据集路径
            "--dataset_mode", "unaligned",  # 支持分开文件夹格式
            "--name", "xray_patch_model",  # 模型名称（必须和训练时一致）
            "--model", "pix2pix",  # 使用 Pix2Pix 模型
            "--phase", "test",  # 测试阶段
            "--no_dropout",  # 关闭 dropout（推理阶段应关闭）
            "--preprocess", "resize",  # 图像预处理方式（应与训练一致）
            "--load_size", "1024",  # 输入图像尺寸（应与训练一致）
            "--crop_size", "1024",  # 保持一致，Pix2Pix 需要明确 crop_size
            "--gpu_ids", "-1"  # 使用 CPU，若用 GPU 改成对应 GPU 编号
        ], stdout=f, stderr=subprocess.STDOUT, check=True)


if __name__ == "__main__":
    run_test()
