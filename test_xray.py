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
            "--dataroot", "./datasets/xray_gen",  # 测试数据目录
            "--name", "xray_patch_model",  # 模型名称（和训练保持一致）
            "--model", "cycle_gan",
            "--phase", "test",
            "--no_dropout",
            "--preprocess", "resize",  # 和训练时保持一致
            "--load_size", "1024",  # 保持和训练一致
            # "--crop_size", "1024",
            "--gpu_ids", "-1"  # -1 表示使用 CPU
        ], stdout=f, stderr=subprocess.STDOUT, check=True)


if __name__ == "__main__":
    run_test()
