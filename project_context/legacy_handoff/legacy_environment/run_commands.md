# Legacy VCD: Main Run Commands

这份文件只保留旧方向最主要的命令模板，作为 provenance 参考。

不建议在当前项目里继续沿这些命令开新实验。

## 1. 远程环境激活

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

## 2. POPE baseline / VCD 命令模板

旧仓库自带的 `llava1.5_pope.bash`：

```bash
seed=${1:-55}
dataset_name=${2:-"coco"}
type=${3:-"random"}
model_path=${4:-"./checkpoints/llava-v1.5-7b"}
cd_alpha=${5:-1}
cd_beta=${6:-0.2}
noise_step=${7:-500}
if [[ $dataset_name == 'coco' || $dataset_name == 'aokvqa' ]]; then
  image_folder=./data/coco/val2014
else
  image_folder=./data/gqa/images
fi

python ./eval/object_hallucination_vqa_llava.py \
  --model-path ${model_path} \
  --question-file ./data/POPE/${dataset_name}/${dataset_name}_pope_${type}.json \
  --image-folder ${image_folder} \
  --answers-file ./output/llava15_${dataset_name}_pope_${type}_answers_no_cd_seed${seed}.jsonl \
  --use_cd \
  --cd_alpha $cd_alpha \
  --cd_beta $cd_beta \
  --noise_step $noise_step \
  --seed ${seed}
```

注意：

- 这个脚本会开 `--use_cd`，但输出文件名里写着 `no_cd`，不适合直接拿来做严谨 baseline bookkeeping。

## 3. MME 数据准备

```bash
python ./eval/mme_prepare.py \
  --parquet_glob "./data/MME_Benchmark/data/*.parquet" \
  --image_output_dir ./output/mme/images \
  --question_file ./output/mme/mme_questions.jsonl \
  --manifest_file ./output/mme/mme_manifest.jsonl
```

## 4. MME full VCD 推理

```bash
python ./eval/object_hallucination_vqa_llava.py \
  --model-path ./checkpoints/llava-v1.5-7b \
  --image-folder ./output/mme/images \
  --question-file ./output/mme/mme_questions.jsonl \
  --answers-file ./output/mme/answers/llava15_vcd_mme_seed55_a1_b02_ns500.jsonl \
  --use_cd \
  --cd_alpha 1 \
  --cd_beta 0.2 \
  --noise_step 500 \
  --seed 55
```

## 5. MME 结果格式化

```bash
python ./eval/mme_format_results.py \
  --manifest_file ./output/mme/mme_manifest.jsonl \
  --answers_file ./output/mme/answers/llava15_vcd_mme_seed55_a1_b02_ns500.jsonl \
  --results_dir ./output/mme/results_vcd
```

## 6. 和 legacy 结果关系最密切的关键入口

- 主评测入口：`experiments/eval/object_hallucination_vqa_llava.py`
- POPE 评测：`experiments/eval/eval_pope.py`
- MME prepare：`experiments/eval/mme_prepare.py`
- MME format：`experiments/eval/mme_format_results.py`
- full-vocab trace 分析：`experiments/eval/analyze_mme_fullvocab_trace.py`
- MME self-diagnostic 分析：`experiments/eval/analyze_mme_self_diagnostic.py`

## 7. 这份命令表怎么用

- 用来查 provenance：旧结果当时到底怎么跑的。
- 用来查参数：seed / alpha / beta / noise_step / question-file / image-folder。
- 不建议把它当成当前新项目继续扩 VCD 的起点。

## 8. 来源

- `E:\VScode\VCD\experiments\cd_scripts\llava1.5_pope.bash`
- `E:\VScode\VCD\docs\baseline_reproduction_log.md`
- `E:\VScode\VCD\docs\codex_handoff_docs\codex_handoff_unified_optimized.md`
- `E:\VScode\VCD\reports\mme_fullvocab_early_trace_audit.md`
