import uuid

from core.utils import STATUS


class State(object):
    """
    Base class model for Option.
    Stores the state of a script.
    """
    key = None
    script = None
    instance = None
    status = None
    name = None

    def __init__(self, script, name=None, key=None):
        """
        Requires a key and a class to instantiate.
        """
        if script is None:
            raise RuntimeError('NoneType is not allowed for script.')

        self.script = script

        if key is None:
            self.key = uuid.uuid4()

        if hasattr(self.script, 'name'):
            self.name = getattr(self.script, 'name')
        else:
            self.name = self.key

    def add_instance(self, instance, status=STATUS.INITIAL):
        """
        Method to set an instance
        """
        self.instance = instance
        self.status = status

    def check_if_failed(self):
        """
        Returns True if status is `FAILURE`.
        """
        return self.status == STATUS.FAILURE

    def initiate_sequence(self, *args, **kwargs):
        """
        Initiate the script class with provided arguments.
        """
        instance = self.script(*args, **kwargs)
        self.add_instance(instance)
        return True

    def _set_failure(self):
        """
        Set status to failure.
        """
        self.status = STATUS.FAILURE

    def _set_success(self):
        """
        Set status to success.
        """
        self.status = STATUS.SUCCESS

    def _set_running(self):
        """
        Set status to running.
        """
        self.status = STATUS.RUNNING

    def run(self):
        """
        Run the script instance.
        """
        try:
            self._set_running()
            self.instance.initiate_sequence()
        except Exception as e:
            self._set_failure()
        else:
            self._set_success()