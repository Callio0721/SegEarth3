#!/usr/bin/env bash
set -euo pipefail

MANIFEST="${1:-}"
NUM_GPUS="${2:-8}"
if [[ -z "${MANIFEST}" ]]; then
  echo "Usage: $0 <manifest.csv> [num_gpus]" >&2
  exit 2
fi

PYTHON_BIN="${PYTHON_BIN:-python}"
STEM="$(basename "${MANIFEST}" .csv)"
LOG_DIR="${LOG_DIR:-paper_figures_v2/logs/${STEM}}"
mkdir -p "${LOG_DIR}"

pids=()
for ((gpu=0; gpu<NUM_GPUS; gpu++)); do
  echo "[launch] gpu=${gpu} shard=${gpu}/${NUM_GPUS}"
  CUDA_VISIBLE_DEVICES="${gpu}" \
  PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-max_split_size_mb:128}" \
  "${PYTHON_BIN}" tools/export_paper_predictions.py \
    --manifest "${MANIFEST}" \
    --mode both \
    --num-shards "${NUM_GPUS}" \
    --shard-id "${gpu}" \
    ${OVERWRITE:+--overwrite} \
    > "${LOG_DIR}/gpu${gpu}.log" 2>&1 &
  pids+=("$!")
done

status=0
for pid in "${pids[@]}"; do
  if ! wait "${pid}"; then
    status=1
  fi
done

echo "[logs] ${LOG_DIR}"
if [[ "${status}" -ne 0 ]]; then
  echo "[error] at least one shard failed; inspect GPU logs" >&2
  exit "${status}"
fi
echo "[done] all shards finished"