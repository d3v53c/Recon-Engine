import requests
import re
import webbrowser

from core.window import Script
from core.utils import resolve_ip_from_domain

class IpGeolocation(Script):
    """
	Gather geo location info of the target.
	"""
    name = "IP Geolocation Discovery"
    outfile = 'geoip.txt'

    def run(self):
        """
		Run Geolocation discovery on target.
		"""
        self.debug_log(
            f"Running {self.name} on target {self.current_target}..\n",
            console=True,
        )

        ip_addr = resolve_ip_from_domain(self.current_target)
        url = f"https://ipapi.co/{ip_addr}/json/"

        self.spinner.start(text="Collecting information..")
        response = requests.get(url)
        self.spinner.stop()

        response = response.text

        # write output to file
        self.write_out(response)

        # console logging
        self.debug_log(f'--- IP Geolocation Info ---')
        for line in response.splitlines():
            self.debug_log(line.strip(), console=True)
        else:
            self.debug_log(f'--- End ---', console=True)
            self.print_new_line()
