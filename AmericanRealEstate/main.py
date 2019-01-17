# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: main.py
@time: 2019/1/9
"""
from scrapy.cmdline import execute


# execute('scrapy crawl realtor -s JOBDIR=crawls/trulia_state_county_zip-1'.split(' '))
execute('scrapy crawl realtor'.split(' '))


