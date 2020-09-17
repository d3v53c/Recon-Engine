"""
Decorators used in the project.
"""
from core.utils.constants import STATUS


def pre_run_check(method):
    """
    Sets status to RUNNING for Script instance.
    """
    def post_run_log(self):
        """
        Function which actually sets the status.
        """
        # self._set_status(STATUS.RUNNING)

        try:
            # call the method
            method(self)
        except Exception as e:
            # set status to FAILURE
            # self._set_status(STATUS.FAILURE)
            raise
        else:
            pass

        self.print_new_line()
        self.debug_log(
            f'Output written to file located at {self.get_outfile_path()}.',
            console=True,
        )

    return post_run_log
