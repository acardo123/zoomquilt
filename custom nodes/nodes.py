# nodes.py
#
# Custom ComfyUI nodes for retrieving file paths

from pathlib import Path
from typing import Iterable, Optional, Tuple

# ============================================================
# Generic helpers
# ============================================================

def _parse_exts(exts_str: str) -> Optional[set[str]]:
    if not exts_str or not exts_str.strip():
        return None
    norm: set[str] = set()
    for p in (s.strip() for s in exts_str.split("|")):
        if not p:
            continue
        p = p.lower()
        if not p.startswith("."):
            p = "." + p
        norm.add(p)
    return norm or None


def _iter_matching_files(directory: Path, exts: Optional[set[str]]) -> Iterable[Path]:
    for p in directory.iterdir():
        if p.is_file() and (exts is None or p.suffix.lower() in exts):
            yield p

# ============================================================
# Node: IndexedPath
# ============================================================

class IndexedPath:
    CATEGORY = "Utilities"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)
    FUNCTION = "get_latest_path"

    @classmethod
    def IS_CHANGED(cls, directory, extensions):
        return self.get_latest_path(directory, extensions)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
                "extensions": ("STRING", {"default": "", "tooltip": "File types (e.g. 'png|jpg'). Blank = any."}),
                "index": ("INT", {"default": 0, "min": 0, "max": 99999999, "step": 1}),
            }
        }

    def get_latest_path(self, directory, extensions, index):
        try:
            d = Path(directory).expanduser()
            if not d.exists():
                return (f"Error: directory not found: {d}",)
            if not d.is_dir():
                return (f"Error: not a directory: {d}",)
            exts = _parse_exts(extensions)
            files = list(_iter_matching_files(d, exts))
            files = sorted(files)
            if not files:
                return (f"Error: no matching files in {d}",)

            return (str(files[index]),)
        except Exception as e:
            return (f"Error: {e}",)

# ============================================================
# Node: RandomPath
# ============================================================

class RandomPath:
    CATEGORY = "Utilities"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)
    FUNCTION = "get_latest_path"

    @classmethod
    def IS_CHANGED(cls, directory, extensions):
        return self.get_latest_path(directory, extensions)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
                "extensions": ("STRING", {"default": "", "tooltip": "File types (e.g. 'png|jpg'). Blank = any."})
            }
        }

    def get_latest_path(self, directory, extensions):
        try:
            d = Path(directory).expanduser()
            if not d.exists():
                return (f"Error: directory not found: {d}",)
            if not d.is_dir():
                return (f"Error: not a directory: {d}",)
            exts = _parse_exts(extensions)
            files = list(_iter_matching_files(d, exts))
            if not files:
                return (f"Error: no matching files in {d}",)

            return (str(random.choice(files)),)
        except Exception as e:
            return (f"Error: {e}",)

# ============================================================
# Node: LastModifiedPath
# ============================================================

class LastModifiedPath:
    CATEGORY = "Utilities"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)
    FUNCTION = "get_latest_path"

    @classmethod
    def IS_CHANGED(cls, directory, extensions):
        return self.get_latest_path(directory, extensions)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": ""}),
                "extensions": ("STRING", {"default": "", "tooltip": "File types (e.g. 'png|jpg'). Blank = any."})
            }
        }

    def get_latest_path(self, directory, extensions):
        try:
            d = Path(directory).expanduser()
            if not d.exists():
                return (f"Error: directory not found: {d}",)
            if not d.is_dir():
                return (f"Error: not a directory: {d}",)
            exts = _parse_exts(extensions)
            files = list(_iter_matching_files(d, exts))
            if not files:
                return (f"Error: no matching files in {d}",)
            latest = max(files, key=lambda f: f.stat().st_mtime)
            return (str(latest),)
        except Exception as e:
            return (f"Error: {e}",)
