# Paper figures v2

Run from the repository root:

```bash
cd /home/PengJunhao/workspace/SegEarth-OV-3
bash paper_figures_v2/tools/run_dataset_paper_figures_8gpu.sh LoveDA 30
```

Outputs:

```text
paper_figures_v2/
├── manifests/
├── palettes/
├── preds/{baseline,ours}/
├── figures/<dataset>/
└── logs/<dataset>/
```

Each figure contains:

```text
Input | Ground Truth | Baseline | Ours
```

The legend is placed at the bottom. NoData/ignore pixels are shown in light gray. Column titles report per-image mIoU, not the dataset average. Predictions are exported with 8 GPU shards by default; set `NUM_GPUS=4` to reduce memory pressure.