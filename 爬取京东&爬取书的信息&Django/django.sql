/*
MySQL Data Transfer
Source Host: localhost
Source Database: test
Target Host: localhost
Target Database: test
Date: 2019/4/25 15:14:39
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for tb_user
-- ----------------------------
CREATE TABLE `tb_user` (
  `id` int(11) NOT NULL auto_increment,
  `u_name` varchar(20) NOT NULL,
  `u_pass` varchar(20) default NULL,
  `xb` char(4) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records 
-- ----------------------------
INSERT INTO `tb_user` VALUES ('1', 'hml', '1111', '');
INSERT INTO `tb_user` VALUES ('2', 'hhh', '222', null);
INSERT INTO `tb_user` VALUES ('3', 'ghj', '333', null);
INSERT INTO `tb_user` VALUES ('4', 'ghu', '444', null);
INSERT INTO `tb_user` VALUES ('5', 'ads', '555', null);
INSERT INTO `tb_user` VALUES ('6', 'dfg', '666', null);
INSERT INTO `tb_user` VALUES ('7', 'fff', '777', null);
