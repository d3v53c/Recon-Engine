import sys
import curses
import os
import time

from datetime import datetime
from core.utils import (
    makedir,
    init_logger,
    get_home_dir,
    delall,
)
from core.progress import Spinner


class Window(object):
    """
    Handler for the window object.
    """
    args = None
    window = None
    targets = []
    spinner = None
    debug = True
    logfile = None
    verbose = 2
    version = "v0.1"
    exit_e = None
    current_target = None
    dumpfile = "recon.txt"
    logging = True
    outfile = None
    __dir_cleared = False
    _pads = dict()

    def __init__(self, args, screen, exit_e, **kwargs):
        """
        Instance initiation.
        """

        self.args = args
        self.window = screen
        self.exit_e = exit_e
        self.window.scrollok(1)
        self.logging = kwargs.get('logging', True)
        # save right and left tab
        # TODO: Possible addidtional feature, may need to re-evaluate.
        self._pads = dict(
            main=screen,
            right=kwargs.pop('right', None),
            left=kwargs.pop('left', None),
        )

        self.spinner = Spinner(
            text='Loading',
            placement='right',
            spinner='line',
            # interval=200,
            window=self.window,
        )

        # initiate logger
        self._initiate_logger()

        # process each argument provided
        self._validate_inputs()

    def _validate_inputs(self):
        """
        Input validation by child class.
        Logger initiation.
        Argument processing.
        """

        # call custom input validations
        self.validate_inputs()

        # set target
        self.__set_target(self.targets[0])

        # process arguments
        self._process_arguments()

    def _initiate_logger(self):
        """
        Logger initiation
        """

        # initiate log file
        if self.logging and self.logfile is None:
            self.logfile = init_logger()

    def run(self):
        """
        Run all.
        """
        raise NotImplementedError('Run method not implemented')

    def _process_arguments(self):
        """
        Exposed method for additional argument processing.
        """
        if self.__dir_cleared:
            return

        for target in self.targets:
            outdir = self._prepare_outdir(target)
        else:
            self.set_dir_cleared()

    def validate_inputs(self):
        """
        Exposed method for additional input validation.
        """
        pass

    def dump_text(self, line, target=None):
        if self.current_target is None and target is None:
            return
        target = self.current_target or target
        dump_file = self.get_stdout_dir(target).replace(".html", ".txt")
        with open(dump_file, 'a') as f:
            f.write(line)

    def console_log(self, string, dump=True):
        line = f"\n [+] {string}"
        self._print(line)

        if dump:
            self.dump_text(line)

    def _print(self, string):
        """
        Print text to screen.
        """
        string.encode(sys.stdout.encoding, errors='replace')
        self.window.addstr(string)
        self.window.refresh()

    def print_raw(self, string, dump=True):
        string = f'\n{string}\n'
        self._print(string)

        if dump:
            self.dump_text(string)

    def print_line(self, dump=True):
        line = f'\n{"=" * 100} \n'
        self._print(line)

        if dump:
            self.dump_text(line)

    def print_mini_line(self, dump=True):
        right_menu_width = round(curses.COLS * 0.2)
        line = f'\n{"=" * right_menu_width}'
        self._print(line)

        if dump:
            self.dump_text(line)

    def print_new_line(self, dump=True):
        line = f'\n'
        self._print(line)

        if dump:
            self.dump_text(line)

    def print_footer(self):
        self.print_new_line()
        self.print_line()

    def write_out(self, content):
        """
        Write output to a file.
        Works only if outfile path is defined.
        """
        filepath = self.get_outfile_path()
        with open(filepath, 'a') as outfile:
            outfile.write(content)

    def __set_target(self, target):
        if target is None:
            raise ValueError(f'{type(target)} cannot be set as a target.')
        self.current_target = target

        self.debug_log(f'Identified Current target : {target}')

    def __reset_target(self):
        self.current_target = None

    def debug_log(self, string, console=False):
        if not self.debug:
            return

        self.log(string.rstrip("\n"))

        if console:
            self.console_log(string)

    def log(self, string, console=False):
        """
        Logging is handled by `logging` flag.
        """
        if console:
            self.console_log(string)
        if not self.logging:
            return
        timestamp = datetime.today().strftime("%d-%m-%Y %H:%M %p")
        log = f'[+] {string} :: {timestamp}\n'
        with open(self.logfile, 'a') as f:
            f.write(log)

    def _get_target_root_dir(self, target):
        home_dir = get_home_dir()
        return os.path.join(home_dir, 'results', f'{target}')

    def get_stdout_dir(self, target):
        """
        Define path to file which holds all verbose shown in terminal.
        """
        if self.dumpfile is None:
            raise NotImplementedError("Dumpfile is not defined.")

        root_dir = self._get_target_root_dir(target)
        return os.path.join(root_dir, f"{self.dumpfile}_{target}")

    def get_outfile_path(self, target):
        """
        Define path to output file.
        """
        raise NotImplementedError("Outfile path must be defined.")

    def _prepare_outdir(self, target):
        target_root_dir = self._get_target_root_dir(target)
        exists = makedir(target_root_dir)
        self.debug_log(
            f'Output directory for target: {target} already exists.',
            console=True)
        self.debug_log(f'Output directory located at {target_root_dir}.',
                       console=True)
        if exists:
            self.debug_log(f'Clearing files from previous run..\n',
                           console=True)
            self.spinner.start(text="Deleting files..")
            time.sleep(2)
            delall(target_root_dir)
            self.spinner.stop()
            self.debug_log(f'Created output directory for target: {target}.',
                           console=True)
            self.debug_log(f'Output directory located at {target_root_dir}.',
                           console=True)
            self.debug_log(f'Cleared successfully.', console=True)
        return target_root_dir

    def set_dir_cleared(self):
        """
        Set directory cleared flag True.
        """
        self.__dir_cleared = True

    def switch_to_pad(self, pad_name):
        """
        Checks for other tabs to switch to with same key.
        If yes, then current `window` selection is switched, else return False.
        """
        pad = self._get_tab(pad_name)
        if pad is not None:
            self.window = pad
            return True
        return False

    def switch_to_main(self):
        """
        Switches to main pad.
        """
        return self.switch_to_pad('main')

    def switch_to_right(self):
        """
        Switches to right pad.
        """
        return self.switch_to_pad('right')

    def switch_to_left(self):
        """
        Switches to left pad.
        """
        return self.switch_to_pad('left')

    def _get_tab(self, pad_name):
        """
        Returns pad window or None.
        """
        return self._pads.get(pad_name)