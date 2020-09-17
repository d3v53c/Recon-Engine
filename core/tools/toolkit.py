from core.tools.state import State


class Toolkit(object):
    """
    Collection of each tools from the original repo.
    """
    tools = dict()

    def count(self):
        """
        Return total count of tools available.
        """
        return len(self.tools)

    def add(self, key, value):
        """
        Add a new tool to the inventory.
        TODO: Validate the new tool.
        """
        self.tools[key] = State(value)

    def remove(self, key):
        """
        Remove a tool from the inventory.
        TODO: Validate key and remove.
        """
        self.tools = {k: v for k, v in self.tools.items() if not key == k}

    def overview(self):
        """
        List of all keys included in the inventory.
        """
        return self.tools.keys()

    def run_all(self):
        """
        Run all tools in the inventory.
        """
        pass

    def nameof(self, key):
        """
        Returns name of the tool.
        """
        state = self.get_state(key)
        return state.name

    def get_state(self, key):
        """
        Returns state object of a tool if any or None
        """
        self.validate_key(key)
        return self.tools.get(key)

    def validate_key(self, key):
        """
        Returns True if key is valid else raises error.
        """
        if key in self.tools:
            return True
        raise ValueError("`key`: Invalid")