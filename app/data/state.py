class State:
  def __init__(self):
    self.current_state = "not_running"

  def set_current_state(self, current_state: str) -> None:
    self.current_state = current_state
  
  def get_current_state(self) -> str:
    return self.current_state

state = State()