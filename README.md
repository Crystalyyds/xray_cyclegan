## 环境

传统方式：

```bash
conda create -n cyclegan python=3.8 -y
conda activate cyclegan
    
conda install -c pytorch pytorch=1.8.1 torchvision=0.9.1
conda install scipy pillow numpy -y

pip install git+https://github.com/fossasia/visdom.git

pip install dominate==2.6.0 wandb==0.12.18
```

pixi：

```bash
pixi install
# pixi install -e cpu # 如果用 cpu 跑用这一条
````

### 注意
  visdom安装后需要./visdom/server/run_server.py里面download_scripts_and_run()函数
  需要注释掉download_scripts()函数

### 数据操作
1. 把图片放到datasets里面
2. 运行./datasets/rename_and_copy.py


### 运行

传统方式：

```bash

先跑 rename_and_copy.py

# 虚拟环境下
python -m visdom.server

然后运行 train_xray.py
参数选择 "--gpu_ids", "-1",  # 参数 0 是GPU ,参数 -1 是CPU
```

pixi：

```bash
pixi run rename_and_copy
pixi run train_xray
```

### 拉伸
运行resize_back_to_original.py进行图片拉伸。保存到datasets/gen里面

### 测试
运行 test_xray.py 进行测试。保存到datasets/fake_test

