def test_socfaker_products_elastic_hits(socfaker_fixture):
   assert socfaker_fixture.products.elastic.hits(count=1)

def test_socfaker_products_elastic_document(socfaker_fixture):
   assert socfaker_fixture.products.elastic.document