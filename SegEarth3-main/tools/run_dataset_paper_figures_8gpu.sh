#!/usr/bin/env bash
set -euo pipefail

DATASET="${1:-}"
if [[ -z "${DATASET}" ]]; then
  echo "Usage: $0 <dataset> [num_samples]" >&2
  echo "Datasets: LoveDA OpenEarthMap Potsdam Vaihingen iSAID UAVid UDD5 VDD VOC20 Cityscapes" >&2
  exit 2
fi

NUM_SAMPLES="${2:-30}"
OUTPUT_ROOT="${OUTPUT_ROOT:-paper_figures_v2}"
DATA_ROOT="${DATA_ROOT:-/home/PengJunhao/workspace/data}"
PRED_ROOT="${PRED_ROOT:-${OUTPUT_ROOT}/preds}"
PALETTE_DIR="${PALETTE_DIR:-${OUTPUT_ROOT}/palettes}"
MANIFEST_DIR="${MANIFEST_DIR:-${OUTPUT_ROOT}/manifests}"
FIGURE_ROOT="${FIGURE_ROOT:-${OUTPUT_ROOT}/figures}"
PYTHON_BIN="${PYTHON_BIN:-python}"
NUM_GPUS="${NUM_GPUS:-8}"
KEY="$(printf '%s' "${DATASET}" | tr '[:upper:]' '[:lower:]')"
MANIFEST="${MANIFEST_DIR}/${KEY}.csv"
FIG_DIR="${FIGURE_ROOT}/${KEY}"
LOG_DIR="${LOG_DIR:-${OUTPUT_ROOT}/logs/${KEY}}"
export LOG_DIR
mkdir -p "${OUTPUT_ROOT}" "${MANIFEST_DIR}" "${PRED_ROOT}" "${PALETTE_DIR}" "${FIG_DIR}" "${LOG_DIR}"

echo "[palettes] generating dataset palette JSON files"
"${PYTHON_BIN}" tools/make_dataset_palettes.py --out-dir "${PALETTE_DIR}"

echo "[manifest] ${DATASET}: ${NUM_SAMPLES} samples"
"${PYTHON_BIN}" tools/build_dataset_manifest.py \
  --dataset "${DATASET}" \
  --num-samples "${NUM_SAMPLES}" \
  --select-mode diverse \
  --data-root "${DATA_ROOT}" \
  --pred-root "${PRED_ROOT}" \
  --palette-dir "${PALETTE_DIR}" \
  --out "${MANIFEST}"

echo "[export] ${DATASET}: 8-GPU sharded inference"
bash tools/export_dataset_8gpu.sh "${MANIFEST}" "${NUM_GPUS}"

echo "[plot] ${DATASET}: one figure per sample"
"${PYTHON_BIN}" tools/plot_paper_results.py \
  --manifest "${MANIFEST}" \
  --out-dir "${FIG_DIR}" \
  --palette-dir "${PALETTE_DIR}" \
  --class-dir configs \
  --show-gt \
  --font "Liberation Serif" \
  --dpi 300

echo "[done] figures: ${FIG_DIR}"