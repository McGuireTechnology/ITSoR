class BaseUseCase:
    @staticmethod
    def require_exists(item: object | None, message: str) -> object:
        if item is None:
            raise ValueError(message)
        return item
