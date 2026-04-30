# Legacy VCD: Model And Dataset Paths

## 1. 模型 checkpoint

旧方向主模型：

- model: `llava-v1.5-7b`

远程主路径：

- checkpoint: `/root/autodl-tmp/code/VCD/experiments/checkpoints/llava-v1.5-7b`

旧仓库里的相对默认写法通常是：

- `experiments/checkpoints/llava-v1.5-7b`

注意：

- 旧本地 Windows 仓库 `E:\VScode\VCD` 不保证真的有完整 checkpoint；
- 实际可运行权重主要在远程机。

## 2. POPE 数据路径

### 本地旧仓库里可见的标注路径

- `E:\VScode\VCD\experiments\data\POPE`

其下可见：

- `coco`
- `gqa`
- `aokvqa`

### 远程实际运行路径

- POPE annotations: `/root/autodl-tmp/code/VCD/experiments/data/POPE`
- COCO images: `/root/autodl-tmp/code/VCD/experiments/data/coco/val2014`
- GQA images: `/root/autodl-tmp/code/VCD/experiments/data/gqa/images`

`llava1.5_pope.bash` 中对图片路径的旧默认约定：

- `coco` 和 `aokvqa` 走 `./data/coco/val2014`
- `gqa` 走 `./data/gqa/images`

## 3. MME 数据路径

远程主路径：

- MME parquet dataset: `/root/autodl-tmp/code/VCD/experiments/data/MME_Benchmark`
- prepared MME images: `/root/autodl-tmp/code/VCD/experiments/output/mme/images`
- MME eval tool: `/root/autodl-tmp/code/VCD/experiments/tools/mme/eval_tool`

本地旧仓库状态：

- `E:\VScode\VCD\experiments\data\MME_Benchmark` 当前不存在
- 说明旧本地仓库主要承担代码和报告角色，不是 MME 原始数据的完整保存位置

## 4. 与最终结论相关的旧 artifact 路径

这些是 legacy reference path，不建议复制大文件，只保留路径记录：

- MME manifest: `tmp/generalization_compare/mme_manifest.jsonl`
- full VCD output: `tmp/generalization_compare/llava15_vcd_mme_seed55_a1_b02_ns500_sq0423.jsonl`
- composite output: `tmp/generalization_compare/llava15_coer2_confmargin45_step0vcd_popeonly_mme_sq0427.jsonl`
- alternate composite output: `tmp/generalization_compare/llava15_cg2b3_coer2cur_mme_seed55.jsonl`

## 5. 为什么这份路径表要保留

新项目后续如果只是想引用旧结论，不需要碰这些路径。

但如果需要做 legacy lookup，例如：

- 查当年的 answer bank 名字
- 确认 MME 最终报告是基于哪个 artifact
- 回看 POPE / MME 命令的默认数据组织

那这份路径表会比较省时间。

## 6. 来源

- `E:\VScode\VCD\experiments\cd_scripts\llava1.5_pope.bash`
- `E:\VScode\VCD\docs\codex_handoff_docs\codex_handoff_unified_optimized.md`
- `E:\VScode\VCD\reports\mme_fullvocab_early_trace_audit.md`
- `E:\VScode\VCD\docs\baseline_reproduction_log.md`
