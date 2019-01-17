# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from AmericanRealEstate.tools.test_file import post_url


class AmericanrealestatePipeline(object):
    def process_item(self, item, spider):
        return item


class RealtorHouseInfoTestPipeline(object):
    house_list = []

    def process_item(self, item, spider):
        self.house_list.append(str(item['houseData']))
        if len(self.house_list) >= 3:
            print('数据显示',self.house_list)
            post_data = {
                "data": self.house_list
            }
            result = post_url('http://192.168.0.126:8080/America-DataSave/index/saveRealtorDataJson/', post_data)
            print(result == 'success')

            del self.house_list[:]
        return item