from __future__ import annotations
import json
import os
import glob
import shutil
import time
import subprocess
from typing import Optional

from .backend_base import VideoBackend

class LTX25Backend(VideoBackend):
    def __init__(self, lab_dir: str = r"C:\Users\jeffr\Documents\ComfyUI\vram-recipe-lab"):
        self.lab_dir = lab_dir
        self.recipe_path = os.path.join(self.lab_dir, "recipes", "ltx_2_5_t2v_gguf.json")
        self.output_dir = os.path.join(self.lab_dir, "outputs", "UVNN", "obs")
        
        # Ensure OBS output dir exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Use ComfyUI's main venv python if present, else fallback
        comfy_venv_py = r"C:\Users\jeffr\Documents\ComfyUI\.venv\Scripts\python.exe"
        lab_venv_py = os.path.join(self.lab_dir, ".venv", "Scripts", "python.exe")
        
        if os.path.exists(lab_venv_py):
            self.python_exe = lab_venv_py
        elif os.path.exists(comfy_venv_py):
            self.python_exe = comfy_venv_py
        else:
            self.python_exe = "python"

    def generate_segment(self, prompt: str) -> Optional[str]:
        if not os.path.exists(self.recipe_path):
            print(f"[LTX25Backend] Recipe not found: {self.recipe_path}")
            return None
            
        with open(self.recipe_path, "r") as f:
            graph = json.load(f)
        
        # Node "5" is the positive prompt in ltx_2_5_t2v_gguf.json
        graph["prompt"]["5"]["inputs"]["text"] = prompt
        
        tmp_recipe = os.path.join(self.lab_dir, "recipes", "tmp_uvnn_slop.json")
        with open(tmp_recipe, "w") as f:
            json.dump(graph, f, indent=2)
            
        print(f"[LTX25Backend] Dispatching to vram-recipe-lab for LTX-2.5 generation...")
        
        cmd = [
            self.python_exe,
            "run_recipe.py",
            "recipes\\tmp_uvnn_slop.json",
            "--clamp", "14.5"
        ]
        
        try:
            subprocess.run(cmd, cwd=self.lab_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[LTX25Backend] run_recipe.py failed with exit code {e.returncode}")
            return None
        
        # Grab the newest mp4
        list_of_files = glob.glob(os.path.join(self.lab_dir, 'outputs', 'ltx_2_5_gguf*.mp4'))
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
            dest = os.path.join(self.output_dir, f"uvnn_segment_{int(time.time())}.mp4")
            shutil.copy(latest_file, dest)
            print(f"[LTX25Backend] Saved segment to {dest}")
            return dest
            
        return None
