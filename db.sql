select * from watermgmtapi_post

alter table watermgmtapi_posts rename to watermgmtapi_post


select * from watermgmtapi_post_likes

alter table watermgmtapi_postlikes rename to watermgmtapi_postlike


SELECT name FROM sqlite_master WHERE type='table' AND name='watermgmtapi_postlike';

PRAGMA table_info(watermgmtapi_postlike);

