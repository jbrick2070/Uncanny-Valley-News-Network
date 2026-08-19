import json
import random
import time
import subprocess
import os
import glob
import shutil

LAB_DIR = r"C:\Users\jeffr\Documents\ComfyUI\vram-recipe-lab"
RECIPE_PATH = os.path.join(LAB_DIR, "recipes", "ltx_2_5_t2v_gguf.json")
OUTPUT_DIR = os.path.join(LAB_DIR, "outputs", "UVNN", "obs")

PROMPTS = [
    "Dynamic live broadcast footage, a furious news anchor aggressively slamming their fists on the desk while yelling, papers flying through the air, chaotic newsroom background, intense physical action, talking loudly, highly detailed.",
    "Dynamic live broadcast footage, a panicked weatherman pointing erratically at a map of a nonexistent continent that is actively catching fire, dramatic studio lighting, talking fast, highly detailed.",
    "Dynamic action shot, a sports commentator jumping out of their chair and screaming in disbelief as a giant snail crosses a finish line, talking energetically, highly detailed.",
    "Dynamic action shot, an enthusiastic infomercial host aggressively demonstrating how to use a blender that is also a bird, wild gestures, fast talking, highly detailed."
]

def generate_slop():
    with open(RECIPE_PATH, "r") as f:
        graph = json.load(f)
    
    chosen_prompt = random.choice(PROMPTS)
    graph["prompt"]["5"]["inputs"]["text"] = chosen_prompt
    
    tmp_recipe = os.path.join(LAB_DIR, "recipes", "tmp_uvnn_slop.json")
    with open(tmp_recipe, "w") as f:
        json.dump(graph, f, indent=2)
        
    print(f"[UVNN] Broadcasting: {chosen_prompt}")
    
    cmd = [
        os.path.join(LAB_DIR, ".venv", "Scripts", "python.exe"),
        "run_recipe.py",
        "recipes\\tmp_uvnn_slop.json",
        "--clamp", "14.5"
    ]
    subprocess.run(cmd, cwd=LAB_DIR)
    
    # Grab the newest mp4 and move it to the OBS folder
    list_of_files = glob.glob(os.path.join(LAB_DIR, 'outputs', 'ltx_2_5_gguf*.mp4'))
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        dest = os.path.join(OUTPUT_DIR, f"uvnn_slop_{int(time.time())}.mp4")
        shutil.copy(latest_file, dest)
        print(f"[UVNN] Saved segment to {dest}")

if __name__ == "__main__":
    print("Starting UVNN 24/7 Broadcast Generator...")
    while True:
        generate_slop()
