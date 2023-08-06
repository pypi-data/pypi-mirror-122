from typing import Type

from .._exceptions import PostContractError
from .base import Base, CallableType


class Post(Base[CallableType]):
    """
    Check contract (validator) after function processing.
    Validate output result.
    """

    @classmethod
    def _default_exception(cls) -> Type[PostContractError]:
        return PostContractError

    def patched_function(self, *args, **kwargs):
        """
        Step 3. Wrapped function calling.
        """
        result = self.function(*args, **kwargs)
        self.validate(result)
        return result

    async def async_patched_function(self, *args, **kwargs):
        """
        Step 3. Wrapped function calling.
        """
        result = await self.function(*args, **kwargs)
        self.validate(result)
        return result

    def patched_generator(self, *args, **kwargs):
        """
        Step 3. Wrapped function calling.
        """
        for result in self.function(*args, **kwargs):
            self.validate(result)
            yield result
