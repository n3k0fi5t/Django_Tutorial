import threading

from django.db import transaction
from .models import CrawlTask, TaskStatus

from .PttSpider.ptt_spider import PttArticleListSpider, PttArticleSpider
from .PttSpider.ptt_spider import Push, ArticleInfo
from .PttSpider.ptt_spider import PttUrl, PttUrlType

from .taskpool import TaskPool

TASK_POOL_SIZE = 5

def set_task_status(task, status):
    with transaction.atomic():
        task.status = status
        task.save(update_fields=['status', 'update_time'])

def put_task_error(task):
    set_task_status(task, TaskStatus.ERROR)
    raise

def board_handler(board_url):
    spider = PttArticleListSpider(board_url, max_fetch=10)
    spider.run()

    url_list = spider.article_url_list
    if len(url_list) == 0:
        return []

    article_list = []
    for url in url_list:
        try:
            spider = PttArticleSpider(url)
            spider.run()
            article = spider.article
        except Exception as e:
            print(f"Get Exception {e}")
            article = ArticleInfo()
        finally:
            article_list.append(spider.article)

    return article_list

def get_parsing_handler(url):
    url_type = PttUrl(url).type
    if url_type != PttUrlType.BOARD:
        return None

    return board_handler

def c_task(tid, url):
    try:
        with transaction.atomic():
            task = CrawlTask.objects.get(id=tid)
    except CrawlTask.DoesNotExist as e:
        print(f"Get task error {e}")
        raise

    set_task_status(task, TaskStatus.RUNNING)

    handler = get_parsing_handler(url)
    if handler is None:
        put_task_error(task)

    try:
        article_list = handler(url)
    except Exception as e:
        put_task_error(task)

    #create_posts(article_list)
    set_task_status(task, TaskStatus.FINISH)

m = None

def crawler_init():
    global m
    def start_monitor():
        def monitor():
            m.run()
        threading.Thread(target=monitor).start()
        print("start monitoring")

    if m is not None:
        return

    objs = CrawlTask.objects.exclude(status=TaskStatus.ERROR)
    objs.update(status=TaskStatus.FINISH)

    m = TaskPool(TASK_POOL_SIZE)
    start_monitor()

def create_crawl_task(url):
    with transaction.atomic():
        task, _ = CrawlTask.objects.get_or_create(
            url=url,
            defaults={'name':url, 'url':url, 'status':TaskStatus.QUEUING},
        )
    
    try:
        success = m.add(c_task, task.id, task.id, url)
        if not success:
            set_task_status(task, TaskStatus.ERROR)
    except Exception as e:
        success = False
        print("add task fail")
    
    return success

__all__ = ['crawler_init' , 'create_crawl_task']