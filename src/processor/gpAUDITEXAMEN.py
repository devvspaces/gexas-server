import time

from logger import err_logger, logger

from .classGenerarGraficosMPL import generarGraficosMPL
from .classProcesarCSV import procesarCSV


class ProcessException(Exception):
    pass


def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        logger.info(
            f'Function {func.__name__} took {time.time() - start} seconds')
        return result
    return wrapper


@log_time
def process_file(path: str):
    processed = procesarCSV(path)
    if processed.ERROR != '':
        err_logger.error(processed.ERROR)
        raise ProcessException(processed.ERROR)
    return processed


@log_time
def generate_graph(processed: procesarCSV, graph_id: str):
    return generarGraficosMPL(processed.GRAFNOTAS, processed.RESPxPREG, processed.DISCRIMINACION, processed.FACILIDAD, processed.MARCAJESPREG, processed.RESPCORR, processed.ESTNOTAS, graph_id)
