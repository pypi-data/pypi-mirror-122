import subprocess as sp
import threading
from os.path import exists
from typing import Optional

from flask import Flask
from werkzeug.serving import make_server


def get_factory_dll_path() -> str:
    return "/".join(__file__.split('/')[:-1]) + '/bin/factory/Finbourne.Honeycomb.Host.dll'


class _ServerThread(threading.Thread):
    """Class that represents a thread managing a flask app. Allows for the starting and stopping of the webserver
    in the background.

    """

    def __init__(self, app: Flask, host: str, port: int):
        """Constructor for the _ServerThread class.

        Args:
            app (Flask): the flask app to manage.
            host (str): the host to run at.
            port (int): the port to use.
        """
        threading.Thread.__init__(self)
        self.server = make_server(host, port, app)
        self.context = app.app_context()
        self.context.push()

    def run(self) -> None:
        """Start the provider webserver.

        """
        print("Starting provider server")
        self.server.serve_forever()

    def shutdown(self) -> None:
        """Shut down the provider webserver.

        """
        print("Stopping provider server")
        self.server.shutdown()
        self.join()


class _FactoryThread(threading.Thread):
    """Class that represents a thread managing the Luminesce python provider factory process. Allows for the starting
    and stopping of the factory process in the background.

    """

    def __init__(self, host: str, port: int, user_id: Optional[str] = None):
        """Constructor for the _FactoryThread class.

        Args:
            host (str): the host that the provider webserver is running at.
            port (int): the port that the provider webserver is listening at.
        """
        threading.Thread.__init__(self)

        self.factory_dll_path = get_factory_dll_path()

        self.cmd = f'dotnet {self.factory_dll_path} --quiet '
        if user_id is not None:
            self.cmd += f'--localRoutingUserId "{user_id}" '
        self.cmd += f'--config "PythonProvider:BaseUrl=>http://{host}:{port}/api/v1/"'
        self.factory_process = None

    def run(self) -> None:
        """Start the factory process.

        """
        if not exists(self.factory_dll_path):
            raise NotImplementedError(
                "Luminesce python provider factory dll not available - local python providers aren't available yet.\n"
                f"Expected path: {self.factory_dll_path}"
            )

        print("Starting local provider factory")
        self.factory_process = sp.Popen(
            args=self.cmd.split()
        )

    def shutdown(self) -> None:
        """Terminate the factory process.

        """
        if self.factory_process is not None:
            print("Stopping local provider factory")
            self.factory_process.terminate()
            self.join()
        else:
            # No factory is running: no-op
            pass
