# unmatched.gg-profile-lists-bot
its a discord bot that shows unmatched.gg profiles saved in database
* Import this into mysql 
```
CREATE TABLE `unmatched_links` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `link` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
