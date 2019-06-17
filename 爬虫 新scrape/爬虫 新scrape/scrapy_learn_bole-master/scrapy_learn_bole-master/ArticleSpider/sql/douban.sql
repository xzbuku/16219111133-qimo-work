CREATE TABLE douban
(
  url_hashid    VARCHAR(50)  NOT NULL
  COMMENT '根据url生成的唯一hash值'
    PRIMARY KEY,
  douban_url    VARCHAR(200) NOT NULL
  COMMENT '用户主页url',
  user_name     VARCHAR(20)  NOT NULL
  COMMENT '评论的用户名',
  is_view       VARCHAR(10)  NULL
  COMMENT '是否看过',
  star_number   VARCHAR(20)  NOT NULL
  COMMENT '评价',
  comment_time  DATETIME     NOT NULL
  COMMENT '评论时间',
  votes_numbers INT          NOT NULL
  COMMENT '投票有用数',
  short_comment LONGTEXT     NULL
  COMMENT '短评内容'
)
  ENGINE = InnoDB;

CREATE INDEX douban_comment_time_index
  ON douban (comment_time);
