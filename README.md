# Python cbm bbs petscii
Python Commodore BBS multi-client
This is intended for commodore 64, c128 and most commodore compatible machines (as the new Commander X16 under development) 

This is a working Python 3.X script that will help you implement a Commodore Petscii BBS.

Included Files:

1) bbs.py -> main file. Just run in terminal user@yourcomputer:~/yourdirectory $ python3 bbs.py 

2) funct.py -> main bbs functions

3) head.seq -> a sequence (random chars) file generated with http://petscii.krissz.hu/ this is just to have "something" to show to the user.

## To start, first create the needed databases in MySQL with the following commands:

CREATE DATABASE `cbmbbs` /*!40100 DEFAULT CHARACTER SET utf8 */;

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `active` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `idx_accounts_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

CREATE TABLE `boards` (
  `idboard` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`idboard`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE `posts` (
  `idmessage` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `subject` varchar(128) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `idboard` int(11) DEFAULT NULL,
  `body` blob DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `idreply` int(11) DEFAULT NULL,
  PRIMARY KEY (`idmessage`),
  KEY `idx_boardmessages_userid` (`userid`),
  KEY `idx_boardmessages_boardid` (`idboard`),
  KEY `idx_boardmessages_date` (`date`),
  KEY `idx_boardmessages_replyid` (`idreply`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO boards (`idboard`,`name`) VALUES (1,'General');


