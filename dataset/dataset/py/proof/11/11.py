def test_vmagent_missing_get_chain():
    data = {}
    result = data.get('vmAgent', {'default': None}).get('version')
    assert result is None

def test_vmagent_present_get_chain():
    data = {'vmAgent': {'version': '1.2.3'}}
    result = data.get('vmAgent', {'default': None}).get('version')
    assert result == '1.2.3'

def test_direct_indexing_raises_keyerror():
    data = {}
    try:
        _ = data['vmAgent']['version']
        assert False, "Expected KeyError when using direct indexing on missing vmAgent"
    except KeyError:
        pass
