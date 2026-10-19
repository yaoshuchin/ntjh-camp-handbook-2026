# -*- coding: utf-8 -*-
import pypdf
import os

reader = pypdf.PdfReader('115南投國二露營手冊.pdf')
out_dir = 'assets/img/extracted'
os.makedirs(out_dir, exist_ok=True)

img_count = 0
for page_num, page in enumerate(reader.pages):
    for img_name, img_obj in page.images.items():
        clean_name = img_name.replace('/', '_').replace('\\', '_')
        out_path = os.path.join(out_dir, f"p{page_num+1}_{clean_name}")
        with open(out_path, "wb") as f:
            f.write(img_obj.data)
        img_count += 1
        print(f"Page {page_num+1}: saved {out_path} ({len(img_obj.data)} bytes)")

print(f"Total extracted: {img_count}")
