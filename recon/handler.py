import sys
import os
import inspect
import importlib
import recon.tools

from core.window import Window, Script
from core.exception import HumanVerificationFailure
from core.tools import Toolkit
from core.utils import (
    STATUS,
    import_module,
    extract_script_classes,
    list_files_in_dir,
)


class ReconEngine(Window):
    """
    Base class for ReconEngine.
    """
    inventory = Toolkit()

    def __init__(self, *args, **kwargs):
        """
        Load scripts into memory.
        """
        super().__init__(*args, **kwargs)

        # load the scripts from directory to the inventory.
        self.load_scripts()

    def validate_inputs(self):
        """
        Input validations.
        """
        if self.args.target:
            self.targets.append(self.args.target)
        else:
            raise Exception("Usage: ReconEngine <IP ADDRESS>\n")
            print("Usage: ReconEngine --inputfile <file with LIST OF IP>")
            print("-" * 70)
            print(
                "(Provide --target (website address for recon) or --inputfile (List of urls for recon)"
            )
            sys.exit()

    def run(self, *args, **kwargs):
        """
        Run all.
        """
        self.print_new_line()
        self.print_line()

        self.debug_log(
            f"Initiating Reconnaissance on target {self.current_target}..",
            console=True,
        )
        self.print_new_line()
        self.console_log("Running tools from inventory..")

        self.print_new_line()

        # run all scripts in the inventory.
        self.run_inventory()

        self.console_log(f"Reconnaissance completed successfully.")
        # tickmark
        # self.print_raw(u'[\u2713]')

    def run_inventory(self):
        """
        Run the tools included in inventory.
        """
        keys = self.inventory.overview()

        self.switch_to_right()
        self.console_log("Scipts Running:")
        self.print_mini_line()
        self.switch_to_main()

        for i, key in enumerate(keys):

            # acuire state of the script from inventory
            script = self.inventory.get_state(key)

            self.debug_log(
                f"{script.name} ({i + 1}/{self.inventory.count()})",
                console=True,
            )

            self.print_new_line()

            try:
                # instantiate script instance with arguments.
                script.initiate_sequence(
                    self.args,
                    self.window,
                    self.exit_e,
                    logfile=self.logfile,
                )

                # run script instance.
                script.run()
            except Exception as e:
                # Update on right menu.
                if self.switch_to_right():
                    self.console_log(f'{script.name} - F')
                self.switch_to_main()

                raise

                if issubclass(e, HumanVerificationFailure):
                    # TODO: what to do if an error raised.
                    pass
            else:
                if self.switch_to_right():
                    self.console_log(f'{script.name} - ' + u'\u2713', dump=False)
                self.switch_to_main()
                self.print_footer()
        else:
            if self.switch_to_right():
                self.print_new_line()
                self.print_mini_line()
            self.switch_to_main()

    def load_scripts(self):
        """
        Load all the scripts into memory.
        """
        tools_dir = os.path.dirname(recon.tools.__file__)
        self.print_new_line()

        # walk through each file in the dir.
        for f in list_files_in_dir(tools_dir):
            filepath = os.path.join(tools_dir, f)

            try:
                # import module using importlib.
                module = import_module(filepath)

                # list out classes contained in the module.
                for kls in extract_script_classes(module, Script):
                    # check if kls is a class, subclass of `core.window.Script`,
                    # not `core.window.Script` class itself.
                    # add to inventory
                    self.inventory.add(kls.__name__, kls)

                    self.debug_log(
                        f'Script loaded - {kls.name}.',
                        console=True,
                    )
            except Exception as e:
                raise
            else:
                pass
        else:
            pass
