def assertHTTPCode(response, code_list=[200]):
    res_code = response.status_code
    if res_code not in code_list:
        raise AssertionError('响应code不在列表中！')