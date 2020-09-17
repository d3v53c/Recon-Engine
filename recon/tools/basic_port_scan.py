import socket

from core.window import Script
from core.utils import (
    known_port_list,
    resolve_ip_from_domain,
    check_for_open_port,
)


class BasicPortScan(Script):
    """
    This script executes a basic port scan on target
    using socket.
    """
    name = "Basic Port Scan"
    outfile = 'portmap.txt'
    open_ports = dict()

    def run(self):
        """
        Run the basic port scan.
        """
        ip_addr = resolve_ip_from_domain(self.current_target)
        self.debug_log(
            f"Running {self.name} on target {ip_addr}..\n",
            console=True,
        )
        self.debug_log('--- Basic Port Scan ---')

        for port in map(int, known_port_list.keys()):
            self.spinner.start(f'Scanning port {port}..')
            # check if port open or not
            port_open = check_for_open_port(ip_addr, port, timeout=1)
            if port_open:
                self.open_ports[port] = known_port_list.get(str(port))
            self.spinner.stop()

            self.debug_log(
                f'Port {port}: {"Open" if port_open else "Closed"}',
                console=port_open,
            )
            if port_open:
                self.print_new_line()
        else:
            self.debug_log('--- End ---')

        response = ''
        for port, service in self.open_ports.items():
            response += f'Port: {port}, Service: {service}, State: Open\n'
        else:
            self.write_out(response)

        self.debug_log(f'Port scanning completed.', console=True)
