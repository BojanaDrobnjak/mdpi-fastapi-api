import time
from typing import Union


class TokenBucket:
    """Basic rate limiter using token bucket algorithm."""

    def __init__(self, capacity: Union[int, float], refill_rate: Union[int, float]):
        # Initialize the token bucket
        self.capacity = capacity  # Maximum number of tokens in the bucket
        self.refill_rate = refill_rate  # Rate at which tokens are added to the bucket
        # per second
        self.tokens = capacity  # Start with the bucket full
        self.last_refill = time.time()  # Record the time when the bucket
        # was last refilled

    def add_tokens(self) -> None:
        """Add tokens to the bucket."""
        # Add tokens to the bucket based on the time elapsed since the last refill
        now = time.time()
        if self.tokens < self.capacity:
            # Calculate the number of tokens to add
            tokens_to_add = (now - self.last_refill) * self.refill_rate
            # Update the token count, ensuring it doesn't exceed the capacity
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now  # Update the last refill time

    def take_token(self) -> bool:
        """
        Attempt to take a token from the bucket.

        :return: True if a token was successfully taken, False otherwise.
        """
        # Attempt to take a token from the bucket
        self.add_tokens()  # Ensure the bucket is refilled based on the elapsed time
        if self.tokens >= 1:
            self.tokens -= 1  # Deduct a token for the API call
            return True  # Indicate that the API call can proceed
        return False  # Indicate that the rate limit has been exceeded
