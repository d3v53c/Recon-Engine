import requests
import re
import webbrowser

from core.window import Script
from core.utils import (
    validate_domain,
    regex_multisearch,
    find_match,
    resolve_ip_from_domain,
)
from core.exception import HumanVerificationFailure

from recon.constants import *


class WebInfo(Script):
    """
    Gather website information using 'myip.ms'
    """
    name = "Website Info Gathering"
    outfile = "info.txt"

    def parse_web_info(self, response):
        """
        Parses information about website from html response.
        :returns: Dictionary with key -> Labels, value -> Parsed values
        """
        search_dict = {
            "Visitors per day": (RE_VISITORS, 1),
            "Linked IPv6 Address": (RE_IP_V6, 1),
            "IP Location": (RE_IP_LOCATION, 1),
            "IP Reverse DNS (Host)": (RE_REVERSE_DNS, 2),
            "Hosting Company": (RE_HOSTING_COMPANY, 1),
            "Hosting Company IP Owner": (RE_HOSTING_COMPANY_IP_OWNER, 3),
            "Hosting IP Range": (
                RE_HOSTING_IP_RANGE,
                (3, 2, 1),
                lambda args: f'{args[2]} - {args[1]} ({args[0]} ips)',
            ),
            "Hosting Address": (RE_HOSTING_ADDRESS, 1),
            "Owner Address": (RE_OWNER_ADDRESS, 1),
            "Hosting Country": (RE_HOSTING_COUNTRY, 1),
            "Owner Country": (RE_OWNER_COUNTRY, 1),
            "Hosting Phone": (RE_HOSTING_PHONE, 1),
            "Owner Phone": (RE_OWNER_PHONE, 1),
            "Hosting Website": (RE_HOSTING_WEBSITE, 1),
            "Owner Website": (RE_OWNER_WEBSITE, 3),
            "CIDR": (RE_CIDR, 1),
            "Owner CIDR": (
                RE_OWNER_CIDR,
                (3, 4),
                lambda args: f'{args[0]}/{args[1]}',
            ),
            "Hosting CIDR": (
                RE_HOSTING_CIDR,
                (3, 4),
                lambda args: f'{args[0]}/{args[1]}',
            ),
        }
        match_available = find_match(RE_VISITORS, response)
        if not match_available:
            return False, None
        return True, regex_multisearch(search_dict, response)

    def run(self, *args, **kwargs):
        """
        Gather information about the target.
        """
        self.debug_log(
            f"Running {self.name} on target {self.current_target}..\n",
            console=True,
        )
        url = f"https://myip.ms/{self.current_target}"

        self.spinner.start(text="Collecting information..")
        response = requests.get(url)
        self.spinner.stop()

        response = response.text
        parsed, parsed_dict = self.parse_web_info(response)
        if not parsed:
            self.console_log(f"Cannot bypass human verification of the site.")
            self.console_log(f"Please visit the site and retry.")
            webbrowser.open_new_tab(url)
            raise HumanVerificationFailure("Human verification failed.")

        ip_addr = resolve_ip_from_domain(self.current_target)

        self.debug_log(f'--- Website Info ---', console=True)

        hosting_info = f'Hosting Info for Website : {self.current_target}'
        self.debug_log(hosting_info, console=True)
        self.write_out(f'{hosting_info}\n')

        ip_addr_content = f'IP Address : {ip_addr}'
        self.debug_log(ip_addr_content, console=True)
        self.write_out(f'{ip_addr_content}\n')

        for label, value in parsed_dict.items():
            content = f'{label} : {value}'
            self.debug_log(content, console=True)
            self.write_out(f'{content}\n')
        else:
            self.debug_log(f'--- End ---', console=True)
            self.print_new_line()