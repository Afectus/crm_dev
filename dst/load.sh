#!/bin/bash


./manage.py loaddata --format=xml na_dump/node_base1c.xml

./manage.py loaddata --format=xml na_dump/node_pricetype.xml
./manage.py loaddata --format=xml na_dump/node_kontragent.xml
./manage.py loaddata --format=xml na_dump/node_organization.xml
./manage.py loaddata --format=xml na_dump/node_shopstock.xml
./manage.py loaddata --format=xml na_dump/node_shop.xml
./manage.py loaddata --format=xml na_dump/node_stock.xml
./manage.py loaddata --format=xml na_dump/node_qinstock.xml
./manage.py loaddata --format=xml na_dump/node_cashbox.xml
./manage.py loaddata --format=xml na_dump/node_hozoperation.xml
./manage.py loaddata --format=xml na_dump/node_goodscert.xml
./manage.py loaddata --format=xml na_dump/node_tax.xml



./manage.py loaddata --format=xml na_dump/node_goodsmotivationratiosum.xml
./manage.py loaddata --format=xml na_dump/node_goods.xml
./manage.py loaddata --format=xml na_dump/node_goodsinstock.xml
./manage.py loaddata --format=xml na_dump/node_relgoods.xml
./manage.py loaddata --format=xml na_dump/node_pricegoods.xml


./manage.py loaddata --format=xml na_dump/node_baseunit.xml
./manage.py loaddata --format=xml na_dump/node_properties.xml
./manage.py loaddata --format=xml na_dump/node_propertiesvalue.xml
./manage.py loaddata --format=xml na_dump/node_buyer.xml
./manage.py loaddata --format=xml na_dump/node_discountcard1.xml
./manage.py loaddata --format=xml na_dump/node_discountcard.xml

./manage.py loaddata --format=xml na_dump/node_child.xml
./manage.py loaddata --format=xml na_dump/node_buyerevent.xml
./manage.py loaddata --format=xml na_dump/node_buyerrel.xml
./manage.py loaddata --format=xml na_dump/node_barcodelist.xml
./manage.py loaddata --format=xml na_dump/node_discounts.xml


