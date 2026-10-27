from pathlib import Path
from PIL import Image
src=Path(r"C:\Users\ZHANGB~1\AppData\Local\Temp\codex-clipboard-049bebe8-6df2-40c1-8ad6-f1fd0c25d3e2.png")
out=Path(r"D:\论文\9.27论文\中文论文\绘图\role_functional_text_skeleton\assets")
out.mkdir(parents=True,exist_ok=True)
im=Image.open(src).convert("RGB")
im.crop((35,610,255,790)).save(out/"road_input.png")
im.crop((350,470,700,680)).save(out/"road_local.png")
im.crop((345,740,700,900)).save(out/"road_context.png")
print(im.size)