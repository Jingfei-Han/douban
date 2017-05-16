# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class MySQLPipeline(object):
	def __init__(self, dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls, settings):
		dbargs = dict(
			host = settings['MYSQL_HOST'],
			db = settings['MYSQL_DBNAME'],
			user = settings['root'],
			passwd = settings['MYSQL_PASSWD'],
			charset = 'utf8',
			cursorclass = MySQLdb.cursors.DictCursor,
			use_unicode = True,

		)
		dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
		return cls(dbpool)

	def process_item(self, item, spider):
		d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
		d.addBoth(lambda _: item)
		return d

	def _do_upinsert(self, conn, item, spider):
		sql1 = "INSERT INTO top250(top250_id, top250_title, top250_star, top250_year, top250_country, top250_type, top250_quote)\
			VALUES(%d, %s, %f, %d, %s, %s, %s)"
		try:
			conn.execute(sql1, (item['index'], item['title'], item['star'], item['year'], item['country'], item['doubantype'], item['quote']))
		except:
			print "Insert failed!"