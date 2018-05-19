# -*- coding: utf-8 -*-
#!usr/bin/env python
import requests

r = requests.get('https://blockchain.info/ru/ticker')
bitprice = (r.json()['RUB']['buy'])
bitpriceUSD = (r.json()['USD']['buy'])

