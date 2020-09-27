# Blogging
Create a blog-like website with preview list and photo wall
Use **PTT** as our blog source (posts, images, and user...)

## Introduction
1. Practice goals
    - Pagination
    - More complicated database schema design
    - Message Queue (Celery)
    - Performance consideration

2. Functionality
    - See the post
    - Preview post list board by board
    - Photo wall board by board
    - Crawler task control by admin
    - Advance
        - Post search by user, title, and content


## Procedure
### Week1: Spider, Task control, and Frontend template
- [x] Use [PttSpider](https://github.com/n3k0fi5t/PttSpider) as Crawler
- [x] thread-base task queue

![](https://github.com/n3k0fi5t/Django_Tutorial/blob/master/ptt_blog/img/task_collection.png)

### Week2: Preview and Post

