def api_success_resp(code: int, status: str, data: dict) -> object:
    return {'code': code, 'status': status, 'data': data}


def api_failure_resp(code: int, status: str, error: dict) -> object:
    return {'code': code, 'status': status, 'error': error}
