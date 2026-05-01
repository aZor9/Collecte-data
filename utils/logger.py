"""
utils/logger.py

Système de logging unifié.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

from config.settings import LOGS_DIR


class Logger:
    """Logger centralisé pour le projet."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Créer timestamp pour les logs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOGS_DIR / f"pipeline_{timestamp}.log"
        
        # Setup logger
        self.logger = logging.getLogger("DataPipeline")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler fichier
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        
        # Handler console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def critical(self, message: str):
        self.logger.critical(message)


def get_logger() -> Logger:
    """Retourner l'instance du logger."""
    return Logger()
