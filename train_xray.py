import subprocess


def train():
    log_path = "train_log.txt"

    with open(log_path, "w") as f:
        f.write("Starting training...\n")

    with open("train_log.txt", "w") as f:
        subprocess.run([
            "python", "-u", "train.py",
            "--dataroot", "./datasets/xray_gen",
            "--name", "xray_patch_model",
            "--model", "cycle_gan",
            "--preprocess", "resize",  # 参数 none 不压缩
            "--gpu_ids", "-1",  # 参数 0 是GPU ,参数 -1 是CPU
            "--display_id", "10",
            "--display_freq", "5",
            "--update_html_freq", "10",
            "--print_freq", "1",
            "--num_threads", "0",
            "--batch_size", "1",
            # "--load_size", "768",
            # "--crop_size", "768",
            "--n_epochs", "1",
            "--n_epochs_decay", "1",
            "--save_epoch_freq", "1"
        ], stdout=f, stderr=subprocess.STDOUT, check=True)


if __name__ == "__main__":
    train()
