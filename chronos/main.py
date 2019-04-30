"""Main module of kytos/Cronos Kytos Network Application.

Napp to store itens along time
"""
from flask import jsonify
import settings
# from napps.kytos.Cronos import settings
from backends.csvbackend import CSVBackend
from backends.influx import InfluxBackend
from kytos.core import KytosNApp, log, rest


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
        elif settings.DEFAULT_BACKEND == 'CSV':
            self.backend = CSVBackend(settings)

    @rest('v1/<namespace>/<value>', methods=['POST'])
    @rest('v1/<namespace>/<value>/<timestamp>', methods=['POST'])
    def save(self, namespace, value, timestamp=None):
        """Save the data in one of the backends."""

        self.backend.save(namespace, value, timestamp)

        return jsonify({"response": "Value saved !"}), 200

    @rest('v1/<namespace>/', methods=['DELETE'])
    @rest('v1/<namespace>/<start>', methods=['DELETE'])
    @rest('v1/<namespace>/<end>', methods=['DELETE'])
    @rest('v1/<namespace>/<start>/<end>', methods=['DELETE'])
    def delete(self, namespace, start=None, end=None):
        """Delete the data in one of the backends."""
        self.backend.delete(namespace, start, end)

        return jsonify({"response": "Values deleted !"}), 200

    def get(self, namespace, start=None, end=None, method=None,
            fill=None, group=None):
        """Retrieve the data from one of the backends."""

        result = self.backend.get(namespace, start, end, method, fill, group)
        if not result:
            return jsonify({"response": "Not Found"}), 404

        return jsonify(result), 200

    def execute(self):
        """Run after the setup method execution.

        You can also use this method in loop mode if you add to the above setup
        method a line like the following example:

            self.execute_as_loop(30)  # 30-second interval.
        """

    def shutdown(self):
        """Execute before tha NApp is unloaded."""
        log.info("Time Series NApp is shutting down.")
