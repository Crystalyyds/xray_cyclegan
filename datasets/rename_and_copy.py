import os
import random
import shutil

from PIL import Image, ImageOps
import numpy as np
import json


# 创建文件夹
def create_xray_gen_folders(base_dir="xray_gen"):
    subfolders = ["trainA", "trainB", "testA", "testB"]
    for sub in subfolders:
        path = os.path.join(base_dir, sub)
        os.makedirs(path, exist_ok=True)
    print("文件夹创建")


# 计算中值分辨率，然后进行拉伸
def get_image_paths(folder):
    exts = ('.jpg', '.jpeg', '.png', '.bmp')
    return [os.path.join(folder, f) for f in sorted(os.listdir(folder)) if f.lower().endswith(exts)]


def compute_median_resolution(image_paths):
    widths, heights = [], []
    for path in image_paths:
        with Image.open(path) as img:
            w, h = img.size
            widths.append(w)
            heights.append(h)
    median_w = int(np.median(widths))
    median_h = int(np.median(heights))
    print(f"📏 中值分辨率为: {median_w} x {median_h}")
    return median_w, median_h


def stretch_and_save_to_trainB(image_paths, target_size, save_dir):
    for idx, path in enumerate(image_paths, start=1):
        with Image.open(path) as img:
            stretched = img.resize(target_size, Image.BICUBIC)
            out_path = os.path.join(save_dir, f"{idx}.jpg")
            stretched.convert("RGB").save(out_path, "JPEG")
            print(f"拉伸保存: {out_path}")


# 等比缩放 + padding + 记录
def resize_with_padding(img, target_size=(1024, 1024)):
    original_w, original_h = img.size
    ratio = min(target_size[0] / original_w, target_size[1] / original_h)
    new_w = int(original_w * ratio)
    new_h = int(original_h * ratio)

    resized_img = img.resize((new_w, new_h), Image.BICUBIC)

    pad_left = (target_size[0] - new_w) // 2
    pad_top = (target_size[1] - new_h) // 2
    pad_right = target_size[0] - new_w - pad_left
    pad_bottom = target_size[1] - new_h - pad_top

    padded_img = ImageOps.expand(resized_img, (pad_left, pad_top, pad_right, pad_bottom), fill=0)
    assert padded_img.size == target_size

    padding_info = {
        "original_size": [original_w, original_h],
        "resized_size": [new_w, new_h],
        "padding": {
            "left": pad_left,
            "top": pad_top,
            "right": pad_right,
            "bottom": pad_bottom
        }
    }

    return padded_img, padding_info


def apply_padding_to_trainB(trainB_dir):
    image_paths = get_image_paths(trainB_dir)
    all_padding_info = {}

    for path in image_paths:
        filename = os.path.basename(path)
        with Image.open(path) as img:
            img = img.convert("RGB")
            padded_img, info = resize_with_padding(img)
            padded_img.save(path, "JPEG")
            all_padding_info[filename] = info
            print(f"Padding: {filename} → {info['resized_size']} + pad {info['padding']}")

    # Save padding info
    json_path = "padding_info.json"  # 当前目录保存
    with open(json_path, "w") as f:
        json.dump(all_padding_info, f, indent=2)
    print(f" Padding 信息保存至: {json_path}")


def main():
    src_folder = "useful_photo"
    trainB_folder = "xray_gen/trainB"

    # 步骤 1：创建文件夹
    create_xray_gen_folders()

    # 步骤 2：拉伸到中值分辨率
    image_paths = get_image_paths(src_folder)
    if not image_paths:
        print("useful——photo为空")
        return

    median_size = compute_median_resolution(image_paths)
    stretch_and_save_to_trainB(image_paths, median_size, trainB_folder)

    # 步骤 3：对 trainB 中的图片进行 padding 并记录信息
    apply_padding_to_trainB(trainB_folder)


# trainB抽铺0张到testB
def copy_random_10_to_testB():
    trainB_dir = "xray_gen/trainB"
    testB_dir = "xray_gen/testB"

    os.makedirs(testB_dir, exist_ok=True)

    all_images = [f for f in os.listdir(trainB_dir) if f.lower().endswith(".jpg")]
    selected = random.sample(all_images, 10)

    for filename in selected:
        src = os.path.join(trainB_dir, filename)
        dst = os.path.join(testB_dir, filename)
        shutil.copy(src, dst)
        print(f"复制 {filename} 到 testB")

    print("随机复制完成：10张图片已保存到 xray_gen/testB")


def generate_black_images(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)

    for filename in os.listdir(src_dir):
        if filename.lower().endswith(".jpg"):
            src_path = os.path.join(src_dir, filename)
            dst_path = os.path.join(dst_dir, filename)

            with Image.open(src_path) as img:
                black = Image.new("RGB", img.size, (0, 0, 0))
                black.save(dst_path, "JPEG")
                print(f"生成黑图: {dst_dir}/{filename}")


def generate_black_images_for_train_test():
    generate_black_images("xray_gen/trainB", "xray_gen/trainA")
    generate_black_images("xray_gen/testB", "xray_gen/testA")
    print(" trainA 和 testA 黑图生成完毕")


if __name__ == "__main__":
    main()
    copy_random_10_to_testB()
    generate_black_images_for_train_test()
