# import sys
import os
import json
import time
from codecs import open
import sys
import multiprocessing

import pyHook
import pythoncom
import pygame
# from pygame.locals import RESIZABLE


class Main(object):

    _display_pygame = False
    _pass_got = []
    exit_program = False

    _pygame_inited = False

    def __init__(self, password, timeout, image_path, bg_color):
        hm = pyHook.HookManager()

        hm.MouseAll = self.on_mouse_event
        # hm.MouseAll = OnMouseEvent
        hm.HookMouse()

        hm.KeyDown = self.on_keyboard_event
        hm.HookKeyboard()
        # pythoncom.PumpMessages()
        self._password = password.lower()
        self._timeout = timeout
        self._image_path = image_path
        self._bg_color = bg_color

        self._start_time = time.time()

    def on_mouse_event(self, event):
        if not self._display_pygame and time.time() - self._start_time > self._timeout:
            print('mouse event trigger pygame')
            self.display_pygame()

    def on_keyboard_event(self, event):
        print(event.Key)
        if not self._display_pygame:
            if time.time() - self._start_time > self._timeout:
                print('keyboard event trigger pygame')
                self.display_pygame()
            return

        if not event.Key:
            return

        self._pass_got.append(event.Key.lower())
        got_string = ''.join(self._pass_got)
        if not self._password.startswith(got_string):
            self._pass_got[:] = list()
            return
        if got_string == self._password:
            self._display_pygame = False
            self.exit_program = True
            # sys.exit()

    def display_pygame(self):
        if self._pygame_inited:
            return

        self._pygame_inited = True

        print('start pygame')
        self._display_pygame = True

        try:
            pygame.init()
        except BaseException as e:
            print(e)
            sys.exit()

        pygame.mouse.set_visible(False)
        display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        display_surface.fill(self._bg_color)
        image = pygame.image.load(self._image_path)
        display_surface.blit(image, (0, 0))
        while self._display_pygame:
            # pygame.event.pump()
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:  # The user pressed the close button in the top corner of the window.
            #         self._display_pygame = False
            pygame.display.update()
            pygame.event.clear()
            # pythoncom.PumpWaitingMessages()

        pygame.quit()


# def OnMouseEvent(event):
#     # called when mouse events are received
#     print 'MessageName:',event.MessageName
#     print 'Message:',event.Message
#     print 'Time:',event.Time
#     print 'Window:',event.Window
#     print 'WindowName:',event.WindowName
#     print 'Position:',event.Position
#     print 'Wheel:',event.Wheel
#     print 'Injected:',event.Injected
#     print '---'
#
#
# def OnKeyboardEvent(event):
#     print 'MessageName:',event.MessageName
#     print 'Message:',event.Message
#     print 'Time:',event.Time
#     print 'Window:',event.Window
#
#     print 'WindowName:',event.WindowName
#     print 'Ascii:', event.Ascii, chr(event.Ascii)
#     print 'Key:', event.Key
#     print 'KeyID:', event.KeyID
#     print 'ScanCode:', event.ScanCode
#     print 'Extended:', event.Extended
#     print 'Injected:', event.Injected
#     print 'Alt', event.Alt
#     print 'Transition', event.Transition
#     print '---'

def except_hook(*exc_info):
    pass


def main():
    multiprocessing.freeze_support()
    config_file = os.path.join(os.getcwd(), 'config.json')
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    sys.excepthook = except_hook

    main_obj = Main(config['password'], config['timeout'], config['image'], tuple(config['bgColor']))
    # main_obj.display_pygame()
    while not main_obj.exit_program:
        pythoncom.PumpWaitingMessages()


if __name__ == '__main__':
    main()
