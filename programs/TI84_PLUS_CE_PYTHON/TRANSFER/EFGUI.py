GRAPHICS=[True]
WIDTH=28
ROWS=4
TEXT_ASCENT=0
SAFE_TOP=32
TITLE_Y=SAFE_TOP+TEXT_ASCENT
BODY_Y=78
LINE_STEP=22
KEYMAP={}
def wrap_at(text,width=WIDTH):
 lines=[]
 for para in str(text).split('\n'):
  current=''
  for word in para.split(' '):
   if not word:continue
   while len(word)>width:
    if current:lines.append(current);current=''
    depth=0;cuts=[]
    for i in range(width):
     c=word[i]
     if c in '([':depth+=1
     elif c in ')]':depth-=1
     elif depth==0 and c in '/=+-*' and i>=width//3:
      cuts.append(i+1)
    cut=cuts[-1]if cuts else width
    lines.append(word[:cut]);word=word[cut:]
   if current and len(current)+1+len(word)>width:
    lines.append(current);current=''
   if word:current=(current+' '+word)if current else word
  lines.append(current)
 return lines
def raw_key():
 from ti_system import wait_key
 while True:
  code=wait_key()
  if code is not None and code!=0 and(code!=''):
   return code
def key_action(code):
 if code in KEYMAP:
  return KEYMAP[code]
 if isinstance(code,str):
  code=code.strip().lower()
  if code in('0','q','b','clear','esc'):
   return 'back'
  if code in('8','left'):
   return 'prev'
  if code in('9','right'):
   return 'next'
  if code in('up','down','enter'):
   return code
  if code in('1','2','3','4','5'):
   return code
  return ''
 if code in(9,62):
  return 'back'
 if code in(13,5):
  return 'enter'
 if code in(14,2,250):
  return 'prev'
 if code in(15,1,251):
  return 'next'
 if code==3:
  return 'up'
 if code==4:
  return 'down'
 if 243<=code<=247:
  return str(code-242)
 return ''
def event():
 try:
  import ti_system
 except ImportError:
  s=input('> ').strip().lower()
  return 'enter' if s=='' else key_action(s)
 while True:
  action=key_action(raw_key())
  if action:return action
def frame(title,lines,page,total,highlight=None,reading=False):
 heading=wrap_at(title)
 while len(heading)<2:heading.append('')
 foot1='ENTER/RIGHT next  LEFT prev' if reading else 'UP/DOWN choose  ENTER open'
 foot2='0/CLEAR back  '+str(page+1)+'/'+str(total)
 if GRAPHICS[0]:
  try:
   import ti_draw as d
   d.clear();d.set_color(255,255,255);d.fill_rect(0,0,320,210)
   d.set_color(20,43,65)
   d.draw_text(8,TITLE_Y,heading[0]);d.draw_text(8,TITLE_Y+18,heading[1])
   if highlight is not None:
    d.set_color(205,234,238)
    d.fill_rect(4,BODY_Y-TEXT_ASCENT-3+LINE_STEP*highlight[0],312,LINE_STEP*highlight[1])
   d.set_color(20,43,65)
   for i in range(len(lines)):d.draw_text(8,BODY_Y+LINE_STEP*i,lines[i])
   d.set_color(70,85,95)
   d.draw_text(8,168,foot1);d.draw_text(8,186,foot2)
   return
  except(ImportError,AttributeError,MemoryError):GRAPHICS[0]=False
 from APCORE import disp_clr
 disp_clr()
 print(heading[0]);print(heading[1])
 for i in range(ROWS):
  line=lines[i]if i<len(lines)else ''
  if highlight is not None and i==highlight[0]and line:line='>'+line[1:]
  print(line)
 print(foot1);print(foot2)
def menu_pages(items):
 pages=[];page=[];used=0
 for index,item in enumerate(items):
  lines=wrap_at(item,WIDTH-2)
  while lines:
   chunk=lines[:ROWS];lines=lines[ROWS:]
   if page and used+len(chunk)>ROWS:pages.append(page);page=[];used=0
   page.append((index,chunk));used+=len(chunk)
   if lines:pages.append(page);page=[];used=0
 if page:pages.append(page)
 return pages
def choose(title,items):
 if not items:return-1
 pages=menu_pages(items);page=0;selected=0
 while True:
  entries=pages[page];lines=[];mark=(0,1)
  for i,(index,parts)in enumerate(entries):
   if i==selected:mark=(len(lines),len(parts))
   lines.append(str(i+1)+' '+parts[0])
   for part in parts[1:]:lines.append('  '+part)
  frame(title,lines,page,len(pages),mark)
  key=event()
  if key=='back':return-1
  if key=='enter':return entries[selected][0]
  if key in('1','2','3','4','5')and int(key)<=len(entries):return entries[int(key)-1][0]
  if key in('next','prev'):
   page=(page+(1 if key=='next' else-1))%len(pages);selected=0
  elif key=='down':
   if selected+1<len(entries):selected+=1
   else:page=(page+1)%len(pages);selected=0
  elif key=='up':
   if selected:selected-=1
   else:page=(page-1)%len(pages);selected=len(pages[page])-1
def cards(title,steps):
 pages=[]
 for heading,body in steps:
  lines=wrap_at(body)
  for start in range(0,len(lines),ROWS):pages.append((heading,lines[start:start+ROWS]))
 page=0
 while pages:
  heading,lines=pages[page]
  frame(heading,lines,page,len(pages),reading=True)
  key=event()
  if key=='back':return
  if key in('prev','up'):page=max(0,page-1)
  elif key in('next','down','enter'):
   if page==len(pages)-1:return
   page+=1
def read(title,text):cards(title,[(title,text)])
def sketch(kind):
 try:
  import ti_draw as d
 except ImportError:
  read('Geometry','Ring: x from center along axis. Rod bisector: x perpendicular from midpoint; L is FULL length. Rod axis: x from NEAR END.')
  return
 d.clear()
 d.set_color(20,43,65)
 d.draw_text(8,TITLE_Y,'Ring edge-on' if kind==0 else 'Rod: perpendicular bisector')
 d.set_color(0,104,110)
 d.draw_line(80,70,80,155)
 d.set_color(20,43,65)
 d.draw_line(45,101,285,101)
 d.draw_line(80,70,240,101)
 d.draw_line(80,155,240,101)
 d.fill_circle(240,101,3)
 d.draw_text(245,87,'P')
 d.draw_text(145,92,'x')
 d.draw_text(50,72,'R' if kind==0 else 'L/2')
 d.draw_text(95,62,'r')
 d.draw_text(8,168,'Transverse fields cancel.')
 d.draw_text(8,186,'Axial fields add.')
 d.show_draw()
