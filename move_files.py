import os
import shutil

src = 'ai-smart-canvas'
dst = '.'

if os.path.exists('.git'):
    # Try to safely remove if it's empty or handle permission gracefully
    import stat
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree('.git', onerror=remove_readonly)

for item in os.listdir(src):
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    if os.path.exists(d):
        if os.path.isdir(d):
            shutil.rmtree(d, onerror=remove_readonly)
        else:
            os.remove(d)
    shutil.move(s, d)

if not os.listdir(src):
    os.rmdir(src)
