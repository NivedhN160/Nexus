class PresenceProvider:
    def __init__(self):
        self.is_present = False
        
    def set_presence(self, status: bool):
        self.is_present = status
        
    def get_context(self) -> str:
        if self.is_present:
            return "User appears to be present at their desk."
        return "User is currently away."

mock_presence = PresenceProvider()
