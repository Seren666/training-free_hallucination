# Legacy VCD: Remote Paths And Runtime Notes

## 1. 远程机入口

旧方向实际运行主环境不是本地 Windows 仓库，而是远程 AutoDL 机器。

从旧 handoff 和运行记录可整理出的入口如下：

- host: `connect.westc.seetacloud.com`
- port: `21607`
- user: `root`
- repo root: `/root/autodl-tmp/code/VCD`
- conda env: `/root/autodl-tmp/envs/vcd`

常用连接方式：

```bash
ssh -p 21607 root@connect.westc.seetacloud.com
```

## 2. 远程运行激活顺序

```bash
source /root/miniconda3/etc/profile.d/conda.sh
conda activate /root/autodl-tmp/envs/vcd
cd /root/autodl-tmp/code/VCD

unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY all_proxy ALL_PROXY
export HF_HOME=/root/autodl-tmp/hf-home
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export HF_DATASETS_OFFLINE=1
export OMP_NUM_THREADS=8
```

## 3. 旧 runtime 常见坑

### 3.1 GPU 可见性会丢

旧日志里明确出现过：

- `nvidia-smi` 无设备
- `torch.cuda.is_available() == False`

所以任何新线程如果只是读 legacy 信息，不需要重新跑；如果以后真要考古跑命令，先查 GPU。

### 3.2 代理变量会破坏 HF / CLIP 加载

旧运行记录里，坏代理会导致：

- CLIP vision tower 加载失败
- HF 访问异常

所以旧命令普遍会先清空代理，并启用离线缓存。

### 3.3 MME parquet glob 必须加引号

旧 `mme_prepare.py` 跑过一次坑：

```bash
python ./eval/mme_prepare.py --parquet_glob "./data/MME_Benchmark/data/*.parquet"
```

不要去掉引号。

## 4. 这份信息现在还有什么用

主要作为“旧方向 provenance / archaeology”使用：

- 回看当时到底在哪台机器上跑
- 回看数据和模型实际挂载在哪里
- 回看为什么很多命令都会带 offline / unset proxy

不建议把它当成新项目必须沿用的主环境。

## 5. 来源

- `E:\VScode\VCD\docs\README.md`
- `E:\VScode\VCD\docs\codex_handoff_docs\codex_handoff_unified_optimized.md`
- `E:\VScode\VCD\docs\baseline_reproduction_log.md`
- 用户给出的旧 remote execution handoff
