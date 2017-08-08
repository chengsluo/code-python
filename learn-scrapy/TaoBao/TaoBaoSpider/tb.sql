/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50715
 Source Host           : localhost
 Source Database       : tb

 Target Server Type    : MySQL
 Target Server Version : 50715
 File Encoding         : utf-8

 Date: 03/17/2017 15:29:49 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `product`
-- ----------------------------
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `dt` tinyint(1) DEFAULT '0' COMMENT '删除标志',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `id` varchar(36) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `comment_num` int(20) DEFAULT NULL COMMENT '产品的评分次数',
  `sale_num` int(20) DEFAULT NULL COMMENT '销量',
  `shop_price` char(20) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '店内价格',
  `standard_price` char(20) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '标准价格',
  `collect_num` char(20) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '收藏数量',
  `nid` varchar(36) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '产品ID',
  `shop_id` varchar(36) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '产品的店铺ID',
  `pay_num` int(20) DEFAULT NULL COMMENT '付款人数（淘宝是销量、天猫是月销量）',
  `url` varchar(225) COLLATE utf8mb4_bin DEFAULT NULL,
  `raw_html` text COLLATE utf8mb4_bin,
  `month_sale_num` int(20) DEFAULT '0',
  `search_key` varchar(225) COLLATE utf8mb4_bin DEFAULT NULL,
  `cid` varchar(225) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC;

-- ----------------------------
--  Table structure for `shop`
-- ----------------------------
DROP TABLE IF EXISTS `shop`;
CREATE TABLE `shop` (
  `create_time` datetime(6) DEFAULT NULL COMMENT '创建时间',
  `dt` tinyint(1) DEFAULT '0' COMMENT '删除标志',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_time` datetime DEFAULT NULL COMMENT '删除时间',
  `id` varchar(36) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `shop_name` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '店铺名',
  `rid` int(11) DEFAULT NULL COMMENT '店铺类目编号',
  `created` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '开店时间',
  `modified` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL COMMENT '店铺修改时间',
  `type` tinyint(4) DEFAULT '1',
  `url` varchar(225) COLLATE utf8mb4_bin DEFAULT NULL,
  `raw_html` text COLLATE utf8mb4_bin,
  `shop_id` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `seller_id` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `seller_nick` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `search_key` varchar(225) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
