"""Main module of kytos/Cronos Kytos Network Application.

Napp to store itens along time
"""
import settings
# from napps.kytos.Cronos import settings
from backends.csvbackend import CSVBackend
from backends.influx import InfluxBackend
from backends.rrd import RRDBackend
from kytos.core import KytosNApp, log


class Main(KytosNApp):
    """Main class of kytos/Cronos NApp.

    This class is the entry point for this napp.
    """
    backend = None

    def setup(self):
        """Init method for the napp."""
        log.info("Time Series NApp started.")

        if settings.DEFAULT_BACKEND == 'INFLUXDB':
            self.backend = InfluxBackend(settings)
        elif settings.DEFAULT_BACKEND == 'RRD':
            self.backend = RRDBackend()
        elif settings.DEFAULT_BACKEND == 'CSV':
            self.backend = CSVBackend(settings)

    def save(self, namespace, value, timestamp=None):
        """Save the data in one of the backends."""
        self.backend.save(namespace, value, timestamp)

    def delete(self, namespace, start, end, file_name=None):
        """Delete the data in one of the backends."""

        if settings.DEFAULT_BACKEND == 'CSV':
            self.backend.delete(file_name, start, end)
        else:
            self.backend.delete(namespace, start, end)

    def get(self, namespace, start=None, end=None, file_name=None):
        """Retrieve the data from one of the backends."""

        if settings.DEFAULT_BACKEND == 'CSV':
            self.backend.get(file_name, start, end)
        else:
            self.backend.get(namespace, start, end)

    def execute(self):
        """Run after the setup method execution.

        You can also use this method in loop mode if you add to the above setup
        method a line like the following example:

            self.execute_as_loop(30)  # 30-second interval.
        """

    def shutdown(self):
        """Execute before tha NApp is unloaded."""
        log.info("Time Series NApp is shutting down.")


teste = Main(KytosNApp)
print(teste.get("average_temperature"))
