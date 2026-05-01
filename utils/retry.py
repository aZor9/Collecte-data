"""
utils/retry.py

Décorateur et utilitaire pour les retry automatiques.
"""

import random
import time
from functools import wraps
from typing import Any, Callable, TypeVar

from utils.logger import get_logger

logger = get_logger()

T = TypeVar('T')


def retry(max_attempts: int = 3, delay_min: float = 1.0, delay_max: float = 3.0):
    """
    Décorateur pour retry automatique avec délai exponentiel.
    
    Args:
        max_attempts: Nombre maximum de tentatives
        delay_min: Délai min entre les tentatives (secondes)
        delay_max: Délai max entre les tentatives (secondes)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt < max_attempts:
                        delay = random.uniform(delay_min, delay_max)
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt}/{max_attempts}). "
                            f"Retry in {delay:.1f}s... Error: {str(e)[:100]}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts. "
                            f"Final error: {str(e)}"
                        )
            
            raise last_exception
        
        return wrapper
    
    return decorator
