import functools
import psutil
import os
import time
from typing import Callable, Optional

# Configuration class to hold custom settings
class Config:
    custom_logger: Optional[Callable[[str], None]] = None
    cpu_format: str = "Function {name}: CPU usage={cpu_usage}%"
    ram_format: str = "Function {name}: RAM usage={ram_usage}MB"

def custom_log(message: str) -> None:
    if Config.custom_logger:
        Config.custom_logger(message)
    else:
        print(message)

def u_cpu(func: Callable) -> Callable:
    """
    Decorator to monitor CPU usage of a function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Measure CPU usage before
        cpu_before = psutil.cpu_percent(interval=None)
        
        result = func(*args, **kwargs)

        # Measure CPU usage after
        cpu_after = psutil.cpu_percent(interval=None)
        cpu_usage = cpu_after - cpu_before

        # Logging CPU usage
        message = Config.cpu_format.format(name=func.__name__, cpu_usage=cpu_usage)
        custom_log(message)

        return result
    return wrapper

def u_ram(func: Callable) -> Callable:
    """
    Decorator to monitor RAM usage of a function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        # Measure RAM before
        mem_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB

        result = func(*args, **kwargs)

        # Measure RAM after
        mem_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
        ram_usage = mem_after - mem_before

        # Logging RAM usage
        message = Config.ram_format.format(name=func.__name__, ram_usage=ram_usage)
        custom_log(message)

        return result
    return wrapper

# Functions to set custom logger and format
def set_custom_logger(logger_func: Callable[[str], None]) -> None:
    Config.custom_logger = logger_func

def set_cpu_format(format_str: str) -> None:
    Config.cpu_format = format_str

def set_ram_format(format_str: str) -> None:
    Config.ram_format = format_str
