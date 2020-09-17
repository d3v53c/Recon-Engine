from core.window import Window
from core.utils import (
    makedir,
    delall,
    validate_domain,
)
from core.utils.constants import STATUS
from core.utils.decorators import pre_run_check


class Script(Window):
    """
    Window object for each script module.
    """
    name = None
    status = None

    def __init__(self, *args, **kwargs):
        """
        Initialise all necessary attributes before calling parent method.
        """
        # use logfile if provided.
        self.logfile = kwargs.get('logfile', None)

        # check if clearing directory flag is set
        clear_dir = kwargs.get('clear_dir', False)
        if not clear_dir:
            self.set_dir_cleared()

        if self.name is not None:
            self.debug_log(f"Initiating {self.name}")

        super().__init__(*args, **kwargs)

        self._set_initialize()

        if self.name is None:
            raise ValueError("Valid name is missing for the script.")

    def validate_inputs(self):
        """
        Validate arguments to the tool.
        """
        target = self.args.target
        try:
            valid = validate_domain(target)
            if valid:
                self.targets.append(target)
        except Exception as _:
            raise ValueError(f"Invalid Target specified {target}")
        else:
            self.debug_log(f"Target : {target} is valid.")

    @pre_run_check
    def run(self, *args, **kwargs):
        """
        This is where business logic happens
        """
        raise NotImplementedError("`run` method not implemented in script.")

    @pre_run_check
    def initiate_sequence(self):
        """
        Kick off running sequence
        """
        self.run()

    @staticmethod
    def name(cls):
        """
        Returns name of the child class.
        """
        return cls.name

    def get_outfile_path(self):
        """
        Define outfile path to enable write out.
        """
        out_dir = self.get_output_directory()
        return os.path.join(out_dir, self.outfile)

    def get_output_directory(self):
        """
        Return path to output directory.
        """
        root_dir = self._get_target_root_dir(self.current_target)
        return os.path.join(root_dir, '')

    def _set_status(self, status):
        """
        Method: set status as provided after validation.
        """
        valid = STATUS.check_status(status)
        if valid:
            self.status = status

    def _set_initialize(self):
        """
        Set status to INITIAL
        """
        self._set_status(STATUS.INITIAL)