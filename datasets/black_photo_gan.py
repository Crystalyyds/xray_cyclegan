from PIL import Image
import os


def create_photo():

    root_folder = "black_gan"
    subfolders = ["trainA", "trainB", "testA", "testB"]
    current_dir = os.getcwd()
    subfolder_paths = {}
    for sub in subfolders:
        path = os.path.join(current_dir, root_folder, sub)
        os.makedirs(path, exist_ok=True)
        subfolder_paths[sub] = path
        print(f"创建：{path}")

    # 生成纯黑图像并保存到 testA/
    black_img = Image.new("RGB", (1024, 1024), color=(0, 0, 0))
    save_path = os.path.join(subfolder_paths["testA"], "test1.jpg")
    black_img.save(save_path)
    print(f"黑图已保存：{save_path}")


if __name__ == '__main__':
    create_photo()
