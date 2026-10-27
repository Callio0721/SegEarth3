"""Small tqdm-compatible progress helper with a no-dependency fallback."""

from __future__ import annotations

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


def progress(iterable, total=None, desc=None):
    """Iterate with a progress bar when tqdm is available."""
    if tqdm is not None:
        return tqdm(iterable, total=total, desc=desc, ncols=100, leave=True)
    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            total = None

    def _fallback():
        for index, item in enumerate(iterable, 1):
            if total:
                pct = 100.0 * index / total
                print(f"\r[{desc or 'progress'}] {index}/{total} ({pct:5.1f}%)",
                      end="", flush=True)
            else:
                print(f"\r[{desc or 'progress'}] {index}", end="", flush=True)
            yield item
        print()

    return _fallback()