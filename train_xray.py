import subprocess


def train():
    with open("train_log.txt", "w") as f:
        subprocess.run([
            "python", "-u", "train.py",
            "--dataroot", "./datasets/xray_gen",
            "--name", "xray_patch_model",
            "--model", "pix2pix",
            "--dataset_mode", "unaligned",  # 支持分开文件夹格式
            "--preprocess", "resize",
            "--gpu_ids", "-1",
            "--no_flip",  # 禁用水平翻转
            "--display_id", "0",  # 0
            "--display_freq", "10",
            "--update_html_freq", "2",
            "--num_threads", "0",
            "--batch_size", "1",
            "--load_size", "1024",
            "--crop_size", "1024",
            "--lambda_L1", "100",
            "--n_epochs", "50",  # 50
            "--n_epochs_decay", "100",  # 100
            "--save_epoch_freq", "5",  # 5
            "--print_freq", "20",
        ], stdout=f, stderr=subprocess.STDOUT, check=True)


if __name__ == "__main__":
    train()
