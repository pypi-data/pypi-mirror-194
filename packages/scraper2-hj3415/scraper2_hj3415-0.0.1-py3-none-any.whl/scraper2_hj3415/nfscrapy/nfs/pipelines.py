from itemadapter import ItemAdapter
from pymongo import errors


class MongoPipeline:

    collection_name = 'c101'

    def open_spider(self, spider):
        self.client = spider.mongo_client

    def process_item(self, item, spider):
        print("In the MongoPipeline...", end="")
        if self.client is None:
            print("Skip the save to mongoDB.")
        else:
            print("Save data to mongoDB.")
            my_collection = self.client[item['코드']][self.collection_name]
            try:
                my_collection.create_index('date', unique=True)
                my_collection.insert_one(ItemAdapter(item).asdict())
            except errors.DuplicateKeyError:
                # 스크랩한 데이터가 이미 데이터베이스에 있을경우 지우고 저장
                my_collection.delete_many({'date': {"$gte": item['date']}})
                my_collection.insert_one(ItemAdapter(item).asdict())
        return item
