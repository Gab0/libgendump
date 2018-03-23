import io
import pycurl

import stem.process

from stem.util import term

SOCKS_PORT = 7000



def print_bootstrap_lines(line):
    if "Bootstrapped " in line:
        print(term.format(line, term.Color.BLUE))


    print(term.format("Starting Tor:\n", term.Attr.BOLD))


class TorConnection():

    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = stem.process.launch_tor_with_config(
          config={
            'SocksPort': str(SOCKS_PORT),
            'ExitNodes': '{ru}',
          },
          init_msg_handler = print_bootstrap_lines,
        )

        print(term.format("\nChecking our endpoint:\n", term.Attr.BOLD))
        print(term.format(self.query("https://www.atagar.com/echo.php"), term.Color.BLUE))

    def kill(self):
        self.connection.kill()  # stops tor

    def download(self, URL, filename=None):
        content = URL

    def query(self, url):
        """
        Uses pycurl to fetch a site using the proxy on the SOCKS_PORT.
        """

        output = io.BytesIO()

        query = pycurl.Curl()
        query.setopt(pycurl.URL, url)
        query.setopt(pycurl.PROXY, 'localhost')
        query.setopt(pycurl.PROXYPORT, SOCKS_PORT)
        query.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
        query.setopt(pycurl.WRITEFUNCTION, output.write)

        try:
            query.perform()
            return output.getvalue()
        except pycurl.error as exc:
            return "Unable to reach %s (%s)" % (url, exc)


# Start an instance of Tor configured to only exit through Russia. This prints
# Tor's bootstrap information as it starts. Note that this likely will not
# work if you have another Tor instance running.
