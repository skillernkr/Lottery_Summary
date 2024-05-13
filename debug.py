#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 23:48:14 2024

@author: 2024, K. R. Skillern, Jr., All Rights Reserved

debug.py - Debug Tools 

Purpose:  Assist in monitoring flow of application by information output.

To Do:
    Add color
"""
# references:
# Python - Printing on same line:  https://stackoverflow.com/questions/5419389/how-to-overwrite-the-previous-print-to-stdout
# Python - Terminal control:  https://code.activestate.com/recipes/475116/    
# Python - How to Print on Same Line:  https://tech.sadaalomma.com/python/how-to-print-on-same-line-python/#google_vignette
# Python - How do I print colored text to the terminal?:  https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
# VGA terminal & emulator colors:  https://en.wikipedia.org/wiki/ANSI_escape_code#Colors



# Python - function key word arguments:
    # In [000]: def f(*s, **kwargs):
    #               for t in s:
    #                   for k, v in kwargs.items():
    #                       print(f"t={t}, k={k}, v={v}")
                

    # In [001]: f("ab", "cd", "ef", a=1, b=2, c=3)
    # t=ab, k=a, v=1
    # t=ab, k=b, v=2
    # t=ab, k=c, v=3
    # t=cd, k=a, v=1
    # t=cd, k=b, v=2
    # t=cd, k=c, v=3
    # t=ef, k=a, v=1
    # t=ef, k=b, v=2
    # t=ef, k=c, v=3
"""
def print_format_table():

    # prints table of formatted text format options

    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')

print_format_table()
print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')

Tests on spyder iPython console:    
    CSI = "\x1B["
    print(CSI + "31;40m" + "Colored Text" + CSI + "0m")
    Colored Text (red on black)
    
    print(CSI+"1;3;32;100m" + "Colored Text" + CSI + "0m")
    Colored Text (bright green on gray - matches spyder iPython console)
    
    print(CSI+"32;100m" + "Colored Text" + CSI + "0m")
    Colored Text (dark green on gray - matches spyder iPython console)
    
    print(CSI + "3;31;100m" + "Colored Text" + CSI + "0m")
    Colored Text (italic red on gray - matches spyder iPython console)
    
    print(CSI + "1;3;31;100m" + "Colored Text" + CSI + "0m")
    Colored Text (italic bright red on gray - matches spyder iPython console)

    print(CSI + "3;43;32m" + "Colored" +  CSI + "38;2;80;200;80m" + " Text" + CSI + "0m")
    Colored Text (italic dark green with lighter green on red background)

SGR (Select Graphic Rendition) parameters
    The control sequence 
        CSI n m
    named Select Graphic Rendition (SGR), sets display attributes. 
    Several attributes can be set in the same sequence, separated by semicolons.
    Each display attribute remains in effect until a following occurrence of SGR resets it.
    If no codes are given, CSI m is treated as CSI 0 m (reset / normal).

n	Name  	                            Note
0	Reset or normal	                    All attributes become turned off
1	Bold or increased intensity	        As with faint, the color change is a PC (SCO / CGA) invention.
2	Faint, decreased intensity, or dim	May be implemented as a light font weight like bold.
3	Italic	                            Not widely supported. Sometimes treated as inverse or blink.
4	Underline	                        Style extensions exist for Kitty, VTE, mintty, iTerm2 and Konsole.
5	Slow blink	                        Sets blinking to less than 150 times per minute.
6	Rapid blink	                        MS-DOS ANSI.SYS, 150+ per minute; not widely supported.
7	Reverse video or invert	            Swap foreground and background colors; inconsistent emulation.
8	Conceal or hide	                    Not widely supported.
9	Crossed-out, or strike	            Characters legible but marked as if for deletion. Not supported in Terminal.app.
10	Primary (default) font	
11–19	Alternative font	                Select alternative font n − 10
20	Fraktur (Gothic)	                    Rarely supported
21	Doubly underlined; or: not bold	    Double-underline per ECMA-48,: 8.3.117  but instead disables bold intensity on several terminals, including in the Linux kernel's console before version 4.17.
22	Normal intensity	                    Neither bold nor faint; color changes where intensity is implemented as such.
23	Neither italic, nor blackletter	
24	Not underlined	                    Neither singly nor doubly underlined
25	Not blinking	                        Turn blinking off
26	Proportional spacing	                ITU T.61 and T.416, not known to be used on terminals
27	Not reversed	
28	Reveal	                            Not concealed
29	Not crossed out	
30–37	Set foreground color	
38	Set foreground color	                Next arguments are 5;n or 2;r;g;b
39	Default foreground color	            Implementation defined (according to standard)
40–47	Set background color	
48	Set background color         	    Next arguments are 5;n or 2;r;g;b
49	Default background color	            Implementation defined (according to standard)
50	Disable proportional spacing	T.61 and T.416
51	Framed	                            Implemented as "emoji variation selector" in mintty.
52	Encircled
53	Overlined	                        Not supported in Terminal.app
54	Neither framed nor encircled	
55	Not overlined	
58	Set underline color	                Not in standard; implemented in Kitty, VTE, mintty, and iTerm2. Next arguments are 5;n or 2;r;g;b.
59	Default underline color	            Not in standard; implemented in Kitty, VTE, mintty, and iTerm2.
60	Ideogram underline or right side line	Rarely supported
61	Ideogram double underline, or double line on the right side
62	Ideogram overline or left side line
63	Ideogram double overline, or double line on the left side
64	Ideogram stress marking
65	No ideogram attributes	            Reset the effects of all of 60–64
73	Superscript	                        Implemented only in mintty
74	Subscript
75	Neither superscript nor subscript
90–97	Set bright foreground color	    Not in standard; originally implemented by aixterm
100–107	Set bright background color

Colors
3-bit and 4-bit
The original specification only had 8 colors, and just gave them names. 
The SGR parameters 30–37 selected the foreground color, while 40–47 
selected the background. 
Quite a few terminals implemented "bold" (SGR code 1) as a brighter color 
rather than a different font, thus providing 8 additional foreground colors. 
Usually you could not get these as background colors, though sometimes 
inverse video (SGR code 7) would  allow that. 
Examples: 
    to get black letters on white background use ESC[30;47m 
    to get red use ESC[31m
    to get bright red use ESC[1;31m
To reset colors to their defaults, use ESC[39;49m (not supported on some 
terminals), or reset all attributes with ESC[0m. Later terminals added the 
ability to directly specify the "bright" colors with 90–97 and 100–107.

VGA 
FG	BG	Color Name             (r,   g,   b)
30	40	Black	                0,   0,   0	
31	41	Red	                  170,   0,   0	
32	42	Green	                0, 170,   0	
33	43	Yellow	              170,  85,   0 
34	44	Blue	                    0,   0, 170	
35	45	Magenta	              170,   0, 170	
36	46	Cyan	                    0, 170, 170
37	47	White	              170, 170, 170
90	100	Bright Black (Gray)	   85,  85,  85	
91	101	Bright Red	          255,  85,  85	
92	102	Bright Green	           85, 255,  85	
93	103	Bright Yellow	      255, 255,  85	
94	104	Bright Blue	           85,  85, 255	
95	105	Bright Magenta	      255,  85, 255	
96	106	Bright Cyan	           85, 255, 255	
97	107	Bright White          255, 255, 255

"""
from datetime import datetime

# CONSTANTS:
# “clear to end of line” escape sequence, '\x1b[1K' ('\x1b' = ESC)
TERMINAL_ESC_RETURN = '\x1b[1K\r' 

FG_COLORS =   { 0: {'name': 'black',    'code': '30'},
                1: {'name': 'red',      'code': '31'},
                2: {'name': 'green',    'code': '32'},
                3: {'name': 'yellow',   'code': '33'},
                4: {'name': 'blue',     'code': '34'},
                5: {'name': 'magenta',  'code': '35'},
                6: {'name': 'cyan',     'code': '36'},
                7: {'name': 'white',    'code': '37'},
                8: {'name': 'rgb',      'code': '38;2'},
                9: {'name': 'default',  'code': '39'}
                }

BG_COLORS =   { 0: {'name': 'black',    'code': '40'},
                1: {'name': 'red',      'code': '41'},
                2: {'name': 'green',    'code': '42'},
                3: {'name': 'yellow',   'code': '43'},
                4: {'name': 'blue',     'code': '44'},
                5: {'name': 'magenta',  'code': '45'},
                6: {'name': 'cyan',     'code': '46'},
                7: {'name': 'white',    'code': '47'},
                8: {'name': 'rgb',      'code': '48;2'},
                9: {'name': 'default',  'code': '49'},
               10: {'name': 'grey',     'code': '100'}
                }

TEXT_STYLES = { 0: {'name': 'normal',   'code': '0'},
                1: {'name': 'bright',   'code': '1'},
                2: {'name': 'dim',      'code': '2'},
                3: {'name': 'italic',   'code': '3'},
                4: {'name': 'underline','code': '4'}
                }


# CLASSES:
class console_command:
    cc_ESC = "\x1b["
    cc_RETURN = "1K\r"
    cc_START_CODE = cc_ESC 
    cc_END_CODE = "m"
    cc_RESET_CODE = cc_ESC + "0" + cc_END_CODE
    
# class console_color:
#     fg_black = "30"
#     fg_red = "31"
#     fg_green = "32"
#     fg_yellow = "33"
#     fg_blue = "34"
#     fg_magenta = "35"
#     fg_cyan = "36"
#     fg_white = "37"
#     fg_rgb = "38;2" # next ;r;g;b m 0-255
#     fg_default = "39"
#     bg_black = "40"
#     bg_red = "41"
#     bg_green = "42"
#     bg_yellow = "43"
#     bg_blue = "44"
#     bg_magenta = "45"
#     bg_cyan = "46"
#     bg_white = "47"    
#     bg_default = "49"
#     bg_grey = "100"
    
# class console_style:
#     st_normal = "0"
#     st_bright = "1"
#     st_dim = "2"
#     st_normal = "22"
#     st_italic = "3"
#     st_underline = "4"
    
# FUNCTIONS:
def cc_code(dx, name):
    """
    Parameters
    ----------
    dx : dictionary of codes.
    name : name for desired code lookup.
    
    Returns
    -------
    code : console code value.

    Examples
    --------
               code = cc_code(FG_COLORS, 'rgb(0,100,0)')
               code = cc_code(BG_COLORS, 'black')
               code = cc_code(TEXT_STYLES, 'italic')
    """
    code = ''        
    names = name.replace(" ", "").split(';')
    # print(f"len(dx)={len(dx)}, name={name}, names={names}")
    for i in range(len(dx)):  
        for name in names:
            # print(f"dx[{i}]={dx[i]}, name={name}, names={names}")
            if dx[i]['name'] == name:
                code += f"{dx[i]['code']};"
                # print(f"code={code}")
                # break
            else:
                if name[:3] == 'rgb' and dx[i]['name'] == name[:3]:
                    # special handling for rgb 
                    # parse string (r,g,b)
                    rgb = name[3:len(name)].strip('()').split(',')
                    # print(f"rgb={rgb}")
                    code += f"{dx[i]['code']};{rgb[0]};{rgb[1]};{rgb[2]};"
                    # print(f"code={code}")
                    # break
    # print(f"final code={code}")            
    return code
                
            
def debug_output(*s, **kwargs):
    """
    Parameters
    ----------
    message : string
    **kwargs : 'begin=' string; default = ""; printed on line first,
                                            can be set to TERMINAL_ESC_RETURN to
                                            continuously print on same line with sequence 
               'end=' string; default = "\n" (line feed); appended to end of s
               'color_fg=' string; default = "white"; color of text foreground
               'color_bg=' string; default = "black"; color of text background
               'showTime=' True/False; default = True; print time stamp at 
                                                 beggining of line.

    CONSTANTS
    ----------
    TERMINAL_ESC_RETURN = '\x1b[1K\r'; print on same line on console repeatedly;
                                       “clear to end of line” escape sequence,
                                       ('\x1b' = ESC)

    Returns
    -------
    txt_output : formatted string containing message sent to console line

    example:  default message output
        In:  debug_output("message")
        Out: '2024-04-23 00:07:29: message'
        
    example:  overwrite output on last line with new message
        In:  debug_output("message", end=TERMINAL_ESC_RETURN)
        2024-04-23 00:16:59: messageOut[93]: '2024-04-23 00:16:59: message'
        
    example:  colors and styles
        In:  dbg.debug_output('Item 1', 'Item 2', color_fg='white', color_bg='grey', style='italic; underline')
        Out: '2024-05-10 15:21:44: Item 1, Item 2' (colored italic underlined) 
    
    example:  rgb colors and styles
        In:  dbg.debug_output('Item 1', 'Item 2', color_fg='rgb(25,25,200)', color_bg='grey', style='italic; underline')
        Out: '2024-05-10 15:30:13: Item 1, Item 2' (colored italic underlined)
    """
    txt_time = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: "  
    txt = ""
    for t in s:
        txt += f"{t}, " 
    txt = txt[:-2] # strip off last ", "
    txt_color_fg = ""
    txt_color_bg = ""
    txt_style = ""
    txt_cc_join = ""
    txt_cc_start = ""
    txt_cc_end = ""
    txt_cc_reset = ""
    txt_begin_value = ""
    txt_end_value = "\n"
    
    # txt_begin_value = ""
    # endValue = "\n"
    for key, value in kwargs.items():
        # print(f"key={key}, value={value}")
        if key == "begin":
            txt_begin_value = value;
        if key == "end":
            txt_end_value = value
        if key == "showTime":
            if not value:
                # do not show time
                txt_time = ""             
        if key in ["color_fg", "color_bg", "style"]:   
            txt_cc_start = console_command.cc_START_CODE
            txt_cc_end = console_command.cc_END_CODE
            txt_cc_reset = console_command.cc_RESET_CODE
            if key == "color_fg":
                txt_color_fg = cc_code(FG_COLORS, value) 
            if key == "color_bg":
                txt_color_bg = cc_code(BG_COLORS, value) 
            if key == "style":
                txt_style = cc_code(TEXT_STYLES, value) 
            
    # default txt_output unless modified below
    # to do:  add modifiers
    # txt_output = txt_time + txt
    
    count = 0
    if len(txt_color_fg) > 0:
        count += 1
    if len(txt_color_bg) > 0:
        count += 1
    if len(txt_style) > 0:
        count += 1
            
    if count > 1:
        txt_cc_join = ";"
    
    
    txt_output = txt_time + (
                            txt_cc_start + 
                            txt_color_fg + 
                            txt_cc_join + 
                            txt_color_bg + 
                            txt_cc_join + 
                            txt_style + 
                            txt_cc_end + 
                            txt + 
                            txt_cc_reset
                            )
    
    # print txt_begin_value to console first - allows printing on same line continously
    # if 'begin' set to TERMINAL_ESC_RETURN        
    print("", end=txt_begin_value)
    # print txt to console
    print(txt_output, end=txt_end_value, flush=True)

    return txt_output

