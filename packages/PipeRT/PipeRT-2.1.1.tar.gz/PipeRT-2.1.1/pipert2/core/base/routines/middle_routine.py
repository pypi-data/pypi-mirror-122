from abc import ABCMeta, abstractmethod
from pipert2.core.base.routine import Routine


class MiddleRoutine(Routine, metaclass=ABCMeta):

    @abstractmethod
    def main_logic(self, data) -> dict:
        """Process the given data to the routine.

        Args:
            data: The data that the routine processes and sends.

        Returns:
            The main logic result.
        """

        raise NotImplementedError

    def _extended_run(self) -> None:
        self.setup()

        while not self.stop_event.is_set():
            message = self.message_handler.get()
            if message is not None:
                try:
                    output_data = self.main_logic(message.get_data())
                except Exception as error:
                    self._logger.exception(f"The routine has crashed: {error}")
                else:
                    message.update_data(output_data)
                    self.message_handler.put(message)

        self.cleanup()
