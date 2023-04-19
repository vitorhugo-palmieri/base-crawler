from scrapy.utils.log import configure_logging
from logging.handlers import RotatingFileHandler
import logging
import os
from log4mongo.handlers import MongoHandler
from base_crawler.log_formatters.mongo_formatter import MongoFormatter

# Scrapy settings for base crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "base-crawler"

# In production, this env should be set to the string "false"
DEBUG_MODE = os.environ.get("DEBUG_MODE", "true")

SPIDER_MODULES = ["base_crawler.spiders", "spiders", "tests.spiders"]
SPIDER_LOADER_WARN_ONLY = True
NEWSPIDER_MODULE = "base_crawler.spiders"
DUPEFILTER_CLASS = "scrapy.dupefilters.BaseDupeFilter"

STATS_CLASS = "base_crawler.stats_collector.MongoStatsCollector"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'base_crawler.middlewares.SpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'base_crawler.middlewares.DownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
SPIDERMON_ENABLED = True

EXTENSIONS = {
    "spidermon.contrib.scrapy.extensions.Spidermon": 500,
}
SPIDERMON_EXPECTED_FINISH_REASONS = ["finished", "all_data_scraped"]
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "base_crawler.pipelines.item_prepare_pipeline.ItemPreparePipeline": 100,
    "base_crawler.pipelines.schema_validation_pipeline.SchemaValidationPipeline": 200,
    "base_crawler.pipelines.mongo_pipeline.MongoPipeline": 300,
    #"base_crawler.pipelines.transformer.transformer_pipeline.TransformerPipeline": 400,
    #'base_crawler.pipelines.elastic_pipeline.ElasticPipeline': 500
}

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"

if DEBUG_MODE == "false":
    LOG_ENABLED = True
else:
    LOG_ENABLED = False
    # Disable default Scrapy log settings.
    configure_logging(install_root_handler=False)

    # Define your logging settings.
    log_file = "/app/tests/files/debug/logs.txt"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    rotating_file_log = RotatingFileHandler(log_file, maxBytes=2000000, backupCount=10)
    rotating_file_log.setLevel(logging.DEBUG)
    rotating_file_log.setFormatter(formatter)
    root_logger.addHandler(rotating_file_log)


logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
mongo_handler = MongoHandler(
    host=os.environ.get("MONGO_HOST") or "mongo",
    formatter=MongoFormatter(),
    database_name=os.environ.get("LOG_DATABASE") or "crawler_logs",
    collection=os.environ.get("SPIDER_NAME") or "crawler_logs",
    level=LOG_LEVEL,
)
logger.addHandler(mongo_handler)


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

CLOSESPIDER_ERRORCOUNT = 1
SPIDER_LOADER_WARN_ONLY = True
