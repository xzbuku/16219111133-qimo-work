CREATE TABLE `lagou_job` (
  `url` varchar(300) NOT NULL COMMENT '拉钩url地址',
  `url_object_id` varchar(50) NOT NULL COMMENT 'url的hashid',
  `title` varchar(100) NOT NULL COMMENT '招聘标题',
  `salary` varchar(20) DEFAULT NULL COMMENT '薪资',
  `job_city` varchar(10) DEFAULT NULL COMMENT '工作城市',
  `work_years` varchar(100) DEFAULT NULL COMMENT '工作年限',
  `degree_need` varchar(30) DEFAULT NULL COMMENT '学历要求',
  `job_type` varchar(20) DEFAULT NULL COMMENT '工作类型(全职/兼职)',
  `publish_time` varchar(20) NOT NULL COMMENT '发布时间',
  `tags` varchar(100) DEFAULT NULL COMMENT '工作标签',
  `job_advantage` varchar(1000) DEFAULT NULL COMMENT '福利待遇',
  `job_desc` longtext NOT NULL COMMENT '工作描述',
  `job_addr` varchar(50) DEFAULT NULL COMMENT '工作地点',
  `company_url` varchar(300) DEFAULT NULL COMMENT '公司网址url',
  `company_name` varchar(100) DEFAULT NULL COMMENT '公司名称',
  `crawl_time` datetime NOT NULL COMMENT '抓取时间',
  `crawl_update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

