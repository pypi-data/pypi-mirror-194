class CliColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def green(cls, string: str) -> str:
        return f"{cls.OK_GREEN}{string}{cls.ENDC}"

    @classmethod
    def blue(cls, string: str) -> str:
        return f"{cls.OK_BLUE}{string}{cls.ENDC}"

    @classmethod
    def cyan(cls, string: str) -> str:
        return f"{cls.OK_CYAN}{string}{cls.ENDC}"

    @classmethod
    def warning(cls, string: str) -> str:
        return f"{cls.WARNING}{string}{cls.ENDC}"

    @classmethod
    def fail(cls, string: str) -> str:
        return f"{cls.FAIL}{string}{cls.ENDC}"
