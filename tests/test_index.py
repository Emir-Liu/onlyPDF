from onlyPDF.index import index

def test_index():
    ret = index()

    assert ret == 'welcome to onlyPDF'