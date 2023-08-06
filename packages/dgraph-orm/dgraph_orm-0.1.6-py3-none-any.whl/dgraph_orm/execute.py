import os
import time
import requests
from . import GQLException

URL = os.environ["DGRAPH_URL"]


def execute(query_str: str, should_print: bool = False) -> dict:
    start = time.time()
    j = requests.post(URL, json={"query": query_str}).json()
    print(
        f'took: {(time.time() - start) * 1000}, took internal: {int(j["extensions"]["tracing"]["duration"]) / (10 ** 6)}'
    )
    if should_print:
        print(f"{query_str=}, {j=}")
    if "data" not in j:
        raise GQLException(f"data not in j!, {j=}, {query_str=}")
    return j
