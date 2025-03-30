import logging
import sys


class LocationError(Exception):
    def __init__(self, message, error_code=None, location_data=None):
        super().__init__(message)
        self.error_code = error_code
        self.location_data = location_data

    def __str__(self):
        """Custom string representation for the exception."""
        base_message = super().__str__()  # Get the base exception message
        if self.error_code:
            base_message += f" (Error Code: {self.error_code})"
        if self.location_data:
            base_message += f" (Location Data: {self.location_data})"
        return base_message

    def log_error(self):
        logger = logging.getLogger('location_error_logger')
        logging.basicConfig(
            level=logging.ERROR,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
        logger.error(self.__str__())

