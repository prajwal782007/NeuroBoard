import os
import shutil
import time

src = 'ai-smart-canvas'
dst = '.'

try:
    if os.path.exists('.git'):
        os.rename('.git', '.git_old')
except Exception as e:
    print("Error renaming .git:", e)

for item in os.listdir(src):
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    try:
        if os.path.isdir(s):
            if not os.path.exists(d):
                shutil.copytree(s, d)
            else:
                # If Dir exists, merge it
                shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
        print("Copied", s, "to", d)
    except Exception as e:
        print("Error moving", s, "->", d, ":", e)

print("Done moving files.")
