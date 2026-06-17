"""Módulo de configuração do logger.

Fornece uma instância compartilhada `logger` (do Loguru) para ser importada
por todo o job para registro consistente. Sinks adicionais ou formatação
podem ser configurados centralmente aqui no futuro, se necessário.
"""

from loguru import logger

__all__ = ["logger"]
