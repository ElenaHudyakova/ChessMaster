/*
 Navicat MySQL Data Transfer

 Source Server         : localhost
 Source Server Version : 50524
 Source Host           : localhost
 Source Database       : chess

 Target Server Version : 50524
 File Encoding         : utf-8

 Date: 06/20/2012 22:44:31 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `games`
-- ----------------------------
DROP TABLE IF EXISTS `games`;
CREATE TABLE `games` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `event` varchar(30) DEFAULT NULL,
  `site` varchar(30) DEFAULT NULL,
  `date` varchar(10) DEFAULT NULL,
  `round` varchar(10) DEFAULT NULL,
  `white` varchar(30) DEFAULT NULL,
  `black` varchar(30) DEFAULT NULL,
  `result` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9914 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `moves`
-- ----------------------------
DROP TABLE IF EXISTS `moves`;
CREATE TABLE `moves` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `game_id` bigint(20) DEFAULT NULL,
  `notation` varchar(10) DEFAULT NULL,
  `fullmove_number` int(11) DEFAULT NULL,
  `color` int(5) DEFAULT NULL,
  `serial1` decimal(65,0) DEFAULT NULL,
  `serial2` decimal(65,0) DEFAULT NULL,
  `serial3` decimal(65,0) DEFAULT NULL,
  `serial0` decimal(65,0) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `game_id` (`game_id`)
) ENGINE=InnoDB AUTO_INCREMENT=672517 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
