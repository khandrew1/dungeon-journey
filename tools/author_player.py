from PIL import Image,ImageDraw
from pathlib import Path
import json
p=Path(__file__).resolve().parent.parent;src=p/'source-art/player';src.mkdir(exist_ok=True)
front=['................','.....DDDDDD.....','....DLLLLLLD....','...DLLLLLLLLD...','..DLLLLLLLLLLD..','..DLLDLLLDLLLD..','..DLLDLLLDLLLD..','...DLLLLLLLLD...','....DLLDDLLD....','.....DMMMMD.....','...DLMMMMMMLD...','...DDMMMMMMDD...','.....DDDDDD.....','.....DMDMD......','.....DDDDD......','....DDD.DDD.....']
back=front.copy();back[5]='..DLLLLLLLLLLD..';back[6]='..DLLLLLLLLLLD..';back[8]='....DDDDDDDD....'
side=['................','.....DDDDD......','....DLLLLLD.....','...DLLLLLLLD....','...DLLLLLLLLD...','...DLLLLLDLLD...','...DLLLLLDLLD...','....DLLLLLLD....','.....DLLDDD.....','.....DMMMD......','....DMMMMLD.....','....DDMMMDD.....','.....DDDDD......','.....DMDMD......','.....DDDDD......','....DDDDDDD.....']
source={'.':'#65ff00','D':'#071821','M':'#86c06c','L':'#e0f8cf'};palette={'.':None,'D':'#252D39','M':'#3F70B0','L':'#DDC487'}
images=[];frames=[];pixelrows={}
for name,base in [('down',front),('up',back),('right',side)]:
 for phase in range(2):
  rows=base.copy()
  if phase:
   if name=='right':rows[13]='.....DMMDD......';rows[14]='....DDD.DDD.....';rows[15]='....DD...DDD....'
   else:rows[13]='.....DDDDD......';rows[14]='....DDD.DDD.....';rows[15]='.....DD..DD.....';rows[10]='....LMMMMMMLD...';rows[11]='....DMMMMMMD....'
  assert len(rows)==16 and all(len(r)==16 for r in rows)
  pixelrows[name+'-'+str(phase)]=rows
  native=Image.new('RGB',(16,16));art=Image.new('RGBA',(16,16))
  for y,row in enumerate(rows):
   for x,c in enumerate(row):
    native.putpixel((x,y),tuple(bytes.fromhex(source[c][1:])))
    if c!='.':art.putpixel((x,y),tuple(bytes.fromhex(palette[c][1:]))+(255,))
  native.save(src/f'{name}-{phase}-native.png');art.save(src/f'{name}-{phase}-color.png');frames.append(native);images.append(art)
sheet=Image.new('RGB',(96,16))
for i,im in enumerate(frames):sheet.paste(im,(16*i,0))
sheet.save(p/'assets/sprites/bald_blue_player.png')
(src/'pixels-and-timing.json').write_text(json.dumps({'frameSize':[16,16],'frames':pixelrows,'sourcePalette':source,'displayPalette':palette,'left':'mirrored right','previewDurationMs':180,'approvedIdentity':'bald, blue shirt, vertical eyes, no eyebrows'},indent=2))
board=Image.new('RGB',(800,320),'#F0EDE5');d=ImageDraw.Draw(board)
d.text((20,18),'BALD / BLUE SHIRT - ACTUAL 16 x 16 GAME SPRITE',fill='#252D39')
for j,name in enumerate(['DOWN','UP / BALD REAR','RIGHT / LEFT MIRRORED']):
 d.text((20+j*255,50),name,fill='#252D39')
 for ph in range(2):
  a=images[j*2+ph].resize((112,112),Image.Resampling.NEAREST);board.paste(a,(20+j*255+ph*116,80),a)
 d.text((20+j*255,210),'idle                 walk',fill='#252D39')
d.text((20,260),'Native 1x:',fill='#252D39')
for i,im in enumerate(images):board.paste(im,(95+i*30,260),im)
board.save(src/'bald-blue-sprite-sheet.png')
gif=[]
for ph in [0,1]:
 out=Image.new('RGB',(640,220),'#F0EDE5');d=ImageDraw.Draw(out)
 for j in range(4):
  im=images[(0 if j==0 else 2 if j==1 else 4)+ph] if j<3 else images[4+ph].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  a=im.resize((128,128),Image.Resampling.NEAREST);out.paste(a,(j*160+16,50),a);d.text((j*160+20,20),['DOWN','UP','RIGHT','LEFT'][j],fill='#252D39')
 gif.append(out)
gif[0].save(src/'bald-blue-walking.gif',save_all=True,append_images=gif[1:],duration=180,loop=0,disposal=2)
