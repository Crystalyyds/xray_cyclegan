import os
import random
import shutil
from PIL import Image


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def get_all_images(input_dir):
    return sorted([f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])


def find_max_size(input_dir, image_files):
    max_w, max_h = 0, 0
    for filename in image_files:
        path = os.path.join(input_dir, filename)
        try:
            with Image.open(path) as img:
                w, h = img.size
                max_w = max(max_w, w)
                max_h = max(max_h, h)
        except Exception as e:
            print(f"跳过无法打开的图片 {filename}: {e}")
    return max_w, max_h


def resize_and_save_all(input_dir, output_dir, image_files, target_size):
    for idx, filename in enumerate(image_files, start=1):
        in_path = os.path.join(input_dir, filename)
        out_path = os.path.join(output_dir, f"{idx}.jpg")
        try:
            with Image.open(in_path) as img:
                resized = img.resize(target_size, Image.BICUBIC)
                resized.save(out_path)
                print(f"保存: {out_path}")
        except Exception as e:
            print(f"处理失败 {filename}: {e}")


def copy_all(src_dir, dst_dir):
    ensure_dir(dst_dir)
    for filename in os.listdir(src_dir):
        if filename.lower().endswith(".jpg"):
            shutil.copy2(os.path.join(src_dir, filename), os.path.join(dst_dir, filename))


def copy_random_subset(src_dir, dstA_dir, dstB_dir, num=5):
    all_files = [f for f in os.listdir(src_dir) if f.lower().endswith(".jpg")]
    chosen = random.sample(all_files, min(num, len(all_files)))
    ensure_dir(dstA_dir)
    ensure_dir(dstB_dir)
    for f in chosen:
        shutil.copy2(os.path.join(src_dir, f), os.path.join(dstA_dir, f))
        shutil.copy2(os.path.join(src_dir, f), os.path.join(dstB_dir, f))
    print(f"从 trainA 随机抽取了 {len(chosen)} 张保存到 testA 和 testB。")


if __name__ == "__main__":
    raw_dir = "useful_photo"
    base_dir = "xray_gen"
    trainA_dir = os.path.join(base_dir, "trainA")
    trainB_dir = os.path.join(base_dir, "trainB")
    testA_dir = os.path.join(base_dir, "testA")
    testB_dir = os.path.join(base_dir, "testB")

    # 创建目录
    for d in [trainA_dir, trainB_dir, testA_dir, testB_dir]:
        ensure_dir(d)

    image_files = get_all_images(raw_dir)
    max_w, max_h = find_max_size(raw_dir, image_files)
    print(f"最大分辨率: {max_w} x {max_h}")

    # 步骤 1：resize + rename 保存到 trainA
    resize_and_save_all(raw_dir, trainA_dir, image_files, (max_w, max_h))

    # 步骤 2：复制所有 trainA 到 trainB
    copy_all(trainA_dir, trainB_dir)

    # 步骤 3 & 4：随机选5张图片保存到 testA 和 testB
    copy_random_subset(trainA_dir, testA_dir, testB_dir, num=5)

    print("所有步骤已完成。")
