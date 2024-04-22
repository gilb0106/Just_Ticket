-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema ticketsystem
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `ticketsystem` ;

-- -----------------------------------------------------
-- Schema ticketsystem
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ticketsystem` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `ticketsystem` ;

-- -----------------------------------------------------
-- Table `ticketsystem`.`userrole`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ticketsystem`.`userrole` ;

CREATE TABLE IF NOT EXISTS `ticketsystem`.`userrole` (
  `RoleID` INT NOT NULL AUTO_INCREMENT,
  `RoleName` ENUM('agent', 'customer') NOT NULL,
  PRIMARY KEY (`RoleID`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `ticketsystem`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ticketsystem`.`user` ;

CREATE TABLE IF NOT EXISTS `ticketsystem`.`user` (
  `UserID` INT NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(255) NOT NULL,
  `Password` VARCHAR(255) NOT NULL,
  `RoleID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  INDEX `fk_user_role` (`RoleID` ASC) VISIBLE,
  CONSTRAINT `fk_user_role`
    FOREIGN KEY (`RoleID`)
    REFERENCES `ticketsystem`.`userrole` (`RoleID`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `ticketsystem`.`ticket`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ticketsystem`.`ticket` ;

CREATE TABLE IF NOT EXISTS `ticketsystem`.`ticket` (
  `TicketNumber` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `UserID` INT NULL DEFAULT NULL,
  `TicketContent` VARCHAR(255) NOT NULL,
  `State` ENUM('open', 'inprogress', 'closed') NOT NULL,
  `Created` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `Modified` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`TicketNumber`),
  INDEX `fk_ticket_user` (`UserID` ASC) VISIBLE,
  CONSTRAINT `fk_ticket_user`
    FOREIGN KEY (`UserID`)
    REFERENCES `ticketsystem`.`user` (`UserID`))
ENGINE = InnoDB
AUTO_INCREMENT = 100011
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `ticketsystem`.`ticketcomment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ticketsystem`.`ticketcomment` ;

CREATE TABLE IF NOT EXISTS `ticketsystem`.`ticketcomment` (
  `CommentID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `TicketNumber` INT UNSIGNED NOT NULL,
  `UserID` INT NOT NULL,
  `CommentContent` TEXT NOT NULL,
  `CommentDate` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`CommentID`),
  INDEX `fk_ticketcomment_ticket` (`TicketNumber` ASC) VISIBLE,
  INDEX `fk_ticketcomment_user` (`UserID` ASC) VISIBLE,
  CONSTRAINT `fk_ticketcomment_ticket`
    FOREIGN KEY (`TicketNumber`)
    REFERENCES `ticketsystem`.`ticket` (`TicketNumber`),
  CONSTRAINT `fk_ticketcomment_user`
    FOREIGN KEY (`UserID`)
    REFERENCES `ticketsystem`.`user` (`UserID`))
ENGINE = InnoDB
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `ticketsystem`.`useractivity`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ticketsystem`.`useractivity` ;

CREATE TABLE IF NOT EXISTS `ticketsystem`.`useractivity` (
  `ActivityID` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `UserID` INT NOT NULL,
  `ActivityType` ENUM('login', 'logout', 'ticket_create', 'ticket_update') NOT NULL,
  `ActivityDate` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ActivityID`),
  INDEX `fk_useractivity_user` (`UserID` ASC) VISIBLE,
  CONSTRAINT `fk_useractivity_user`
    FOREIGN KEY (`UserID`)
    REFERENCES `ticketsystem`.`user` (`UserID`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
