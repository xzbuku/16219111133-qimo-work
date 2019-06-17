/*
 Navicat MySQL Data Transfer

 Source Server         : sy
 Source Server Type    : MySQL
 Source Server Version : 50722
 Source Host           : localhost:3306
 Source Schema         : article_spider

 Target Server Type    : MySQL
 Target Server Version : 50722
 File Encoding         : 65001

 Date: 09/07/2018 22:31:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for jobbole_article
-- ----------------------------
DROP TABLE IF EXISTS `jobbole_article`;
CREATE TABLE `jobbole_article`  (
  `title` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '文章标题',
  `create_time` date NULL DEFAULT NULL COMMENT '文章创建时间',
  `url` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '文章url',
  `url_obejct_id` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '文章url的md5值',
  `front_image_url` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '每篇文章首页的图片路径',
  `front_image_path` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '图片下载的本地路径',
  `comment_nums` int(11) NOT NULL DEFAULT 0 COMMENT '评论数',
  `fav_nums` int(11) NOT NULL DEFAULT 0 COMMENT '收藏数',
  `parise_nums` int(11) NOT NULL DEFAULT 0 COMMENT '点赞数',
  `tags` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '文章标签',
  `content` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '文章具体内容',
  PRIMARY KEY (`url_obejct_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;