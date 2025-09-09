import logging

# Criar um handler específico para console
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

# Criar logger da aplicação
logger = logging.getLogger("gateway")
logger.setLevel(logging.INFO)

# Evitar handlers duplicados
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.propagate = False
