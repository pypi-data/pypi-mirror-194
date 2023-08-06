import curses
from math import ceil

from threading import Lock
import time
class ScreenHandler:
  def __init__(self, config, wrapper):
    self.config = config
    self.wrapper = wrapper

    self.stdscr = None
    self.input_window = None
    
    self.output_window = None
    self.output_window_h = 0
    self.output_content_h = 0
    self.output_content_s_line = 0
    self.next_output_line = 1
    self.output_view_h = 0
    
    self.screen_h = 0
    self.screen_w = 0
    
    self.output_scroll_pos = 0
    self.prompt_string = " spsm >> "
    
    self.current_input = []
    
    self.error_handler = None
    self.input_handler = None
    self.log_handler = None
    
    self.screen_lock = Lock()
  
  def connect_log_handling(self, log_handler):
    self.log_handler = log_handler
  
  def connect_error_handling(self, error_handler):
    self.error_handler = error_handler
    
  def connect_input_handler(self, input_handler):
    self.input_handler = input_handler

  def init_windows(self):
    
    # Initialize the curses screen
    self.stdscr = curses.initscr()

    # Enable keypad keys to be recognized
    self.stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

    # Get the dimensions of the terminal window
    self.screen_h, self.screen_w = self.stdscr.getmaxyx()

    # Create the output window
    
    self.init_output_window()

    # Create the input window
    self.input_window = curses.newwin(3, self.screen_w, self.screen_h - 3, 0)
    self.input_window.nodelay(True)
    self.input_window.keypad(True)
    self.refresh()

  def append_output(self, output, color=0, refresh=True):
    self.output_content_h += 1
    self.output_window.addstr("\n" + output.replace("\n", ""), curses.color_pair(color))
    scroll_amt = ceil(len(output)/self.screen_w)
    self.next_output_line += scroll_amt
    self.scroll_down()
    if refresh:
      self.refresh()

  def set_scroll(self):
    self.output_scroll_pos = self._max_scroll_value()
    
  def scroll_down(self):
    if not self.output_scroll_pos > self._max_scroll_value():
      self.output_scroll_pos += 1
        
  def scroll_up(self):
    if not self.output_scroll_pos < self.output_content_s_line:
      self.output_scroll_pos -= 1
      
  def format_screen(self):
    self.screen_h, self.screen_w = self.stdscr.getmaxyx()
    
    self.input_window.resize(3, self.screen_w)
    self.input_window.mvwin(self.screen_h - 3, 0)
    
    output_window_content = self.log_handler.get_log_as_strings()
    self.reset_output_window()
    
    for log in output_window_content:
      self.append_output(log['content'], log['color'], False)
    
    self.refresh()

  def init_output_window(self):
    self.output_view_h = self.screen_h - 4
    self.output_window_h = self.screen_h*200
    self.output_window = curses.newpad(self.output_window_h, self.screen_w)
    self.output_content_s_line = self.output_view_h + 1
    self.output_window.move(self.output_content_s_line, 0)
    self.output_window.scrollok(True)
    
  def refresh_output_window(self):
    self.output_window.refresh(self.output_scroll_pos,0, 0,0, self.output_view_h, self.screen_w)

  def reset_output_window(self):
    self.next_output_line = 1
    self.output_content_h = 0
    self.output_scroll_pos = 0
    self.output_view_h = self.screen_h - 4
    # self.output_window_h = self.screen_h*200
    self.output_window.clear()
    self.output_window.resize(self.output_window_h, self.screen_w)
    self.output_content_s_line = self.output_view_h + 1
    self.output_window.move(self.output_content_s_line, 0)

  def reset_input_window(self):
    self.refresh()

  def refresh(self, force=False):
    self.screen_lock.acquire()
    retry = False
    if force:
      self.stdscr.touchwin()
    try:
      self.input_window.clear()
      self.input_window.border()
      self.input_window.addstr(1,1, self.prompt_string)
      self.input_window.addstr("".join(self.current_input))
      
      self.input_window.refresh()
      self.refresh_output_window()
    except curses.error:
      retry = True
    finally:
      self.screen_lock.release()
      if retry:
        time.sleep(0.1)
        self.refresh()

  def clear_input_window(self):
    self.input_window.clear()
    self.refresh()

  def cleanup(self):
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    
  def prepare_for_attach(self):
    self.format_screen()
    
  def prepare_for_detach(self):
    pass
    
  def _max_scroll_value(self):
    return self.output_content_s_line + self.output_content_h - self.output_view_h - 1
    
  #---- Input Decoding ----#
  def track_input(self):
    while self.wrapper.active:
      try:
        c = self.input_window.get_wch()
      except curses.error:
        continue
      
      if c == -1 or c == curses.ERR:
        continue
      elif c == curses.KEY_BACKSPACE or c == '^?' or c == '\b':
        if len(self.current_input) == 0:
          continue
        self.input_window.addstr("\b \b")
        self.current_input = self.current_input[:-1]
      elif c == curses.KEY_ENTER or c == '\n' or c == '\r':
        if len(self.current_input) == 0:
          continue
        command = ''.join(self.current_input)
        self.reset_input_window()
        self.current_input = []
        self.input_handler.handle_command(command)
      elif c == curses.KEY_RESIZE:
        try:
          self.format_screen()
        except curses.error:
          pass
      elif c == curses.KEY_UP:
        self.scroll_up()
        self.refresh_output_window()
      elif c == curses.KEY_DOWN:
        self.scroll_down()
        self.refresh_output_window()
      else:
        self.screen_lock.acquire()
        
        self.current_input.append(c)
        self.input_window.addch(c)
        
        self.screen_lock.release()
      self.input_window.refresh()