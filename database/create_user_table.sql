CREATE TABLE `users` (
  `username` varchar(20) NOT NULL,
  `password` varchar(45) NOT NULL,
  `ELORating` int DEFAULT '0',
  `gameMode` varchar(45) DEFAULT 'local',
  `boardColor` varchar(45) DEFAULT 'green',
  `boardSize` int DEFAULT '4',
  `aiLevel` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`username`),
  CONSTRAINT `user_has_ai_with_level` CHECK (((`aiLevel` <> 0) or (`gameMode` <> _utf8mb4'AI')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
