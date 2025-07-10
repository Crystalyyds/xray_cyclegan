import os

def count_images_in_folder(folder):
    exts = ('.jpg', '.jpeg', '.png')
    files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
    return len(files)

def main():
    base_dir = "xray_gen"
    if not os.path.exists(base_dir):
        print(f"目录不存在: {base_dir}")
        return

    for subfolder in os.listdir(base_dir):
        path = os.path.join(base_dir, subfolder)
        if os.path.isdir(path):
            count = count_images_in_folder(path)
            print(f"{subfolder} 文件夹中有 {count} 张图片。")

if __name__ == "__main__":
    main()
