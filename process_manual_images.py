# -*- coding: utf-8 -*-
from PIL import Image
import os

extracted_dir = 'assets/img/extracted'

def convert_to_img(src_file, out_name):
    src = os.path.join(extracted_dir, src_file)
    if os.path.exists(src):
        try:
            im = Image.open(src)
            out_path = os.path.join('assets/img', out_name)
            im.convert('RGB').save(out_path, 'JPEG', quality=90)
            print(f"Saved {out_path} ({im.size})")
        except Exception as e:
            print(f"Error {src_file}: {e}")

# 1. 營地建設與屋式帳
convert_to_img('p13__Image130', 'tent_pitch_guide.jpg')
# 2. 童軍常用八大繩結
convert_to_img('p15__Image145', 'rope_knots_manual.jpg')
# 3. 自然方向辨識 (16 方位盤)
convert_to_img('p17__Image152', 'direction_16_compass.jpg')
# 4. 毒蛇 (百步蛇與雨傘節)
# Let's combine p16__Image148 and p16__Image149 into one comparison image
try:
    im1 = Image.open(os.path.join(extracted_dir, 'p16__Image148')).convert('RGB')
    im2 = Image.open(os.path.join(extracted_dir, 'p16__Image149')).convert('RGB')
    # Resize to same height
    h = max(im1.height, im2.height)
    w1 = int(im1.width * (h / im1.height))
    w2 = int(im2.width * (h / im2.height))
    im1_r = im1.resize((w1, h), Image.Resampling.LANCZOS)
    im2_r = im2.resize((w2, h), Image.Resampling.LANCZOS)
    combo = Image.new('RGB', (w1 + w2 + 10, h), (255, 255, 255))
    combo.paste(im1_r, (0, 0))
    combo.paste(im2_r, (w1 + 10, 0))
    combo.save('assets/img/snakes_manual.jpg', 'JPEG', quality=92)
    print(f"Saved assets/img/snakes_manual.jpg ({combo.size})")
except Exception as e:
    print("Error combining snake images:", e)
