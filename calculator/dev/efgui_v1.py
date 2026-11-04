# Graphical guide cards use the installed TI_DRAW module; text fallback is automatic.
from APCORE import info, wrap
GRAPHICS=[True]
def cards(title,steps):
    pages=[]
    for heading,body in steps:
        lines=wrap(body)
        for i in range(0,len(lines),7): pages.append((heading,lines[i:i+7]))
    page=0
    while page<len(pages):
        heading,lines=pages[page]
        drawn=False
        if GRAPHICS[0]:
            try:
                import ti_draw as d
                d.clear()
                d.set_color(245,248,252)
                d.fill_rect(0,0,320,210)
                d.set_color(20,43,65)
                d.fill_rect(0,0,320,32)
                d.set_color(255,255,255)
                d.draw_text(9,9,(str(page+1)+'/'+str(len(pages))+' '+heading)[:36])
                d.set_color(20,43,65)
                for j in range(len(lines)): d.draw_text(9,43+j*19,lines[j])
                d.set_color(0,104,110)
                d.fill_rect(0,188,320,22)
                d.set_color(255,255,255)
                d.draw_text(9,192,'CLEAR, then ENTER next / 8 prev / 0 exit')
                d.show_draw()
                drawn=True
            except (ImportError,AttributeError,MemoryError): GRAPHICS[0]=False
        if not drawn: info(heading,'\n'.join(lines))
        s=input('ENTER next; 8 prev; 0 exit: ').strip()
        if s in ('0','q','Q'): return
        page=max(0,page-1) if s=='8' else page+1

def sketch(kind):
    try:
        import ti_draw as d
    except ImportError:
        info('Geometry','Ring: x from center along axis. Rod bisector: x perpendicular from midpoint; L is FULL length. Rod axis: x from NEAR END.')
        return
    d.clear()
    d.set_color(20,43,65)
    d.draw_text(8,8,'Ring edge-on' if kind==0 else 'Rod: perpendicular bisector')
    d.set_color(0,104,110)
    d.draw_line(80,48,80,155)
    d.set_color(20,43,65)
    d.draw_line(45,101,285,101)
    d.draw_line(80,48,240,101)
    d.draw_line(80,155,240,101)
    d.fill_circle(240,101,3)
    d.draw_text(245,105,'P')
    d.draw_text(145,110,'x')
    d.draw_text(50,65,'R' if kind==0 else 'L/2')
    d.draw_text(95,58,'r')
    d.draw_text(8,174,'Opposite transverse components cancel.')
    d.show_draw()
