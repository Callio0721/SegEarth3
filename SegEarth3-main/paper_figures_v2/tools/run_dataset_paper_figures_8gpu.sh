#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"

DATASET="${1:-}"
if [[ -z "${DATASET}" ]]; then
  echo "Usage: $0 <dataset> [num_samples]" >&2
  echo "Datasets: LoveDA OpenEarthMap Potsdam Vaihingen iSAID UAVid UDD5 VDD VOC20 Cityscapes" >&2
  exit 2
fi

NUM_SAMPLES="${2:-30}"
OUTPUT_ROOT="${OUTPUT_ROOT:-${REPO_ROOT}/paper_figures_v2}"
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

echo "[stage 1/4] palettes"
"${PYTHON_BIN}" "${SCRIPT_DIR}/make_dataset_palettes.py" --out-dir "${PALETTE_DIR}"

echo "[stage 2/4] manifest: ${DATASET}, ${NUM_SAMPLES} samples"
"${PYTHON_BIN}" "${SCRIPT_DIR}/build_dataset_manifest.py" \
  --dataset "${DATASET}" \
  --num-samples "${NUM_SAMPLES}" \
  --select-mode diverse \
  --data-root "${DATA_ROOT}" \
  --pred-root "${PRED_ROOT}" \
  --palette-dir "${PALETTE_DIR}" \
  --out "${MANIFEST}"

echo "[stage 3/4] export: ${DATASET}, ${NUM_GPUS} GPUs"
bash "${SCRIPT_DIR}/export_dataset_8gpu.sh" "${MANIFEST}" "${NUM_GPUS}"

echo "[stage 4/4] plot: ${DATASET}"
"${PYTHON_BIN}" "${SCRIPT_DIR}/plot_paper_results.py" \
  --manifest "${MANIFEST}" \
  --out-dir "${FIG_DIR}" \
  --palette-dir "${PALETTE_DIR}" \
  --class-dir "${REPO_ROOT}/configs" \
  --show-gt \
  --font "Liberation Serif" \
  --dpi 300

echo "[done] figures: ${FIG_DIR}"