from __future__ import print_function
import os
import sys
import time
import math

nyan_frames = [
    [
        r'~,------,  ',
        r'~|   /\_/\ ',
        r'~|__( ^ .^)',
        r'  ""  ""   ',
    ],[
        r'-,------,  ',
        r'-|  /\_/\  ',
        r'-|_( ^ .^) ',
        r' ""  ""    ',
    ],
]
nyan_height = len(nyan_frames[0])

def clear():
    os.system('tput reset')

def get_print_color(text, red, green, blue):
    return '\x1b[38;5;%dm' % (16 + (red * 36) + (green * 6) + blue) + text + '\x1b[0m'

def get_nyan_frame(initial_frame, line):
    return nyan_frames[int(initial_frame)][line]

def get_rainbow_colors(rainbow_length):
    center = 128
    width = 127
    frequency = math.pi * 2 / rainbow_length

    colors = []
    for i in range(rainbow_length):
        colors.append((
            math.floor((math.sin(frequency * i + 2) * width + center) / 42.51),
            math.floor((math.sin(frequency * i + 0) * width + center) / 42.51),
            math.floor((math.sin(frequency * i + 4) * width + center) / 42.51)
        ))

    return colors

def clear_buffer(length=nyan_height):
    return [[] for x in xrange(nyan_height)]

initial_frame = True
rainbow_length = 10
terminal_width = map(int, os.popen('stty size', 'r').read().split())[1]
colors = get_rainbow_colors(terminal_width)
draw_buffer = clear_buffer()

def split_buffer():
    cutoff = terminal_width
    for line in range(len(draw_buffer)):
        draw_buffer[line] = [draw_buffer[line][x:x+cutoff] for x in xrange(0, len(draw_buffer[line]), cutoff)]

while True:
    clear()
    terminal_width = map(int, os.popen('stty size', 'r').read().split())[1]

    for line in range(nyan_height):
        is_underscore = initial_frame
        for i in range(rainbow_length):
            color = colors[i * terminal_width / rainbow_length]
            line_mod = line % 2 == 1
            char = '_' if is_underscore ^ line_mod else '-'
            draw_buffer[line].append(get_print_color(char, color[0], color[1], color[2]))
            is_underscore = not is_underscore

        [draw_buffer[line].append(char) for char in get_nyan_frame(initial_frame, line)]
        draw_buffer[line].append("\n")

    split_buffer()

    for idx in xrange(len(draw_buffer[0])):
        for line in xrange(len(draw_buffer)):
            [print(char, end='') for char in draw_buffer[line][idx]]
    # while len(draw_buffer[nyan_height-1]):
    #     for line in range(nyan_height):
    #         for index, char in enumerate(draw_buffer[line]):
    #             if index < terminal_width:
    #                 print(char, end='')
    #             else:
    #                 print("HIHSHGKSG")
    #                 # print(draw_buffer[line])
    #                 # draw_buffer[line] = draw_buffer[line][index:]
    #                 # print(draw_buffer[line])
    #                 sys.exit()

    draw_buffer = clear_buffer()
    initial_frame = not initial_frame
    rainbow_length += 1
    time.sleep(0.1)
