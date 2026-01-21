"""Example of fastapi main file with custom memory metrics."""
import os
import psutil
from typing import Union
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge

app = FastAPI()

# Definición de la métrica personalizada con el sufijo requerido
# Usamos un Gauge porque la memoria puede subir y bajar
MEMORY_USAGE_METRIC = Gauge(
    'app_memory_usage_0oqfemca',
    'Current memory usage of the application in bytes'
)

@app.get("/actuator/prometheus")
def metrics():
    """Exposes custom metrics in Prometheus format."""
    # Actualizamos el valor antes de servir la petición
    process = psutil.Process(os.getpid())
    memory_in_bytes = process.memory_info().rss
    MEMORY_USAGE_METRIC.set(memory_in_bytes)

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/")
def read_root():
    """Returns Hello World."""
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, item_count: Union[str, None] = None):
    """Returns numbers of items."""
    return {"item_id": item_id, "q": item_count}
