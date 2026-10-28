from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
p=Path('work/ZR4-20261011')
for name in ('seq','xor','combo','game'):
    files=sorted(p.glob(name+'-*.png'))
    cols=2
    rows=(len(files)+cols-1)//cols
    w,h=650,940
    out=Image.new('RGB',(cols*w,rows*h),(215,224,232))
    dr=ImageDraw.Draw(out)
    for i,f in enumerate(files):
        im=Image.open(f).convert('RGB')
        im.thumbnail((w-18,h-30))
        x=(i%cols)*w+(w-im.width)//2
        y=(i//cols)*h+22
        out.paste(im,(x,y))
        dr.text(((i%cols)*w+12,(i//cols)*h+5),f'{name} page {i+1}',fill=(20,45,65))
    out.save(p/(name+'-contact.png'))
