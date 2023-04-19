import logging as logger


class State:
    def __init__(self):
        self.current_state = "not_running"

    def set_busy_state(self) -> bool:
        try:
            self.current_state = "busy_running"
            logger.info("State set to busy_running")
            return True
        except:
            logger.error("Error in set_busy_state")
            pass
        finally:
            self.current_state = "not_running"
        return False

    def set_idle_state(self) -> bool:
        try:
            self.current_state = "not_running"
            return True
        except:
            logger.error("Error in set_idle_state")
            pass

        return False

    def isStateBusy(self) -> bool:
        if self.current_state == "busy_running":
            return True
        else:
            return False


state = State()
