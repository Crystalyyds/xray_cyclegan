import os
from PIL import Image

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def get_nth_image(input_dir, n):
    images = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    if 1 <= n <= len(images):
        return images[n - 1]
    return None

def crop_and_save(image_path, out_dir, img_idx, crop_size=(768, 768), stride=256):
    ensure_dir(out_dir)
    with Image.open(image_path) as img:
        w, h = img.size
        crop_w, crop_h = crop_size
        for left in range(0, w - crop_w + 1, stride):       # 先横向切
            for top in range(0, h - crop_h + 1, stride):    # 再竖向切
                crop = img.crop((left, top, left + crop_w, top + crop_h))
                crop_name = f"{img_idx}_{left:04d}_{top:04d}.jpg"
                crop.save(os.path.join(out_dir, crop_name))


if __name__ == "__main__":
    raw_dir = "useful_photo"  # 原始图片文件夹
    patch_base_dir = "test_one_patch"  # 切片保存的根目录

    # 指定训练集和测试集的图片序号
    train_imgs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    test_imgs = [1, 4, 8, 12]

    # 对应的子目录名
    train_subdirs = ["trainA", "trainB"]
    test_subdirs = ["testA", "testB"]

    # 处理训练集图片
    for img_idx in train_imgs:
        img_name = get_nth_image(raw_dir, img_idx)
        if not img_name:
            print(f"未找到第{img_idx}张图片，跳过")
            continue
        img_path = os.path.join(raw_dir, img_name)
        for sub in train_subdirs:
            out_dir = os.path.join(patch_base_dir, sub)
            crop_and_save(img_path, out_dir, img_idx)
            print(f"已处理第{img_idx}张图，保存到 {out_dir}")

    # 处理测试集图片
    for img_idx in test_imgs:
        img_name = get_nth_image(raw_dir, img_idx)
        if not img_name:
            print(f"未找到第{img_idx}张图片，跳过")
            continue
        img_path = os.path.join(raw_dir, img_name)
        for sub in test_subdirs:
            out_dir = os.path.join(patch_base_dir, sub)
            crop_and_save(img_path, out_dir, img_idx)
            print(f"已处理第{img_idx}张图，保存到 {out_dir}")

    print("所有切片操作完成。")
