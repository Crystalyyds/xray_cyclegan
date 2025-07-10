# 基于cycle-gan的图像生成
  通过全黑图片到目标图片的转换学习图像生成的模型。图片预处理，进行等比例缩小，短边进行padding填充。
  图片处理信息保存再datasets/padding_info.json

## 环境
```bash
conda create -n cyclegan python=3.8 -y
conda activate cyclegan
    
conda install -c pytorch pytorch=1.8.1 torchvision=0.9.1
conda install scipy pillow numpy -y

pip install git+https://github.com/fossasia/visdom.git

pip install dominate==2.6.0 wandb==0.12.18
```

### 注意
  非必需开启：
    1. 开启可视化训练过程，train_xray.py里面的--display_id参数设置为 非0
      (1) visdom安装后需要./visdom/server/run_server.py里面download_scripts_and_run()函数
      (2) 需要注释掉download_scripts()函数
    2. 关闭可视化训练过程，train_xray.py里面的--display_id参数设置为 0


### 数据操作
1. 把图片放到datasets里面
2. 运行./datasets/rename_and_copy.py


### 运行
```bash

先跑 rename_and_copy.py

# 虚拟环境下
python -m visdom.server

然后运行 train_xray.py
参数选择 "--gpu_ids", "-1",  # 参数 0 是GPU ,参数 -1 是CPU
```


### 拉伸 (目前不支持拉伸)
运行resize_back_to_original.py进行图片拉伸。保存到datasets/gen里面

### 测试
运行 test_xray.py 进行测试。保存到datasets/fake_test

  