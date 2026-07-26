import sys
import time
import threading

class ConsoleAnimation:
    STYLES = {
        "0": ["", "", ""],
        "1": [".  ", ".. ", "..."],
        "2": [" / ", " - ", " \\ ", " | "],
        "3": [" > ", " >> ", " >>>"],
        "download": "download"
    }

    def __init__(self, style="1", delay=0.1, clear_line=True, bar_length=20):
        self.style = style
        self.delay = delay
        self.clear_line = clear_line
        self.bar_length = bar_length
        self.frames = self.STYLES.get(style, self.STYLES["1"])
        self.current = 0
        self.total = 0 
        self.start_time = 0
        self.text = ""
        self.done = False
        self._thread = None

    def update(self, current, total=None):
        self.current = current
        if total is not None:
            self.total = total

    def _draw_progress(self):
        if self.total > 0:
            percent = min(1.0, self.current / self.total)
            filled = int(self.bar_length * percent)
            bar = '█' * filled + '▒' * (self.bar_length - filled)
            elapsed = time.time() - self.start_time
            speed = self.current / elapsed if elapsed > 0 else 0
            eta = (self.total - self.current) / speed if speed > 0 else 0
            eta_str = time.strftime("%M:%S", time.gmtime(eta))
            sys.stdout.write(f"\r{self.text} [{bar}] {self.current}/{self.total} | Ост: {eta_str}")
        else:
            sys.stdout.write(f"\r{self.text} [{self.current}/?] | Ост: --:--")
        sys.stdout.flush()
    def logo(self, text, delay=0.1):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    print()
    def _animate(self):
        self.start_time = time.time()
        max_frame_len = max(len(f) for f in self.frames) if isinstance(self.frames, list) else 60
        clear_spaces = " " * (len(self.text) + max_frame_len + 20)
        while not self.done:
            if self.style == "download":
                self._draw_progress()
                time.sleep(self.delay)
            else:
                for frame in self.frames:
                    if self.done:
                        break
                    sys.stdout.write(f"\r{self.text}{frame}")
                    sys.stdout.flush()
                    time.sleep(self.delay)
        if self.clear_line:
            sys.stdout.write(f"\r{clear_spaces}\r")
        else:
            if self.style == "download" and self.total > 0:
                self.current = self.total
                self._draw_progress()
            sys.stdout.write("\n")
        sys.stdout.flush()

    def process_iterable(self, text, iterable, action):
        self.text = text
        self.done = False
        self.current = 0
        try:
            self.total = len(iterable)
        except TypeError:
            self.total = 0
        self.start_time = time.time()
        self._thread = threading.Thread(target=self._animate)
        self._thread.start()
        results = []
        try:
            for item in iterable:
                results.append(action(item))
                self.current += 1
            return results
        finally:
            self.done = True
            if self._thread:
                self._thread.join()

    def __call__(self, text, action, *args, **kwargs):
        self.text = text
        self.done = False
        self.current = 0
        self.start_time = time.time()
        self._thread = threading.Thread(target=self._animate)
        self._thread.start()
        try:
            result = action(*args, **kwargs)
            return result
        finally:
            self.done = True
            if self._thread:
                self._thread.join()