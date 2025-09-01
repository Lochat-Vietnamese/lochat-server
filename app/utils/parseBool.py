class ParseBool:
    @staticmethod
    def __new__(cls, value):
        if value is None or value == "" or value in ("None", "none"):
            return None
        val = str(value).lower().strip()
        if val in ("true", "1", "yes", "y"):
            return True
        if val in ("false", "0", "no", "n"):
            return False
        return None
