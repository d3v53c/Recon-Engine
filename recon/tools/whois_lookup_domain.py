import requests

from core.window import Script
from core.utils import (
    find_match,
    validate_domain,
)


class DomainWhoisLookup(Script):
    """
    Gather whois lookup info of target domain using `hackertarget.com`.
    """
    name = 'Domain Whois Lookup'
    outfile = 'whois.txt'

    def run(self, *args, **kwargs):
        """
        Run Domain Whois Lookup on target.
        """
        self.debug_log(
            f"Running {self.name} on target {self.current_target}..\n",
            console=True,
        )
        url = f"https://api.hackertarget.com/whois/?q={self.current_target}"

        self.spinner.start(text="Collecting information..")
        response = requests.get(url)
        self.spinner.stop()

        response = response.text

        # write output to file
        self.write_out(response)

        # console logging
        self.debug_log(f'--- Domain Whois Lookup info ---')
        for line in response.splitlines():
            self.debug_log(line.strip(), console=True)
        else:
            self.debug_log(f'--- End ---', console=True)
            self.print_new_line()
