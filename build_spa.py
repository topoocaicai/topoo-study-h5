# -*- coding: utf-8 -*-
import os, re, sys

BASE = r"C:\Users\Administrator\WorkBuddy\Claw"
OUT  = os.path.join(BASE, "TopSpace_full_spa.html")

files = {
    "collision": os.path.join(BASE, "TopSpace碰撞H5.html"),
}

# List all H5 files
for f in os.listdir(BASE):
    if f.endswith('.html') and 'TopSpace' in f:
        fp = os.path.join(BASE, f)
        print(f"  {f} ({os.path.getsize(fp)} bytes)")
