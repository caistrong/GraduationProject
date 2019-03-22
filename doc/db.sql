DROP TABLE IF EXISTS `movie_info`;
CREATE TABLE `movie_info` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `title` varchar(128) COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT '标题',
  `directors` varchar(256) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '导演',
  `screenwriters` varchar(256) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '编剧',
  `types` varchar(256) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '类型',
  `nations` varchar(256) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '国家/地区',
  `languages` varchar(256) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '语言',
  `releaseDate` varchar(256) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '上映日期',
  `year` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '年份',
  `duration` varchar(128) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '片长(分)',
  `actors` varchar(1024) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '演员列表',
  `knownAs` varchar(512) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '又名',
  `doubanId` int(10) unsigned DEFAULT NULL COMMENT '对应的豆瓣电影id',
  `imdbId` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '对应的imdb的id',
  `posterUrl` varchar(512) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '海报图片链接',
  `star` tinyint(4) DEFAULT NULL,
  `rate` tinyint(4) unsigned DEFAULT NULL COMMENT '评分(87代表豆瓣8.7分)',
  `votesNum` int(10) unsigned DEFAULT NULL COMMENT '评分人数',
  `fiveStarRatio` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '五星占比',
  `fourStarRatio` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '四星占比',
  `threeStarRatio` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '三星占比',
  `twoStarRatio` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '两星占比',
  `oneStarRatio` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '一星占比',
  `summary` longtext COLLATE utf8mb4_unicode_520_ci COMMENT '电影简介',
  `posterX` int(11) DEFAULT NULL COMMENT '海报宽度',
  `posterY` int(11) DEFAULT NULL COMMENT '海报高度',
  `doubanUrl` varchar(256) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '该电影豆瓣链接',
  `createdTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  `playLinks` longtext COLLATE utf8mb4_unicode_520_ci COMMENT '播放链接',
  PRIMARY KEY (`id`),
  UNIQUE KEY `doubanId_UNIQUE` (`doubanId`)
) ENGINE=InnoDB AUTO_INCREMENT=623 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci

DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `openId` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '用户openId',
  `sessionKey` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '会话密钥',
  `unionId` varchar(45) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '用户开放平台唯一标识',
  `userInfo` varchar(512) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '用户信息',
  `createdTime` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `openId_UNIQUE` (`openId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;