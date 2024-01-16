SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `ui`.`calculate`;
CREATE TABLE `ui`.`calculate`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `UId` int NULL DEFAULT NULL,
  `Mod` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Date` date NULL DEFAULT NULL,
  `Time` time NULL DEFAULT NULL,
  `Total` int NULL DEFAULT NULL,
  `Easy` int NULL DEFAULT NULL,
  `Media`int NULL DEFAULT NULL,
  `Difficult` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `UId`(`UId` ASC) USING BTREE,
  CONSTRAINT `bills_ibfk_1` FOREIGN KEY (`UId`) REFERENCES `ui`.`users` (`userID`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of bills
-- ----------------------------
INSERT INTO `ui`.`calculate` VALUES (1, 2,'MOD1', '2022-02-20', '12:15:20', 300,250,25,50);
INSERT INTO `ui`.`calculate` VALUES (2, 2, 'MOD1','2023-06-21', '15:55:33', 750,250,250,250);
INSERT INTO `ui`.`calculate` VALUES (3, 3, 'MOD2','2023-12-03', '19:51:41', 550,250,100,100);
INSERT INTO `ui`.`calculate` VALUES (4, 1, 'MOD1','2023-12-05', '1:58:31', 525,250,25,250);
INSERT INTO `ui`.`calculate` VALUES (5, 2, 'MOD2','2023-12-03', '19:00:41', 600,150,250,200);
