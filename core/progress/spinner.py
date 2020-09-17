import curses
import threading
from halo import Halo


class Spinner(Halo):
    """
    Windows wrapper for halo spinner module.
    """
    window = None
    y = None
    x = None

    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window

    def __enter__(self):
        """Starts the spinner on a separate thread. For use in context managers.
        Returns
        -------
        self
        """
        return self.start()

    def start(self, text=None):
        """Starts the spinner on a separate thread.
        Parameters
        ----------
        text : None, optional
            Text to be used alongside spinner
        Returns
        -------
        self
        """

        self.y, self.x = self.window.getyx()

        if text is not None:
            self.text = text

        if self._spinner_id is not None:
            return self

        if not (self.enabled and self._check_stream()):
            return self

        self._hide_cursor()
        self._stop_spinner = threading.Event()
        self._spinner_thread = threading.Thread(target=self.render)
        self._spinner_thread.setDaemon(True)
        self._render_frame()
        self._spinner_id = self._spinner_thread.name
        self._spinner_thread.start()

    def stop(self):
        """Stops the spinner and clears the line.
        Returns
        -------
        self
        """
        super().stop()
        self.y = None
        self.x = None
        return self

    def _write(self, s):
        """Write to the stream, if writable
        Parameters
        ----------
        s : str
            Characters to write to the stream
        """
        # if self._check_stream():
        if self.x is not None and self.y is not None:
            # self.debug(f'SELF - {self.x},{self.y}')
            self.window.addstr(self.y, self.x, s)
        else:
            # self.debug(f'GETSYX - {x},{y}')
            self.window.addstr(s)

        self.window.refresh()

    def _render_frame(self):
        """Renders the frame on the line after clearing it.
        """

        if not self.enabled:
            # in case we're disabled or stream is closed while still rendering,
            # we render the frame and increment the frame index, so the proper
            # frame is rendered if we're reenabled or the stream opens again.
            return

        self.clear()
        frame = self.frame()
        # output = '\r{}'.format(frame)
        output = frame

        try:
            self._write(output)
        except UnicodeEncodeError:
            self._write(encode_utf_8_text(output))

    def frame(self):
        """Builds and returns the frame to be rendered
        Returns
        -------
        self
        """
        frames = self._spinner['frames']
        frame = frames[self._frame_index]

        # if self._color:
        #     frame = colored_frame(frame, self._color)

        self._frame_index += 1
        self._frame_index = self._frame_index % len(frames)

        text_frame = self.text_frame()
        return u' [+] {0} {1}  '.format(
            *[(text_frame,
               frame) if self._placement == 'right' else (frame,
                                                          text_frame)][0])

    def clear(self):
        """Clears the line and returns cursor to the start.
        of line
        Returns
        -------
        self
        """
        self._write('\r')
        # self._write(self.CLEAR_LINE)
        # self.window.clrtoeol()
        self.window.refresh()
        return self

    def debug(self, string):
        with open('log.txt', 'a+') as d:
            d.write(f'\n{string}')