from pathlib import Path
from PIL import Image
src=Path(r"C:\Users\ZHANGB~1\AppData\Local\Temp\codex-clipboard-049bebe8-6df2-40c1-8ad6-f1fd0c25d3e2.png")
out=Path(r"D:\论文\9.27论文\中文论文\绘图\role_functional_text_skeleton\assets")
im=Image.open(src).convert("RGB")
im.crop((38,610,250,720)).save(out/"road_input3.png")
im.crop((350,470,700,615)).save(out/"road_local3.png")
im.crop((347,740,700,830)).save(out/"road_context3.png")