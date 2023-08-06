def test_get_rpc_schema(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, dict)
        assert "openrpc" in response

    _assert(CLIENT.queries.get_rpc_schema())


def test_get_rpc_endpoints(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, list)
        print(response)
        print(sorted(CLIENT.NODE_RPC_ENDPOINTS))
        assert response == sorted(CLIENT.NODE_RPC_ENDPOINTS)

    _assert(CLIENT.queries.get_rpc_endpoints())


def test_get_rpc_endpoint(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_discover.json
        assert isinstance(response, dict)        

    for endpoint in CLIENT.NODE_RPC_ENDPOINTS:
        _assert(CLIENT.queries.get_rpc_endpoint(endpoint))
