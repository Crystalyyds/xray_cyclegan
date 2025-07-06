import os
from PIL import Image
from tqdm import tqdm

def upscale_all_images(
    input_dir, output_dir, target_size=(1821, 9705)
):
    os.makedirs(output_dir, exist_ok=True)

    print(f"将所有图像统一放大到 {target_size} ...")
    for fname in tqdm(os.listdir(input_dir)):
        if fname.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(input_dir, fname)
            try:
                with Image.open(input_path) as img:
                    resized_img = img.resize(target_size, Image.BICUBIC)
                    save_path = os.path.join(output_dir, fname)
                    resized_img.save(save_path)
                    print(f"放大并保存: {fname}，新大小: {target_size}")
            except Exception as e:
                print(f" 处理图像失败 {fname}: {e}")

    print(f"\n 所有图像已放大并保存到: {output_dir}")

if __name__ == "__main__":
    input_images_dir = "./checkpoints/xray_patch_model/web/images"  # 输入图片路径
    output_resized_dir = "./datasets/gen"  # 放大后保存路径
    target_width = 1821
    target_height = 9705

    upscale_all_images(
        input_dir=input_images_dir,
        output_dir=output_resized_dir,
        target_size=(target_width, target_height)
    )
