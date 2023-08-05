class Stateful:
    """Stateful implementation."""
    CLOSED = 0
    CLOSING = 1
    OPENING = 2
    OPEN = 3

    def __init__(self):
        self._state = self.CLOSED

    def set_state(self, state):
        """Set State.
        :param int state:
        :return:
        """
        self._state = state

    @property
    def current_state(self):
        """Get the State.
        :rtype: int
        """
        return self._state

    @property
    def is_closed(self):
        """Is Closed?
        :rtype: bool
        """
        return self._state == self.CLOSED

    @property
    def is_closing(self):
        """Is Closing?
        :rtype: bool
        """
        return self._state == self.CLOSING

    @property
    def is_opening(self):
        """Is Opening?
        :rtype: bool
        """
        return self._state == self.OPENING

    @property
    def is_open(self):
        """Is Open?
        :rtype: bool
        """
        return self._state == self.OPEN
