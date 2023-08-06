from SlyUWU import *

async def test_readme():

    uwu = UWURandom()

    random = await uwu.of_length(20)

    print(random)
    assert len(random) == 20