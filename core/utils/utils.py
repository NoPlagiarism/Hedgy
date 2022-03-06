__all__ = [
    "lambda_awaited",
]


def lambda_awaited(async_iter):
    return async_iter.__anext__()
