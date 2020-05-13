import sys
try:
    import pymysql
except:
    print("Library pymysql not installed. Run 'pip install mysql' and un the program again.")
import warnings
from datetime import date


# Variables to check valid inputs from the user
aux = 0
loop = True
check_menu = [1,2,3,4,5,6,7]
#check_menu = ['1', "2", "3", "4", "5", "6", "7"]
check_search = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
check_insert = ["1", "2", "3", "4", "5", "6", "7"]
check_update = ["1", "2", "3"]
check_book_update_options = ["1", "2", "3", "4"]
check_ebook_update_options = ["1", "2", "3", "4"]
check_audio_update_options = ["1", "2", "3", "4", "5"]
check_delete = ["1", "2", "3", "4", "5"]


# Read configuration file and get the values to connect to the database
with open("conf.txt") as config_file:
    host_input = config_file.readline().split(":")[1].strip()
    user_input = config_file.readline().split(":")[1].strip()
    password_input = config_file.readline().split(":")[1].strip()
    db_input = config_file.readline().split(":")[1].strip()

# Eliminate empty spaces in the database name
db_input = db_input.replace(" ", "")
# Eliminate quote marks in the database name
db_input = db_input.replace('"', "")

# Create database if not exist
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        database = pymysql.connect(host=host_input, user=user_input, password=password_input)
        cursor = database.cursor()
        database.commit()
        sql = "CREATE DATABASE IF NOT EXISTS " + db_input
        cursor.execute(sql)
        database.commit()
    except:
        print()

# Connection to the database
database = pymysql.connect(host=host_input, user=user_input, password=password_input, db=db_input)
cursor = database.cursor()
database.commit()

# Don't show non-existing table warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    ######################################################################################
    ############################## CREATE TABLES #########################################
    ######################################################################################
    # Create sys table
    sql = """CREATE TABLE IF NOT EXISTS `sys`(
                        `ssid` INT NOT NULL AUTO_INCREMENT,
                        `upid` INT,
                        `banid` INT,
                        `oid` INT,
                        `iid` INT,
                        PRIMARY KEY (`ssid`))"""
    cursor.execute(sql)
    database.commit()
    # Crete user table
    sql = """CREATE TABLE IF NOT EXISTS `user`(
                        `uid` INT NOT NULL AUTO_INCREMENT,
                        `age` INT NOT NULL,
                        `name` VARCHAR(45) NOT NULL,
                        `last_name` VARCHAR(45) NOT NULL,
                        `birthdate` DATE NOT NULL,
                        `ssid` INT NOT NULL,
                        PRIMARY KEY (`uid`),
                        FOREIGN KEY (`ssid`) REFERENCES sys(`ssid`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()
    # Create plagiarism_team table
    sql = """CREATE TABLE IF NOT EXISTS `plagiarism_team`(
                        `ptid` INT NOT NULL,
                        PRIMARY KEY (`ptid`))"""
    cursor.execute(sql)
    database.commit()
    # Create ban table
    sql = """CREATE TABLE IF NOT EXISTS `ban`(
                        `banid` INT NOT NULL,
                        `ptid` INT NOT NULL,
                        PRIMARY KEY (`banid`))"""
    cursor.execute(sql)
    database.commit()
    # Create publisher table
    sql = """CREATE TABLE IF NOT EXISTS `publisher`(
                        `pubid` INT NOT NULL,
                        `ISBN` VARCHAR(13) NOT NULL,
                        PRIMARY KEY (`pubid`))"""
    cursor.execute(sql)
    database.commit()
    # Create permission table
    sql = """CREATE TABLE IF NOT EXISTS `permission`(
                        `permid` INT NOT NULL,
                        `pubid` INT NOT NULL,
                        PRIMARY KEY (`permid`),
                        FOREIGN KEY (`pubid`) REFERENCES publisher(`pubid`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()
    # Create writer table
    sql = """CREATE TABLE IF NOT EXISTS `writer`(
                        `wid` INT NOT NULL,
                        `uid` INT NOT NULL,
                        `num_books` INT NOT NULL,
                        `banid` INT,
                        `permid` INT,
                        PRIMARY KEY (`wid`),
                        FOREIGN KEY (`uid`) REFERENCES user(`uid`) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (`banid`) REFERENCES ban(`banid`) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (`permid`) REFERENCES permission(`permid`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()
    # Create customer table
    sql = """CREATE TABLE IF NOT EXISTS `customer`(
                        `cid` INT NOT NULL,
                        `User_uid` INT NOT NULL,
                        PRIMARY KEY (`cid`),
                        FOREIGN KEY (`User_uid`) REFERENCES user(`uid`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()
    # Create student table
    sql = """CREATE TABLE IF NOT EXISTS `student`(
                        `stid` INT NOT NULL,
                        `discount` INT NOT NULL DEFAULT 25,
                        `cid` INT NOT NULL,
                        PRIMARY KEY (`stid`),
                        FOREIGN KEY (`cid`) REFERENCES customer(`cid`) ON DELETE NO ACTION ON UPDATE NO ACTION)"""
    cursor.execute(sql)
    database.commit()
    # Create senior table
    sql = """CREATE TABLE IF NOT EXISTS `senior`(
                        `seid` INT NOT NULL,
                        `discount` INT NOT NULL DEFAULT 30,
                        `cid2` INT NOT NULL,
                        PRIMARY KEY (`seid`),
                        FOREIGN KEY (`cid2`) REFERENCES customer(`cid`) ON DELETE NO ACTION ON UPDATE NO ACTION)"""
    cursor.execute(sql)
    database.commit()
    # Create disabled table
    sql = """CREATE TABLE IF NOT EXISTS `disabled`(
                        `did` INT NOT NULL,
                        `discount` INT NOT NULL DEFAULT 35,
                        `cid3` INT NOT NULL,
                        PRIMARY KEY (`did`),
                        FOREIGN KEY (`cid3`) REFERENCES customer(`cid`) ON DELETE NO ACTION ON UPDATE NO ACTION)"""
    cursor.execute(sql)
    database.commit()
    # Create veteran table
    sql = """CREATE TABLE IF NOT EXISTS `veteran`(
                        `vid` INT NOT NULL,
                        `discount` INT NOT NULL DEFAULT 25,
                        `cid4` INT NOT NULL,
                        PRIMARY KEY (`vid`),
                        FOREIGN KEY (`cid4`) REFERENCES customer(`cid`) ON DELETE NO ACTION ON UPDATE NO ACTION)"""
    cursor.execute(sql)
    database.commit()
    # Create table pay
    sql = """CREATE TABLE IF NOT EXISTS `pay`(
                        `payid` INT NOT NULL,
                        `stid1` INT,
                        `seid1` INT,
                        `did1` INT,
                        `vid1` INT,
                        `wid` INT,
                        PRIMARY KEY (`payid`),
                        FOREIGN KEY (`stid1`) REFERENCES student(`stid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
                        FOREIGN KEY (`seid1`) REFERENCES senior(`seid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
                        FOREIGN KEY (`did1`) REFERENCES disabled(`did`) ON DELETE NO ACTION ON UPDATE NO ACTION,
                        FOREIGN KEY (`vid1`) REFERENCES veteran(`vid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
                        FOREIGN KEY (`wid`) REFERENCES writer(`wid`) ON DELETE NO ACTION ON UPDATE NO ACTION)"""
    cursor.execute(sql)
    database.commit()
    # Create rent table
    sql = """CREATE TABLE IF NOT EXISTS `rent`(
                        `rid` INT NOT NULL AUTO_INCREMENT,
                        `ISBN` VARCHAR(13) NOT NULL,
                        `seid2` INT,
                        `did2` INT,
                        `vid2` INT,
                        `Wrtier2_wid` INT,
                        `stid2` INT,    
                        PRIMARY KEY (`rid`),
                        FOREIGN KEY (`seid2`) REFERENCES senior(`seid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
                        FOREIGN KEY (`did2`) REFERENCES disabled(`did`) ON DELETE NO ACTION ON UPDATE NO ACTION,
                        FOREIGN KEY (`vid2`) REFERENCES veteran(`vid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
                        FOREIGN KEY (`stid2`) REFERENCES student(`stid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
                        FOREIGN KEY (`Wrtier2_wid`) REFERENCES writer(`wid`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()
    # Create ebook table
    sql = """CREATE TABLE IF NOT EXISTS `ebook`(
                        `eBookid` INT NOT NULL,
                        `ISBN` VARCHAR(13) NOT NULL,
                        `title` VARCHAR(45) NOT NULL,
                        `cat` VARCHAR(45) NOT NULL,
                        `authors` VARCHAR(45) NOT NULL,
                        `publisher` VARCHAR(45) NOT NULL,
                        `price` FLOAT NOT NULL,
                        PRIMARY KEY (`ISBN`, `eBookid`))"""
    cursor.execute(sql)
    database.commit()
    # Create book table
    sql = """CREATE TABLE IF NOT EXISTS `book`(
                        `bookid` INT NOT NULL,
                        `ISBN` VARCHAR(13) NOT NULL,
                        `title` VARCHAR(45) NOT NULL,
                        `cat` VARCHAR(45) NOT NULL,
                        `authors` VARCHAR(45) NOT NULL,
                        `publisher` VARCHAR(45) NOT NULL,
                        `price` FLOAT NOT NULL,
                        PRIMARY KEY (`ISBN`, `bookid`))"""
    cursor.execute(sql)
    database.commit()
    # Create audio table
    sql = """CREATE TABLE IF NOT EXISTS `audio`(
                        `audid` INT NOT NULL,
                        `ISBN` VARCHAR(13) NOT NULL,
                        `title` VARCHAR(45) NOT NULL,
                        `cat` VARCHAR(45) NOT NULL,
                        `authors` VARCHAR(45) NOT NULL,
                        `publisher` VARCHAR(45) NOT NULL,
                        `duration` INT NOT NULL,
                        `price` FLOAT NOT NULL,
                        PRIMARY KEY (`ISBN`, `audid`))"""
    cursor.execute(sql)
    database.commit()
    # Create upload table
    sql = """CREATE TABLE IF NOT EXISTS `upload`(
                        `upid` INT NOT NULL AUTO_INCREMENT,
                        `ISBN` VARCHAR(13),
                        `wid1` INT NOT NULL,
                        PRIMARY KEY (`upid`),
                        FOREIGN KEY (`wid1`) REFERENCES writer(`wid`) ON DELETE NO ACTION ON UPDATE NO ACTION)"""
    cursor.execute(sql)
    database.commit()
    # Create final_order table
    sql = """CREATE TABLE IF NOT EXISTS `final_order`(
                        `oid` INT NOT NULL AUTO_INCREMENT,
                        `quantity` INT,
                        `eBook1_ISBN` VARCHAR(13),
                        `Book1_ISBN` VARCHAR(13),
                        `Audio1_ISBN` VARCHAR(13),
                        PRIMARY KEY (`oid`),
                        FOREIGN KEY (`eBook1_ISBN`) REFERENCES ebook(`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (`Book1_ISBN`) REFERENCES book(`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (`Audio1_ISBN`) REFERENCES audio(`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()
    # Create table invoice
    sql = """CREATE TABLE IF NOT EXISTS `invoice`(
                        `iid` INT NOT NULL AUTO_INCREMENT,
                        `date` DATE NOT NULL,
                        `total` FLOAT NOT NULL,
                        `oid` INT NOT NULL,
                        `payid` INT NOT NULL,
                        PRIMARY KEY (`iid`),
                        FOREIGN KEY (`oid`) REFERENCES final_order(`oid`) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (`payid`) REFERENCES pay(`payid`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()
    # Create shelf table
    sql = """CREATE TABLE IF NOT EXISTS `shelf`(
                        `shid` INT NOT NULL AUTO_INCREMENT,
                        `ISBN` VARCHAR(13) NOT NULL,
                        `category` VARCHAR(20),
                        PRIMARY KEY (`shid`))"""
    cursor.execute(sql)
    database.commit()
    # Create shelf_has_ebook table
    sql = """CREATE TABLE IF NOT EXISTS `shelf_has_ebook`(
                        `Shelf1_shid` INT NOT NULL,
                        `eBook_ISBN` VARCHAR(13) NOT NULL,
                        PRIMARY KEY (`Shelf1_shid`, `eBook_ISBN`),
                        FOREIGN KEY (`Shelf1_shid`) REFERENCES shelf(`shid`) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (`eBook_ISBN`) REFERENCES ebook(`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()
    # Create shelf_has_book table
    sql = """CREATE TABLE IF NOT EXISTS `shelf_has_book`(
                        `Shelf2_shid` INT NOT NULL,
                        `Book_ISBN` VARCHAR(13) NOT NULL,
                        PRIMARY KEY (`Shelf2_shid`, `Book_ISBN`),
                        FOREIGN KEY (`Shelf2_shid`) REFERENCES shelf(`shid`) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (`Book_ISBN`) REFERENCES book(`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()
    # Create shelf_has_audio table
    sql = """CREATE TABLE IF NOT EXISTS `shelf_has_audio`(
                        `Shelf3_shid` INT NOT NULL,
                        `Audio_ISBN` VARCHAR(13) NOT NULL,
                        PRIMARY KEY (`Shelf3_shid`, `Audio_ISBN`),
                        FOREIGN KEY (`Shelf3_shid`) REFERENCES shelf(`shid`) ON DELETE CASCADE ON UPDATE CASCADE,
                        FOREIGN KEY (`Audio_ISBN`) REFERENCES audio(`ISBN`) ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(sql)
    database.commit()


    ######################################################################################
    ######################### INSERT SAMPLE DATA #########################################
    ######################################################################################
    # Check if sample data has been inserted
    sql = "SELECT * FROM `sys` WHERE `ssid`= 1"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into sys table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `sys` (`upid`,`banid`,`oid`,`iid`) VALUES(1,33,3,7)"
            if i == 1:
                sql = "INSERT INTO `sys` (`ssid`,`banid`,`oid`,`iid`) VALUES(NULL,120,NULL,NULL)"
            if i == 2:
                sql = "INSERT INTO `sys` (`ssid`,`banid`,`oid`,`iid`) VALUES(3,NULL,NULL,NULL)"
            cursor.execute(sql)
            database.commit()
    # Check if sample data has been inserted
    sql = "SELECT * FROM `user` WHERE `uid`= 1"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into user table
    i = 0
    if result == 0:
        for i in range(0, 15):
            if i == 0:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(19,'Michael','Jones',20010122,1)"  # User 1
            if i == 1:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(47,'Rose','Smith',19730303,1)"  # User 2
            if i == 2:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(36,'Kevin','Ross',19841211,1)"  # User 3
            if i == 3:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(61,'Maria','Lopez',19591122,1)"  # User 4
            if i == 4:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(30,'Hilary','Jackson',19901202,1)"  # User 5
            if i == 5:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(88,'Mark','Ron',19320307,1)"  # User 6
            if i == 6:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(21,'Alex','Ming',19980615,1)"  # User 7
            if i == 7:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(49,'Robin','Specter',19710228,1)"  # User 8
            if i == 8:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(18,'Martha','Smith',20020121,1)"  # User 9
            if i == 9:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(77,'Julia','Adams',19430612,1)"  # User 10
            if i == 10:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(52,'Nick','Robins',19680321,1)"  # User 11
            if i == 11:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(33,'Julian','Smith',19870926,1)"  # User 12
            if i == 12:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(69,'Marcos','Sanchez',19510801,1)"  # User 13
            if i == 13:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(22,'John','Heart',19960606,1)"  # User 14
            if i == 14:
                sql = "INSERT INTO `user` (`age`,`name`,`last_name`,`birthdate`,`ssid`) VALUES(40,'Saul','Stevens',19801010,1)"  # User 15
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `plagiarism_team` WHERE `ptid`= 100"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into plagiarism_team table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `plagiarism_team` (`ptid`) VALUES(100)"
            if i == 1:
                sql = "INSERT INTO `plagiarism_team` (`ptid`) VALUES(400)"
            if i == 2:
                sql = "INSERT INTO `plagiarism_team` (`ptid`) VALUES(300)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `ban` WHERE `banid`= 33"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into ban table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `ban` (`banid`,`ptid`) VALUES(33,100)"
            if i == 1:
                sql = "INSERT INTO `ban` (`banid`,`ptid`) VALUES(123,510)"
            if i == 2:
                sql = "INSERT INTO `ban` (`banid`,`ptid`) VALUES(45,451)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
        sql = "SELECT * FROM `publisher` WHERE `pubid`= 236"
        result = cursor.execute(sql)
        database.commit()
        # Insert sample data into publisher table
        i = 0
        if result == 0:
            for i in range(0, 3):
                if i == 0:
                    sql = "INSERT INTO `publisher` (`pubid`,`ISBN`) VALUES(236,'1456965874325')"
                if i == 1:
                    sql = "INSERT INTO `publisher` (`pubid`,`ISBN`) VALUES(451,'7453691458732')"
                if i == 2:
                    sql = "INSERT INTO `publisher` (`pubid`,`ISBN`) VALUES(799,'6598297314657')"
                cursor.execute(sql)
                database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `permission` WHERE `permid`= 147"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into permission table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `permission` (`permid`,`pubid`) VALUES(147,236)"
            if i == 1:
                sql = "INSERT INTO `permission` (`permid`,`pubid`) VALUES(321,451)"
            if i == 2:
                sql = "INSERT INTO `permission` (`permid`,`pubid`) VALUES(52,799)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `writer` WHERE `wid`= 17"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into writer table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `writer` (`wid`,`uid`,`num_books`,`banid`,`permid`) VALUES(17,2,5,NULL,147)"
            if i == 1:
                sql = "INSERT INTO `writer` (`wid`,`uid`,`num_books`,`banid`,`permid`) VALUES(328,3,2,NULL,321)"
            if i == 2:
                sql = "INSERT INTO `writer` (`wid`,`uid`,`num_books`,`banid`,`permid`) VALUES(145,8,12,33,52)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `customer` WHERE `cid`= 17"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into customer table
    i = 0
    if result == 0:
        for i in range(0, 12):
            if i == 0:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(17,10)"
            if i == 1:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(301,1)"
            if i == 2:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(145,5)"
            if i == 3:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(101,4)"
            if i == 4:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(414,9)"
            if i == 5:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(10,15)"
            if i == 6:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(321,13)"
            if i == 7:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(211,14)"
            if i == 8:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(122,11)"
            if i == 9:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(38,6)"
            if i == 10:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(421,7)"
            if i == 11:
                sql = "INSERT INTO `customer` (`cid`,`User_uid`) VALUES(302,12)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `student` WHERE `stid`= 42"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into student table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `student` (`stid`,`cid`) VALUES(42,301)"
            if i == 1:
                sql = "INSERT INTO `student` (`stid`,`cid`) VALUES(371,414)"
            if i == 2:
                sql = "INSERT INTO `student` (`stid`,`cid`) VALUES(145,421)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `senior` WHERE `seid`= 171"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into senior table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `senior` (`seid`,`cid2`) VALUES(171,321)"
            if i == 1:
                sql = "INSERT INTO `senior` (`seid`,`cid2`) VALUES(29,38)"
            if i == 2:
                sql = "INSERT INTO `senior` (`seid`,`cid2`) VALUES(102,17)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `disabled` WHERE `did`= 307"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into disabled table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `disabled` (`did`,`cid3`) VALUES(307,211)"
            if i == 1:
                sql = "INSERT INTO `disabled` (`did`,`cid3`) VALUES(291,101)"
            if i == 2:
                sql = "INSERT INTO `disabled` (`did`,`cid3`) VALUES(127,302)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `veteran` WHERE `vid`= 402"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into veteran table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `veteran` (`vid`,`cid4`) VALUES(402,122)"
            if i == 1:
                sql = "INSERT INTO `veteran` (`vid`,`cid4`) VALUES(221,145)"
            if i == 2:
                sql = "INSERT INTO `veteran` (`vid`,`cid4`) VALUES(184,10)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `pay` WHERE `payid`= 100032"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into pay table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `pay` (`payid`,`stid1`,`seid1`,`did1`,`vid1`,`wid`) VALUES(100032,371,NULL,NULL,NULL,NULL)"
            if i == 1:
                sql = "INSERT INTO `pay` (`payid`,`stid1`,`seid1`,`did1`,`vid1`,`wid`) VALUES(200400,NULL,NULL,NULL,NULL,328)"
            if i == 2:
                sql = "INSERT INTO `pay` (`payid`,`stid1`,`seid1`,`did1`,`vid1`,`wid`) VALUES(145326,NULL,NULL,NULL,221,NULL)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `ebook` WHERE `eBookid`= 47"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into ebook table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `ebook` (`eBookid`,`ISBN`,`title`,`cat`,`authors`,`publisher`,`price`) VALUES(47,'5623149862764','The Da Vinci Code','Mystery','Dan Brown','Booket',5)"
            if i == 1:
                sql = "INSERT INTO `ebook` (`eBookid`,`ISBN`,`title`,`cat`,`authors`,`publisher`,`price`) VALUES(123,'7946132586437','Good Omens','Humor',' Neil Gaiman, Terry Pratchett','Workman Publishing Company',4.75)"
            if i == 2:
                sql = "INSERT INTO `ebook` (`eBookid`,`ISBN`,`title`,`cat`,`authors`,`publisher`,`price`) VALUES(84,'9137642853917','Hamlet','Drama','William Shakespeare','Rex Gibson',5.25)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `book` WHERE `bookid`= 74"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into book table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `book` (`bookid`,`ISBN`,`title`,`cat`,`authors`,`publisher`,`price`) VALUES(74,'6167345126349','Sherlock Holmes','Crime','Arthur Conan Doyle','George Newnes',4.30)"
            if i == 1:
                sql = "INSERT INTO `book` (`bookid`,`ISBN`,`title`,`cat`,`authors`,`publisher`,`price`) VALUES(333,'5642318975341','The Lord of The Rings','Fantasy','J.R.R. Tolkien','George Allen & Unwin',5.50)"
            if i == 2:
                sql = "INSERT INTO `book` (`bookid`,`ISBN`,`title`,`cat`,`authors`,`publisher`,`price`) VALUES(1001,'1324657983698','A Game of Thrones','Fantasy','George R.R. Martin','Bantam Spectra',3.99)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `audio` WHERE `audid`= 125"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into audio table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `audio` (`audid`,`ISBN`,`title`,`cat`,`authors`,`publisher`,`duration`,`price`) VALUES(125,'6461372581945','Lincoln in the Bardo','History','George Saunders','New York Times',120,3.50)"
            if i == 1:
                sql = "INSERT INTO `audio` (`audid`,`ISBN`,`title`,`cat`,`authors`,`publisher`,`duration`,`price`) VALUES(5653,'5432698741598','Angels in America','LGTB+','Tony Kushner','Amazon',200,4)"
            if i == 2:
                sql = "INSERT INTO `audio` (`audid`,`ISBN`,`title`,`cat`,`authors`,`publisher`,`duration`,`price`) VALUES(4126,'5684213548741','Lock In','Fiction','John Scalzi','Main Market',155,2.99)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `final_order` WHERE `oid`= 1"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into final_order table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `final_order` (`quantity`,`eBook1_ISBN`,`Book1_ISBN`,`Audio1_ISBN`) VALUES(3,'7946132586437','6167345126349','6461372581945')"
            if i == 1:
                sql = "INSERT INTO `final_order` (`quantity`,`eBook1_ISBN`,`Book1_ISBN`,`Audio1_ISBN`) VALUES(1,NULL,NULL,'5684213548741')"
            if i == 2:
                sql = "INSERT INTO `final_order` (`quantity`,`eBook1_ISBN`,`Book1_ISBN`,`Audio1_ISBN`) VALUES(2,'9137642853917',NULL,'5432698741598')"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `invoice` WHERE `iid`= 1"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into invoice table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `invoice` (`payid`,`date`,`total`,`oid`) VALUES(100032,20190312,12,1)"
            if i == 1:
                sql = "INSERT INTO `invoice` (`payid`,`date`,`total`,`oid`) VALUES(200400,20200123,17,2)"
            if i == 2:
                sql = "INSERT INTO `invoice` (`payid`,`date`,`total`,`oid`) VALUES(145326,20180626,20,3)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `upload` WHERE `upid`= 1"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into upload table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `upload` (`ISBN`,`wid1`) VALUES('6167345126349',145)"
            if i == 1:
                sql = "INSERT INTO `upload` (`ISBN`,`wid1`) VALUES('6461372581945',328)"
            if i == 2:
                sql = "INSERT INTO `upload` (`ISBN`,`wid1`) VALUES('1324657983698',17)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `rent` WHERE `rid`= 1"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into rent table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `rent` (`ISBN`,`seid2`,`did2`,`vid2`,`Wrtier2_wid`,`stid2`) VALUES('5623149862764',NULL,NULL,402,NULL,NULL)"
            if i == 1:
                sql = "INSERT INTO `rent` (`ISBN`,`seid2`,`did2`,`vid2`,`Wrtier2_wid`,`stid2`) VALUES('5684213548741',171,NULL,NULL,NULL,NULL)"
            if i == 2:
                sql = "INSERT INTO `rent` (`ISBN`,`seid2`,`did2`,`vid2`,`Wrtier2_wid`,`stid2`) VALUES('1653217896351',NULL,NULL,NULL,17,NULL)"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `shelf` WHERE `shid`= 1"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into shelf table
    i = 0
    if result == 0:
        for i in range(0, 8):
            if i == 0:
                sql = "INSERT INTO `shelf` (`ISBN`,`category`) VALUES('6167345126349','Crime')"
            if i == 1:
                sql = "INSERT INTO `shelf` (`ISBN`,`category`) VALUES('9137642853917','Drama')"
            if i == 2:
                sql = "INSERT INTO `shelf` (`ISBN`,`category`) VALUES('5684213548741','Fiction')"
            if i == 3:
                sql = "INSERT INTO `shelf` (`ISBN`,`category`) VALUES('6461372581945','History')"
            if i == 4:
                sql = "INSERT INTO `shelf` (`ISBN`,`category`) VALUES('5642318975341','Fantasy')"
            if i == 5:
                sql = "INSERT INTO `shelf` (`ISBN`,`category`) VALUES('5432698741598','LGTB+')"
            if i == 6:
                sql = "INSERT INTO `shelf` (`ISBN`,`category`) VALUES('7946132586437','Humor')"
            if i == 7:
                sql = "INSERT INTO `shelf` (`ISBN`,`category`) VALUES('5623149862764','Mystery')"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `shelf_has_ebook` WHERE `Shelf1_shid`= 8"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into shelf_has_ebook table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `shelf_has_ebook` (`Shelf1_shid`,`eBook_ISBN`) VALUES(8,'5623149862764')"
            if i == 1:
                sql = "INSERT INTO `shelf_has_ebook` (`Shelf1_shid`,`eBook_ISBN`) VALUES(7,'7946132586437')"
            if i == 2:
                sql = "INSERT INTO `shelf_has_ebook` (`Shelf1_shid`,`eBook_ISBN`) VALUES(2,'9137642853917')"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `shelf_has_book` WHERE `Shelf2_shid`= 1"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into shelf_has_book table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `shelf_has_book` (`Shelf2_shid`,`Book_ISBN`) VALUES(1,'6167345126349')"
            if i == 1:
                sql = "INSERT INTO `shelf_has_book` (`Shelf2_shid`,`Book_ISBN`) VALUES(5,'5642318975341')"
            if i == 2:
                sql = "INSERT INTO `shelf_has_book` (`Shelf2_shid`,`Book_ISBN`) VALUES(5,'1324657983698')"
            cursor.execute(sql)
            database.commit()

    # Check if sample data has been inserted
    sql = "SELECT * FROM `shelf_has_audio` WHERE `Shelf3_shid`= 4"
    result = cursor.execute(sql)
    database.commit()
    # Insert sample data into shelf_has_audio table
    i = 0
    if result == 0:
        for i in range(0, 3):
            if i == 0:
                sql = "INSERT INTO `shelf_has_audio` (`Shelf3_shid`,`Audio_ISBN`) VALUES(4,'6461372581945')"
            if i == 1:
                sql = "INSERT INTO `shelf_has_audio` (`Shelf3_shid`,`Audio_ISBN`) VALUES(6,'5432698741598')"
            if i == 2:
                sql = "INSERT INTO `shelf_has_audio` (`Shelf3_shid`,`Audio_ISBN`) VALUES(3,'5684213548741')"
            cursor.execute(sql)
            database.commit()


########################################################################################
######################### CREATE ACCOUNT SECTION #######################################
########################################################################################


def create_account():
    print("*** Create Account Site ***")

    # Introducing First Name
    print("Introduce your First Name: ")
    first_name = input()
    first_name = first_name.replace(" ", "")
    not_number = False
    valid_first_name = False
    while not valid_first_name:
        # Check if First Name is long enough
        if len(first_name) <= 1:
            print("First Name is too short. Introduce your First Name again: ")
            first_name = input()
            first_name = first_name.replace(" ", "")
        # Check if First Name contains any number
        elif not not_number:
            for k in first_name:
                if k.isdigit():
                    not_number = False
                    print("First Name can't contain numbers. Introduce your First Name again: ")
                    first_name = input()
                    first_name = first_name.replace(" ", "")
                    break
                else:
                    not_number = True
        else:
            valid_first_name = True

    # Introducing Last Name
    print("Introduce your Last Name: ")
    last_name = input()
    last_name = last_name.replace(" ", "")
    not_number = False
    valid_last_name = False
    while not valid_last_name:
        # Check if Last Name is long enough
        if len(last_name) <= 1:
            print("Last Name is too short. Introduce your First Name again: ")
            last_name = input()
            last_name = last_name.replace(" ", "")
        # Check if Last Name contains any number
        elif not not_number:
            for k in last_name:
                if k.isdigit():
                    not_number = False
                    print("Last Name can't contain numbers. Introduce your Last Name again: ")
                    last_name = input()
                    last_name = last_name.replace(" ", "")
                    break
                else:
                    not_number = True
        else:
            valid_last_name = True

    # Introducing Age
    print("Introduce your Age: ")
    age = input()
    age = age.replace(" ", "")
    not_letter = False
    valid_age = False
    while not valid_age:
        # Check if Age is 18 or more
        try:
            if int(age) < 18:
                print("Age not valid. Minimum Age is 18. Introduce your Age again: ")
                age = input()
                age = age.replace(" ", "")
        except:
            pass
        # Check if Age contains any letter
        if not not_letter:
            for k in age:
                try:
                    if not k.isdigit():
                        not_letter = False
                        print("Age can't contain letters. Introduce your Age again: ")
                        age = input()
                        age = age.replace(" ", "")
                        break
                    else:
                        not_letter = True
                except:
                    pass
        else:
            valid_age = True

    # Introducing Birth Date
    print("Introduce your Birth Date (YYYYMMDD): ")
    birthdate = input()
    birthdate = birthdate.replace(" ", "")
    not_letter = False
    valid_birthdate = False
    valid_year = False
    valid_month = False
    valid_day = False
    while not valid_birthdate:
        # Check if Birth Date 8 characters long
        try:
            if len(birthdate) != 8:
                print("Birth Date not valid. Follow the YYYYMMDD format. Introduce your Birth Date again: ")
                birthdate = input()
                birthdate = birthdate.replace(" ", "")
        except:
            pass
        # Check if Birth Date contains any letter
        if not not_letter:
            for k in birthdate:
                try:
                    if not k.isdigit():
                        not_letter = False
                        print("Birth Date can't contain letters. Introduce your Birth Date again: ")
                        birthdate = input()
                        birthdate = birthdate.replace(" ", "")
                        break
                    else:
                        not_letter = True
                except:
                    pass
        if not valid_year:
            today = str(date.today())
            today = today.replace("-", "")
            result = str(int(today) - int(birthdate))
            result = result[:2]
            if result == age:
                valid_year = True
            else:
                print("Birth Date doesn't match with the age introduced. Introduce your Birth Date again: ")
                birthdate = input()
                birthdate = birthdate.replace(" ", "")
        if not valid_month:
            month = str(birthdate[:6])
            month = month[-2:]
            if int(month) <= 12:
                valid_month = True
            else:
                print("Month can't be higher than 12. Introduce your Birth Date again: ")
                birthdate = input()
                birthdate = birthdate.replace(" ", "")
        if not valid_day:
            day = str(birthdate[-2:])
            if int(day) <= 31:
                valid_day = True
            else:
                print("Day can't be higher than 31. Introduce your Birth Date again: ")
                birthdate = input()
                birthdate = birthdate.replace(" ", "")
        else:
            valid_birthdate = True

    # Insert the new registered user
    sql = "INSERT INTO `user` (`age`, `name`, `last_name`, `birthdate`, `ssid`) VALUES (%s, %s, %s, %s, %s)"
    values = (age, first_name, last_name, birthdate, 1)
    cursor.execute(sql, values)
    database.commit()
    print()
    print("User registered.")
    print("************************************")
    print()


########################################################################################
############################# LOGIN SECTION ############################################
########################################################################################


def login():
    valid_login = False
    while not valid_login:
        print("*** Login Site ***")
        print("Introduce your First Name: ")
        first_name = input()
        first_name = first_name.replace(" ","")
        print("Introduce your Last Name: ")
        last_name = input()
        last_name = last_name.replace(" ","")
        print("Introduce your User ID: ")
        user_id = input()
        user_id = user_id.replace(" ", "")
        sql = "SELECT * FROM `user` WHERE `name` = %s AND `last_name` = %s AND `uid`= %s"
        values = (first_name, last_name, user_id)
        result = cursor.execute(sql, values)
        database.commit()
        if result == 0:
            print("User not found. Try again")
        else:
            valid_login = True
            print("*** Welcome ", first_name, last_name, "*** Back to User Menu...")
            print()


########################################################################################
############################# SEARCH SECTION ###########################################
########################################################################################


def search():
    valid_search = False
    while not valid_search:
        print("*** Search Site ***")
        print("1. Search Book")
        print("2. Search eBook")
        print("3. Search Audio")
        print("4. Search Writer")
        print("5. Search Customer")
        print("6. Search Publisher")
        print("7. Search Shelf")
        print("8. Search Order")
        print("9. Search Invoice")
        print("10. Search Plagiarism Team")
        print("11. Search Ban")
        print("Introduce a number to select an option:")
        item = input()
        item = item.replace(" ", "")
        if item not in check_search:
            print("Input not valid. Try again.")
        else:
            valid_search = True

    if item == "1":
        search_book()
    if item == "2":
        search_ebook()
    if item == "3":
        search_audio()
    if item == "4":
        search_writer()
    if item == "5":
        search_customer()
    if item == "6":
        search_publisher()
    if item == "7":
        search_shelf()
    if item == "8":
        search_order()
    if item == "9":
        search_invoice()
    if item == "10":
        search_plag_team()
    if item == "11":
        search_ban()


def search_book():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_book = False
        while not valid_search_book:
            print("Introduce ISBN: ")
            isbn = input()
            isbn = isbn.replace(" ", "")
            sql = "SELECT * FROM `book` WHERE ISBN = %s"
            value = (isbn)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The ISBN does not exist in the database. Try again.")
            else:
                valid_search_book = True
        for row in cursor.fetchall():
            print("Book ID: ", row[0])
            print("ISBN: ", row[1])
            print("Title: ", row[2])
            print("Category: ", row[3])
            print("Author: ", row[4])
            print("Publisher: ", row[5])
            print("Price: $", row[6])


def search_ebook():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_ebook = False
        while not valid_search_ebook:
            print("Introduce ISBN: ")
            isbn = input()
            isbn = isbn.replace(" ", "")
            sql = "SELECT * FROM `ebook` WHERE ISBN = %s"
            value = (isbn)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The ISBN does not exist in the database. Try again.")
            else:
                valid_search_ebook = True
        for row in cursor.fetchall():
            print("eBook ID: ", row[0])
            print("ISBN: ", row[1])
            print("Title: ", row[2])
            print("Category: ", row[3])
            print("Author: ", row[4])
            print("Publisher: ", row[5])
            print("Price: $", row[6])


def search_audio():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_audio = False
        while not valid_search_audio:
            print("Introduce ISBN: ")
            isbn = input()
            isbn = isbn.replace(" ", "")
            sql = "SELECT * FROM `audio` WHERE ISBN = %s"
            value = (isbn)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The ISBN does not exist in the database. Try again.")
            else:
                valid_search_audio = True
        for row in cursor.fetchall():
            print("Audio ID: ", row[0])
            print("ISBN: ", row[1])
            print("Title: ", row[2])
            print("Category: ", row[3])
            print("Author: ", row[4])
            print("Publisher: ", row[5])
            print("Duration: ", row[6], "sec")
            print("Price: $", row[7])


def search_writer():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_writer = False
        while not valid_search_writer:
            print("Introduce Writer ID: ")
            writer = input()
            writer = writer.replace(" ", "")
            sql = "SELECT * FROM `writer` WHERE wid = %s"
            value = (writer)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The Writer ID does not exist in the database. Try again.")
            else:
                valid_search_writer = True
        for row in cursor.fetchall():
            print("Writer ID: ", row[0])
            print("User ID: ", row[1])
            print("Number of Books: ", row[2])
            print("Ban ID: ", row[3])
            print("Permission ID: ", row[4])


def search_customer():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_customer = False
        while not valid_search_customer:
            print("Introduce Customer ID: ")
            customer = input()
            customer = customer.replace(" ", "")
            sql = "SELECT * FROM `customer` WHERE cid = %s"
            value = (customer)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The Writer ID does not exist in the database. Try again.")
            else:
                valid_search_customer = True
        for row in cursor.fetchall():
            print("Customer ID: ", row[0])
            print("User ID: ", row[1])


def search_publisher():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_publisher = False
        while not valid_search_publisher:
            print("Introduce Publisher ID: ")
            publisher = input()
            publisher = publisher.replace(" ", "")
            sql = "SELECT * FROM `publisher` WHERE pubid = %s"
            value = (publisher)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The Publisher ID does not exist in the database. Try again.")
            else:
                valid_search_publisher = True
        for row in cursor.fetchall():
            print("Publisher ID: ", row[0])
            print("ISBN: ", row[1])


def search_shelf():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_shelf = False
        while not valid_search_shelf:
            print("Introduce a Category: ")
            shelf = input()
            shelf = shelf.replace(" ", "")
            sql = "SELECT * FROM `shelf` WHERE category = %s"
            value = (shelf)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The category does not exist in the database. Try again.")
            else:
                valid_search_shelf = True
        for row in cursor.fetchall():
            print("Shelf ID: ", row[0])
            print("ISBN: ", row[1])
            print("Category: ", row[2])


def search_order():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_order = False
        while not valid_search_order:
            print("Introduce Order ID: ")
            order = input()
            order = order.replace(" ", "")
            sql = "SELECT * FROM `final_order` WHERE oid = %s"
            value = (order)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The Order ID does not exist in the database. Try again.")
            else:
                valid_search_order = True
        for row in cursor.fetchall():
            print("Order ID: ", int(row[0]))
            print("Quantity: ", int(row[1]))
            print("ISBNs: Book:", row[2], "; eBook:", row[3], "; Audio:", row[4])


def search_invoice():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_invoice = False
        while not valid_search_invoice:
            print("Introduce Invoice ID: ")
            invoice = input()
            invoice = invoice.replace(" ", "")
            sql = "SELECT * FROM `invoice` WHERE iid = %s"
            value = (invoice)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The Invoice ID does not exist in the database. Try again.")
            else:
                valid_search_invoice = True
        for row in cursor.fetchall():
            print("Invoice ID: ", row[0])
            print("Date: ", row[1])
            print("Order ID: ", int(row[2]))
            print("Payment ID: ", row[3])


def search_plag_team():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_plag_team = False
        while not valid_search_plag_team:
            print("Introduce a Plagiarism Team ID: ")
            plag_team = input()
            plag_team = plag_team.replace(" ", "")
            sql = "SELECT * FROM `plagiarism_team` WHERE ptid = %s"
            value = (plag_team)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The Plagiarism Team ID does not exist in the database. Try again.")
            else:
                valid_search_plag_team = True
        for row in cursor.fetchall():
            print("Plagiarism Team ID: ", row[0])


def search_ban():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valid_search_ban = False
        while not valid_search_ban:
            print("Introduce a Ban ID: ")
            ban = input()
            ban = ban.replace(" ", "")
            sql = "SELECT * FROM `ban` WHERE banid = %s"
            value = (ban)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("The Ban ID does not exist in the database. Try again.")
            else:
                valid_search_ban = True
        for row in cursor.fetchall():
            print("Ban ID: ", row[0])
            print("Plagiarism Team ID: ", row[1])


def insert():
    valid_insert = False
    while not valid_insert:
        print("*** Insert Site ***")
        print("1. Insert Book")
        print("2. Insert eBook")
        print("3. Insert Audio")
        print("4. Introduce Order")
        print("5. Insert Invoice")
        print("6. Insert Permission")
        print("7. Insert Ban")
        print("Introduce a number to select an option: ")
        item_insert = input()
        if item_insert not in check_insert:
            print("Input not valid. Try again.")
        else:
            valid_insert = True
    if item_insert == "1":
        insert_book()
    if item_insert == "2":
        insert_ebook()
    if item_insert == "3":
        insert_audio()
    if item_insert == "4":
        insert_order()
    if item_insert == "5":
        insert_invoice()
    if item_insert == "6":
        insert_permission()
    if item_insert == "7":
        insert_ban()


def insert_book():
    print("Add the next fields to complete the insertion:")
    valid_id = False
    while not valid_id:
        print("Add Book ID: ")
        book_id = input()
        if book_id.isdigit() == False:
            print("Book ID has to be a number. Try again.")
        else:
            valid_id = True
    valid_isbn = False
    while not valid_isbn:
        print("Add ISBN: ")
        book_isbn = input()
        if len(book_isbn) != 13:
            print("ISBN has to be 13 characters long. Try again")
        elif book_isbn.isdigit() == False:
            print("ISBN has to be a number. Try again.")
        else:
            valid_isbn = True
    print("Add Title: ")
    book_title = input()
    print("Add Category: ")
    book_category = input()
    print("Add Author: ")
    book_author = input()
    print("Add Publisher: ")
    book_publisher = input()
    valid_price = False
    while not valid_price:
        print("Add price: ")
        book_price = float(input())
        book_price = "{:.2f}".format(book_price)
        if type(float(book_price)) not in (int, float):
            print("Input not valid. Try again.")
        else:
            valid_price = True
    sql = "INSERT INTO `book` VALUES (%s,%s,%s,%s,%s,%s,%s)"
    value = (book_id, book_isbn, book_title, book_category, book_author, book_publisher, book_price)
    cursor.execute(sql, value)
    database.commit()
    print()
    sql = "SELECT * FROM `book` WHERE `bookid` = %s"
    value = book_id
    cursor.execute(sql, value)
    for row in cursor.fetchall():
        print("Book ID: ", row[0])
        print("ISBN: ", row[1])
        print("Title: ", row[2])
        print("Category: ", row[3])
        print("Author: ", row[4])
        print("Publisher: ", row[5])
        print("Price: $", row[6])
    database.commit()
    print()
    print("Book inserted into the database.")
    print("************************************")
    print()


def insert_ebook():
    print("Add the next fields to complete the insertion:")
    valid_id = False
    while not valid_id:
        print("Add eBook ID: ")
        ebook_id = input()
        if ebook_id.isdigit() == False:
            print("eBook ID has to be a number. Try again.")
        else:
            valid_id = True
    valid_isbn = False
    while not valid_isbn:
        print("Add ISBN: ")
        ebook_isbn = input()
        if len(ebook_isbn) != 13:
            print("ISBN has to be 13 characters long. Try again")
        elif ebook_isbn.isdigit() == False:
            print("ISBN has to be a number. Try again.")
        else:
            valid_isbn = True
    print("Add Title: ")
    ebook_title = input()
    print("Add Category: ")
    ebook_category = input()
    print("Add Author: ")
    ebook_author = input()
    print("Add Publisher: ")
    ebook_publisher = input()
    valid_price = False
    while not valid_price:
        print("Add price: ")
        ebook_price = float(input())
        ebook_price = "{:.2f}".format(ebook_price)
        if type(float(ebook_price)) not in (int, float):
            print("Input not valid. Try again.")
        else:
            valid_price = True
    sql = "INSERT INTO `ebook` VALUES (%s,%s,%s,%s,%s,%s,%s)"
    value = (ebook_id, ebook_isbn, ebook_title, ebook_category, ebook_author, ebook_publisher, ebook_price)
    cursor.execute(sql, value)
    database.commit()
    print()
    sql = "SELECT * FROM `ebook` WHERE `ebookid` = %s"
    value = ebook_id
    cursor.execute(sql, value)
    for row in cursor.fetchall():
        print("Book ID: ", row[0])
        print("ISBN: ", row[1])
        print("Title: ", row[2])
        print("Category: ", row[3])
        print("Author: ", row[4])
        print("Publisher: ", row[5])
        print("Price: $", row[6])
    database.commit()
    print()
    print("eBook inserted into the database.")
    print("************************************")
    print()


def insert_audio():
    print("Add the next fields to complete the insertion:")
    valid_id = False
    while not valid_id:
        print("Add Audio ID: ")
        audio_id = input()
        if audio_id.isdigit() == False:
            print("Audio ID has to be a number. Try again.")
        else:
            valid_id = True
    valid_isbn = False
    while not valid_isbn:
        print("Add ISBN: ")
        audio_isbn = input()
        if len(audio_isbn) != 13:
            print("ISBN has to be 13 characters long. Try again")
        elif audio_isbn.isdigit() == False:
            print("ISBN has to be a number. Try again.")
        else:
            valid_isbn = True
    print("Add Title: ")
    audio_title = input()
    print("Add Category: ")
    audio_category = input()
    print("Add Author: ")
    audio_author = input()
    print("Add Publisher: ")
    audio_publisher = input()
    valid_duration = False
    while not valid_duration:
        print("Add duration (in seconds): ")
        audio_duration = float(input())
        audio_duration = "{:.2f}".format(audio_duration)
        if type(float(audio_duration)) not in (int, float):
            print("Input not valid. Try again.")
        else:
            valid_duration = True
    valid_price = False
    while not valid_price:
        print("Add price: ")
        audio_price = float(input())
        audio_price = "{:.2f}".format(audio_price)
        if type(float(audio_price)) not in (int, float):
            print("Input not valid. Try again.")
        else:
            valid_price = True
    sql = "INSERT INTO `audio` VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    value = (
    audio_id, audio_isbn, audio_title, audio_category, audio_author, audio_publisher, audio_duration, audio_price)
    cursor.execute(sql, value)
    database.commit()
    print()
    sql = "SELECT * FROM `audio` WHERE `audid` = %s"
    value = audio_id
    cursor.execute(sql, value)
    for row in cursor.fetchall():
        print("Book ID: ", row[0])
        print("ISBN: ", row[1])
        print("Title: ", row[2])
        print("Category: ", row[3])
        print("Author: ", row[4])
        print("Duration: ", row[5], "sec")
        print("Publisher: ", row[6])
        print("Price: $", row[7])
    database.commit()
    print()
    print("Audio inserted into the database.")
    print("************************************")
    print()


def insert_order():
    sum = 0
    print("Add the next fields to complete the insertion:")
    valid_option = False
    while not valid_option:
        print("Do you want to add a book? (Yes/No)")
        book_option = input()
        if book_option != "Yes" and book_option != "No":
            print("Input not valid. Try again")
        else:
            valid_option = True
    if book_option == "Yes":
        valid_book_isbn = False
        while not valid_book_isbn:
            print("Add the ISBN of the book you want to order: ")
            book_isbn = input()
            sql = "SELECT * FROM book WHERE `ISBN` = %s"
            value = (book_isbn)
            result = cursor.execute(sql, value)
            database.commit()
            if len(book_isbn) != 13:
                print("ISBN has to be 13 characters long. Try again")
            elif book_isbn.isdigit() == False:
                print("ISBN has to be a number. Try again.")
            elif result == 0:
                print("ISBN not found. Try again.")
            else:
                valid_book_isbn = True
                sum = sum + 1
    valid_option = False
    while not valid_option:
        print("Do you want to add a eBook? (Yes/No)")
        ebook_option = input()
        if ebook_option != "Yes" and ebook_option != "No":
            print("Input not valid. Try again")
        else:
            valid_option = True
    if ebook_option == "Yes":
        valid_ebook_isbn = False
        while not valid_ebook_isbn:
            print("Add the ISBN of the eBook you want to order: ")
            ebook_isbn = input()
            sql = "SELECT * FROM ebook WHERE `ISBN` = %s"
            value = (ebook_isbn)
            result = cursor.execute(sql, value)
            database.commit()
            if len(ebook_isbn)  !=13:
                print("ISBN has to be 13 characters long. Try again")
            elif ebook_isbn.isdigit() == False:
                print("ISBN has to be a number. Try again.")
            elif result == 0:
                print("ISBN not found. Try again.")
            else:
                valid_ebook_isbn = True
                sum = sum + 1
    valid_option = False
    while not valid_option:
        print("Do you want to add a Audio? (Yes/No)")
        audio_option = input()
        if audio_option != "Yes" and audio_option != "No":
            print("Input not valid. Try again")
        else:
            valid_option = True
    if audio_option == "Yes":
        valid_audio_isbn = False
        while not valid_audio_isbn:
            print("Add the ISBN of the audio you want to order: ")
            audio_isbn = input()
            if str(audio_isbn) == "None":
                valid_audio_isbn = True
                audio_isbn = "NULL"
                break
            sql = "SELECT * FROM audio WHERE `ISBN` = %s"
            value = (audio_isbn)
            result = cursor.execute(sql, value)
            database.commit()
            if len(audio_isbn) != 13:
                print("ISBN has to be 13 characters long. Try again")
            elif audio_isbn.isdigit() == False:
                print("ISBN has to be a number. Try again.")
            elif result == 0:
                print("ISBN not found. Try again.")
            else:
                valid_audio_isbn = True
                sum = sum + 1
    # Only book ordered
    if book_option == "Yes" and ebook_option == "No" and audio_option == "No":
        sql = "INSERT INTO `final_order`(`quantity`,`Book1_ISBN`) VALUES (%s, %s)"
        value = (str(sum), book_isbn)
        cursor.execute(sql, value)
        database.commit()
    # Only ebook ordered
    if book_option == "No" and ebook_option == "Yes" and audio_option == "No":
        sql = "INSERT INTO `final_order`(`quantity`,`eBook1_ISBN`) VALUES (%s, %s)"
        value = (str(sum), ebook_isbn)
        cursor.execute(sql, value)
        database.commit()
    # Only audio ordered
    if book_option == "No" and ebook_option == "No" and audio_option == "Yes":
        sql = "INSERT INTO `final_order`(`quantity`,`Audio1_ISBN`) VALUES (%s, %s)"
        value = (str(sum), audio_isbn)
        cursor.execute(sql, value)
        database.commit()
    # Book and eBook ordered
    if book_option == "Yes" and ebook_option == "Yes" and audio_option == "No":
        sql = "INSERT INTO `final_order`(`quantity`,`Book1_ISBN`,`eBook1_ISBN`) VALUES (%s, %s, %s)"
        value = (str(sum), book_isbn, ebook_isbn)
        cursor.execute(sql, value)
        database.commit()
    # Book and Audio ordered
    if book_option == "Yes" and ebook_option == "No" and audio_option == "Yes":
        sql = "INSERT INTO `final_order`(`quantity`,`Book1_ISBN`,`Audio1_ISBN`) VALUES (%s, %s, %s)"
        value = (str(sum), book_isbn, audio_isbn)
        cursor.execute(sql, value)
        database.commit()
    # eBook and Audio ordered
    if book_option == "No" and ebook_option == "Yes" and audio_option == "Yes":
        sql = "INSERT INTO `final_order`(`quantity`,`eBook1_ISBN`,`Audio1_ISBN`) VALUES (%s, %s, %s)"
        value = (str(sum), ebook_isbn, audio_isbn)
        cursor.execute(sql, value)
        database.commit()
    # Book, eBook and Audio ordered
    if book_option == "Yes" and ebook_option == "Yes" and audio_option == "Yes":
        sql = "INSERT INTO `final_order`(`quantity`,`Book1_ISBN`,`eBook1_ISBN`,`Audio1_ISBN`) VALUES (%s, %s, %s, %s)"
        value = (str(sum), book_isbn, ebook_isbn, audio_isbn)
        cursor.execute(sql, value)
        database.commit()
    print()
    print("Order inserted into the database.")
    print("************************************")
    print()


def insert_invoice():
    print("Add the next fields to complete the insertion:")
    valid_oid = False
    while not valid_oid:
        print("Add Order ID: ")
        order_id = input()
        # Check if the order exists in the database
        sql = "SELECT * FROM `final_order` WHERE `oid` = %s"
        value = (order_id)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("Order not found in the database. Try again.")
        else:
            valid_oid = True
    valid_pay = False
    while not valid_pay:
        print("Add Payment ID: ")
        pay_id = input()
        # Check if the payment exists in the database
        sql = "SELECT * FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("Payment ID not found in the database. Try again.")
        else:
            valid_pay = True

    # Get Book ISBN
    final_book_price = 0
    sql = "SELECT `Book1_ISBN` FROM `final_order` WHERE `oid` = %s"
    value = (order_id)
    cursor.execute(sql, value)
    database.commit()
    book_isbn = cursor.fetchall()
    book_isbn = [i for sub in book_isbn for i in sub]
    book_isbn = book_isbn[0]
    if str(book_isbn) != "None":
        # Get Book Price
        sql = "SELECT `price` FROM `book` WHERE `ISBN` = %s"
        value = (str(book_isbn))
        cursor.execute(sql, value)
        database.commit()
        book_price = cursor.fetchall()
        book_price = [i for sub in book_price for i in sub]
        book_price = book_price[0]

        # Check if User is Student and calculate book price with discount (25%)
        sql = "SELECT `stid1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        database.commit()
        if str(result) != "None":
            book_price = book_price * 0.75

        # Check if User is Senior and calculate book price with discount (30%)
        sql = "SELECT `seid1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        if str(result) != "None":
            book_price = book_price * 0.70

        # Check if User is Disabled and calculate book price with discount (35%)
        sql = "SELECT `did1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        if str(result) != "None":
            book_price = book_price * 0.65

        # Check if User is Veteran and calculate book price with discount (40%)
        sql = "SELECT `vid1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        if str(result) != "None":
            book_price = book_price * 0.65
        # Get Book final price
        final_book_price = book_price

    # Get eBook ISBN
    final_ebook_price = 0
    sql = "SELECT `eBook1_ISBN` FROM `final_order` WHERE `oid` = %s"
    value = (order_id)
    cursor.execute(sql, value)
    database.commit()
    ebook_isbn = cursor.fetchall()
    ebook_isbn = [i for sub in ebook_isbn for i in sub]
    ebook_isbn = ebook_isbn[0]
    if str(ebook_isbn) != "None":
        # Get eBook Price
        sql = "SELECT `price` FROM `ebook` WHERE `ISBN` = %s"
        value = (str(ebook_isbn))
        cursor.execute(sql, value)
        database.commit()
        ebook_price = cursor.fetchall()
        ebook_price = [i for sub in ebook_price for i in sub]
        ebook_price = ebook_price[0]
        print(ebook_price)

        # Check if User is Student and calculate eBook price with discount (25%)
        sql = "SELECT `stid1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        database.commit()
        if str(result) != "None":
            ebook_price = ebook_price * 0.75

        # Check if User is Senior and calculate eBook price with discount (30%)
        sql = "SELECT `seid1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        if str(result) != "None":
            ebook_price = ebook_price * 0.70

        # Check if User is Disabled and calculate eBook price with discount (35%)
        sql = "SELECT `did1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        if str(result) != "None":
            ebook_price = ebook_price * 0.65

        # Check if User is Veteran and calculate eBook price with discount (40%)
        sql = "SELECT `vid1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        if str(result) != "None":
            ebook_price = ebook_price * 0.65
        final_ebook_price = ebook_price


    # Get Audio ISBN
    final_audio_price = 0
    sql = "SELECT `Audio1_ISBN` FROM `final_order` WHERE `oid` = %s"
    value = (order_id)
    cursor.execute(sql, value)
    database.commit()
    audio_isbn = cursor.fetchall()
    audio_isbn = [i for sub in audio_isbn for i in sub]
    audio_isbn = audio_isbn[0]
    if str(audio_isbn) != "None":
        # Get Audio Price
        sql = "SELECT `price` FROM `audio` WHERE `ISBN` = %s"
        value = (str(audio_isbn))
        cursor.execute(sql, value)
        database.commit()
        audio_price = cursor.fetchall()
        audio_price = [i for sub in audio_price for i in sub]
        audio_price = audio_price[0]

        # Check if User is Student and calculate audio price with discount (25%)
        sql = "SELECT `stid1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        database.commit()
        if str(result) != "None":
            audio_price = audio_price * 0.75

        # Check if User is Senior and calculate audio price with discount (30%)
        sql = "SELECT `seid1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        if str(result) != "None":
            audio_price = audio_price * 0.70

        # Check if User is Disabled and calculate audio price with discount (35%)
        sql = "SELECT `did1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        if str(result) != "None":
            audio_price = audio_price * 0.65

        # Check if User is Veteran and calculate audio price with discount (40%)
        sql = "SELECT `vid1` FROM `pay` WHERE `payid` = %s"
        value = (pay_id)
        cursor.execute(sql, value)
        result = cursor.fetchall()
        result = [i for sub in result for i in sub]
        result = result[0]
        if str(result) != "None":
            audio_price = audio_price * 0.65
        final_audio_price = audio_price

    # Get invoice total Price
    invoice_price = final_book_price + final_ebook_price + final_audio_price
    invoice_price = "{:.2f}".format(invoice_price)

    # Get invoice Date
    invoice_date = date.today()

    # Insert invoice
    sql = "INSERT INTO `invoice` (`date`,`total`,`oid`,`payid`)VALUES (%s,%s,%s,%s)"
    value = (str(invoice_date), str(invoice_price), order_id, pay_id)
    cursor.execute(sql, value)
    database.commit()
    print()
    print("Invoice inserted into the database.")
    print("************************************")
    print()


def insert_permission():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        print("Add the next fields to complete the insertion:")
        valid_publisher_id = False
        while not valid_publisher_id:
            print("Add your Publisher ID")
            pub_id = input()
            sql = "SELECT * FROM `publisher` WHERE `pubid` = %s"
            value = (pub_id)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("Publisher ID not found in the database. Try again")
            else:
                valid_publisher_id = True
        valid_permission_id = False
        while not valid_permission_id:
            print("Add Permission ID: ")
            perm_id = input()
            sql = "SELECT * FROM `permission` WHERE `permid` = %s"
            value = (perm_id)
            result = cursor.execute(sql, value)
            database.commit()
            if not perm_id.isdigit():
                print("Permission ID has to be a number. Try again.")
            elif result == 1:
                print("Permission ID already exists. Try again")
            else:
                valid_permission_id = True
        # Insert Permission in the database
        sql = "INSERT INTO `permission` VALUES (%s,%s)"
        value = (perm_id, pub_id)
        cursor.execute(sql, value)
        database.commit()
        print()
        print("Permission inserted into the database.")
        print("************************************")
        print()


def insert_ban():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        print("Add the next fields to complete the insertion:")
        valid_plag_team_id = False
        while not valid_plag_team_id:
            print("Add your Plagirism Team ID: ")
            pt_id = input()
            sql = "SELECT * FROM `plagiarism_team` WHERE `ptid` = %s"
            value = (pt_id)
            result = cursor.execute(sql, value)
            database.commit()
            if result == 0:
                print("Plagirism Team ID not found in the database. Try again. ")
            else:
                valid_plag_team_id = True
        valid_ban_id = False
        while not valid_ban_id:
            print("Add Ban ID: ")
            ban_id = input()
            sql = "SELECT * FROM `ban` WHERE `banid` = %s"
            value = (ban_id)
            result = cursor.execute(sql, value)
            database.commit()
            if not ban_id.isdigit():
                print("Ban ID has to be a number. Try again.")
            elif result == 1:
                print("Ban ID already exists. Try again.")
            else:
                valid_ban_id = True
        # Insert Permission in the database
        sql = "INSERT INTO `ban` VALUES (%s,%s)"
        value = (ban_id, pt_id)
        cursor.execute(sql, value)
        database.commit()
        print()
        print("Ban inserted into the database.")
        print("************************************")
        print()


########################################################################################
############################# UPDATE SECTION ###########################################
########################################################################################


def update():
    valid_update = False
    while not valid_update:
        print("*** Update Site ***")
        print("1. Update Book")
        print("2. Update eBook")
        print("3. Update Audio")
        print("Introduce a number to select an option: ")
        item_update = input()
        if item_update not in check_update:
            print("Input not valid. Try again.")
        else:
            valid_update = True
    if item_update == "1":
        update_book()
    if item_update == "2":
        update_ebook()
    if item_update == "3":
        update_audio()


def update_book():
    valid_book_update = False
    while not valid_book_update:
        # Introducing the ISBN of the item to be updated
        print("Introduce the ISBN to update: ")
        book_update = input()
        sql = "SELECT * FROM `book` WHERE ISBN = %s"
        value = (book_update)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("The ISBN does not exist in the database. Try again.")
        else:
            valid_book_update = True
    # Show the user the Book to edit
    print("Selected Book:")
    for row in cursor.fetchall():
        print("Book ID: ", row[0])
        print("ISBN: ", row[1])
        print("Title: ", row[2])
        print("Category: ", row[3])
        print("Author: ", row[4])
        print("Publisher: ", row[5])
        print("Price: $", row[6])
    print()
    print("************************************")
    print()
    valid_book_update_options = False
    while not valid_book_update_options:
        print("1. Update Author")
        print("2. Update Publisher")
        print("3. Update Category")
        print("4. Update Price")
        book_result = input()
        if book_result not in check_book_update_options:
            print("Input not valid. Try again.")
        else:
            valid_book_update_options = True
    if book_result == "1":
        print("Introduce new Author: ")
        new_author = input()
        sql = "UPDATE `book` SET `authors` = %s WHERE `ISBN`= %s"
        value = (new_author, book_update)
        cursor.execute(sql, value)
        database.commit()
        print("Author Updated.")
    if book_result == "2":
        print("Introduce new Publisher: ")
        new_publisher = input()
        sql = "UPDATE `book` SET `publisher` = %s WHERE `ISBN`= %s"
        value = (new_publisher, book_update)
        cursor.execute(sql, value)
        database.commit()
        print("Publisher Updated.")
    if book_result == "3":
        print("Introduce new Category: ")
        new_category = input()
        sql = "UPDATE `book` SET `cat` = %s WHERE `ISBN`= %s"
        value = (new_category, book_update)
        cursor.execute(sql, value)
        database.commit()
        print("Category Updated.")
    if book_result == "4":
        print("Introduce new Price: ")
        new_price = input()
        if type(float(new_price)) not in (int, float):
            print("Price has to be a number. Introduce Price again: ")
            new_price = input()
        sql = "UPDATE `book` SET `price` = %s WHERE `ISBN`= %s"
        value = (new_price, book_update)
        cursor.execute(sql, value)
        database.commit()
        print("Price Updated.")


def update_ebook():
    valid_ebook_update = False
    while not valid_ebook_update:
        # Introducing the ISBN of the eBook to be updated
        print("Introduce the ISBN to update: ")
        ebook_update = input()
        sql = "SELECT * FROM `ebook` WHERE ISBN = %s"
        value = (ebook_update)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("The ISBN does not exist in the database. Try again.")
        else:
            valid_ebook_update = True
    # Show the user the eBook to edit
    print("Selected eBook:")
    for row in cursor.fetchall():
        print("eBook ID: ", row[0])
        print("ISBN: ", row[1])
        print("Title: ", row[2])
        print("Category: ", row[3])
        print("Author: ", row[4])
        print("Publisher: ", row[5])
        print("Price: $", row[6])
    print()
    print("************************************")
    print()
    valid_ebook_update_options = False
    while not valid_ebook_update_options:
        print("1. Update Author")
        print("2. Update Publisher")
        print("3. Update Category")
        print("4. Update Price")
        ebook_result = input()
        if ebook_result not in check_ebook_update_options:
            print("Input not valid. Try again.")
        else:
            valid_ebook_update_options = True
    if ebook_result == "1":
        print("Introduce new Author: ")
        new_author = input()
        sql = "UPDATE `ebook` SET `authors` = %s WHERE `ISBN`= %s"
        value = (new_author, ebook_update)
        cursor.execute(sql, value)
        database.commit()
        print("Author Updated.")
    if ebook_result == "2":
        print("Introduce new Publisher: ")
        new_publisher = input()
        sql = "UPDATE `ebook` SET `publisher` = %s WHERE `ISBN`= %s"
        value = (new_publisher, ebook_update)
        cursor.execute(sql, value)
        database.commit()
        print("Publisher Updated.")
    if ebook_result == "3":
        print("Introduce new Category: ")
        new_category = input()
        sql = "UPDATE `ebook` SET `cat` = %s WHERE `ISBN`= %s"
        value = (new_category, ebook_update)
        cursor.execute(sql, value)
        database.commit()
        print("Category Updated.")
    if ebook_result == "4":
        print("Introduce new Price: ")
        new_price = input()
        if type(float(new_price)) not in (int, float):
            print("Price has to be a number. Introduce Price again: ")
            new_price = input()
        sql = "UPDATE `ebook` SET `price` = %s WHERE `ISBN`= %s"
        value = (new_price, ebook_update)
        cursor.execute(sql, value)
        database.commit()
        print("Price Updated.")


def update_audio():
    valid_audio_update = False
    while not valid_audio_update:
        # Introducing the ISBN of the eBook to be updated
        print("Introduce the ISBN to update: ")
        audio_update = input()
        sql = "SELECT * FROM `audio` WHERE ISBN = %s"
        value = (audio_update)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("The ISBN does not exist in the database. Try again.")
        else:
            valid_audio_update = True
    # Show the user the eBook to edit
    print("Selected Audio:")
    for row in cursor.fetchall():
        print("Audio ID: ", row[0])
        print("ISBN: ", row[1])
        print("Title: ", row[2])
        print("Category: ", row[3])
        print("Author: ", row[4])
        print("Publisher: ", row[5])
        print("Duration: ", row[6], "sec")
        print("Price: $", row[7])
    print()
    print("************************************")
    print()
    valid_audio_update_options = False
    while not valid_audio_update_options:
        print("1. Update Author")
        print("2. Update Publisher")
        print("3. Update Category")
        print("4. Update Price")
        print("5. Update Duration")
        audio_result = input()
        if audio_result not in check_audio_update_options:
            print("Input not valid. Try again.")
        else:
            valid_audio_update_options = True
    if audio_result == "1":
        print("Introduce new Author: ")
        new_author = input()
        sql = "UPDATE `audio` SET `authors` = %s WHERE `ISBN`= %s"
        value = (new_author, audio_update)
        cursor.execute(sql, value)
        database.commit()
        print("Author Updated.")
    if audio_result == "2":
        print("Introduce new Publisher: ")
        new_publisher = input()
        sql = "UPDATE `audio` SET `publisher` = %s WHERE `ISBN`= %s"
        value = (new_publisher, audio_update)
        cursor.execute(sql, value)
        database.commit()
        print("Publisher Updated.")
    if audio_result == "3":
        print("Introduce new Category: ")
        new_category = input()
        sql = "UPDATE `audio` SET `cat` = %s WHERE `ISBN`= %s"
        value = (new_category, audio_update)
        cursor.execute(sql, value)
        database.commit()
        print("Category Updated.")
    if audio_result == "4":
        print("Introduce new Price: ")
        new_price = input()
        if type(float(new_price)) not in (int, float):
            print("Price has to be a number. Introduce Price again: ")
            new_price = input()
        sql = "UPDATE `audio` SET `price` = %s WHERE `ISBN`= %s"
        value = (new_price, audio_update)
        cursor.execute(sql, value)
        database.commit()
        print("Price Updated.")
    if audio_result == "5":
        print("Introduce new Duration: ")
        new_duration = input()
        while not new_duration.isdigit():
            print("Duration has to be a number. Introduce Duration again: ")
            new_duration = input()
        sql = "UPDATE `audio` SET `duration` = %s WHERE `ISBN`= %s"
        value = (new_duration, audio_update)
        cursor.execute(sql, value)
        database.commit()
        print("Duration Updated.")


########################################################################################
############################# DELETE SECTION ###########################################
########################################################################################


def delete():
    valid_delete = False
    while not valid_delete:
        print("*** Delete Site ***")
        print("1. Delete Book")
        print("2. Delete eBook")
        print("3. Delete Audio")
        print("4. Delete Order")
        print("5. Delete User")
        print("Introduce a number to select an option: ")
        delete = input()
        if delete not in check_delete:
            print("Input not valid. Try again.")
        else:
            valid_delete = True
    if delete == "1":
        delete_book()
    if delete == "2":
        delete_ebook()
    if delete == "3":
        delete_audio()
    if delete == "4":
        delete_order()
    if delete == "5":
        delete_user()


# Delete book
def delete_book():
    valid_delete_book = False
    while not valid_delete_book:
        print("Introduce the ISBN of the Book you want to delete: ")
        delete_book = input()
        sql = "SELECT * FROM `book` WHERE ISBN = %s"
        value = (delete_book)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("The ISBN does not exist in the database. Try again.")
        else:
            valid_delete_book = True
    for row in cursor.fetchall():
        print("Book ID: ", row[0])
        print("ISBN: ", row[1])
        print("Title: ", row[2])
        print("Category: ", row[3])
        print("Author: ", row[4])
        print("Publisher: ", row[5])
        print("Price: $", row[6])
        print("Rent ID: ", row[7])
    print()
    print("************************************")
    print()
    sql = "DELETE FROM `book` WHERE ISBN = %s"
    value = (delete_book)
    cursor.execute(sql, value)
    database.commit()
    print()
    print("Book deleted from the database.")
    print("************************************")
    print()

# Delete eBook
def delete_ebook():
    valid_delete_ebook = False
    while not valid_delete_ebook:
        print("Introduce the ISBN of the eBook you want to delete: ")
        delete_ebook = input()
        sql = "SELECT * FROM `ebook` WHERE ISBN = %s"
        value = (delete_ebook)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("The ISBN does not exist in the database. Try again.")
        else:
            valid_delete_ebook = True
    for row in cursor.fetchall():
        print("Book ID: ", row[0])
        print("ISBN: ", row[1])
        print("Title: ", row[2])
        print("Category: ", row[3])
        print("Author: ", row[4])
        print("Publisher: ", row[5])
        print("Price: $", row[6])
        print("Rent ID: ", row[7])
    print()
    print("************************************")
    print()
    sql = "DELETE FROM `ebook` WHERE ISBN = %s"
    value = (delete_ebook)
    cursor.execute(sql, value)
    database.commit()
    print()
    print("eBook deleted from the database.")
    print("************************************")
    print()

# Delete Audio
def delete_audio():
    valid_delete_audio = False
    while not valid_delete_audio:
        print("Introduce the ISBN of the Audio you want to delete: ")
        delete_audio = input()
        sql = "SELECT * FROM `audio` WHERE ISBN = %s"
        value = (delete_audio)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("The ISBN does not exist in the database. Try again.")
        else:
            valid_delete_audio = True
    for row in cursor.fetchall():
        print("Book ID: ", row[0])
        print("ISBN: ", row[1])
        print("Title: ", row[2])
        print("Category: ", row[3])
        print("Author: ", row[4])
        print("Publisher: ", row[5])
        print("Duration: ", row[6], "sec")
        print("Price: $", row[7])
        print("Rent ID: ", row[8])
    print()
    print("************************************")
    print()
    sql = "DELETE FROM `audio` WHERE ISBN = %s"
    value = (delete_audio)
    cursor.execute(sql, value)
    database.commit()
    print()
    print("Audio deleted from the database.")
    print("************************************")
    print()

def delete_order():
    valid_delete_order = False
    while not valid_delete_order:
        print("Introduce the order ID of the Order you want to delete: ")
        delete_order = input()
        sql = "SELECT * FROM `final_order` WHERE oid = %s"
        value = (delete_order)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("The Order does not exist in the database. Try again.")
        else:
            valid_delete_order = True
    for row in cursor.fetchall():
        print("Order ID: ", row[0])
        print("Quantity: ", row[1])
        print("Book ISBN: ", row[2])
        print("eBook ISBN: ", row[3])
        print("Audio ISBN: ", row[4])
    print()
    print("************************************")
    print()
    sql = "DELETE FROM `final_order` WHERE oid = %s"
    value = (delete_order)
    cursor.execute(sql, value)
    database.commit()
    print()
    print("Order deleted from the database.")
    print("************************************")
    print()


def delete_user():
    valid_delete_user = False
    while not valid_delete_user:
        print("Introduce your User ID to delete it: ")
        delete_user = input()
        sql = "SELECT * FROM `user` WHERE uid = %s"
        value = (delete_user)
        result = cursor.execute(sql, value)
        database.commit()
        if result == 0:
            print("The User does not exist in the database. Try again.")
        else:
            valid_delete_user = True
    for row in cursor.fetchall():
        print("User ID: ", row[0])
        print("Age: ", row[1])
        print("First Name: ", row[2])
        print("Last Name: ", row[3])
        print("Birth Date: ", row[4])
    print()
    print("************************************")
    print()
    sql = "DELETE FROM `user` WHERE uid = %s"
    value = (delete_user)
    cursor.execute(sql, value)
    database.commit()
    print()
    print("User deleted from the database.")
    print("************************************")
    print()


########################################################################################
############################### EXIT SECTION ###########################################
########################################################################################


def exit_programm():
    print("Exiting program...")
    sys.exit()


########################################################################################
############################### USER MENU ##############################################
########################################################################################


while loop:
    if aux == 0:
        valid_menu = False
        while not valid_menu:
            print("************* User Menu **************")
            print("1. Create Account")
            print("2. Login")
            print("3. Search")
            print("4. Insert")
            print("5. Update")
            print("6. Delete")
            print("7. Exit")
            print("**************************************")
            print("Introduce a number to choose a section:")
            input = int(input())
            # Check if the input is valid
            if input in check_menu:
                valid_menu = True
            else:
                print("Input not valid. Try again.")
                del input
            aux = 1

    # Create Account section selected
    if input == 1:
        del input
        create_account()
        aux = 0

    # Login section selected
    if input == 2:
        del input
        login()
        aux = 0

    # Search section selected
    if input == 3:
        del input
        search()
        aux = 0

    # Insert section selected
    if input == 4:
        del input
        insert()
        aux = 0

    # Update section selected
    if input == 5:
        del input
        update()
        aux = 0

    # Delete section selected
    if input == 6:
        del input
        delete()
        aux = 0

    # Exit section selected
    if input == 7:
        del input
        exit_programm()
