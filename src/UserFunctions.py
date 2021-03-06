import hashlib
import mysql.connector as mysql
import datetime as dt

# db = mysql.connect(
#    host ="rm-gs595dd89hu8175hl6o.mysql.singapore.rds.aliyuncs.com",
#    user ="ict1902698psk",
#    passwd ="KSP8962091",
#    database = "sql1902698psk"
# )
# cursor = db.cursor()

#Function to authenticate the user and grab the user details out, also checks for the user
#Tier whether the subscription has expired
def UserAuth(db, cursor, Username, Password):
    query = "SELECT * FROM user WHERE user.UserName = '{0}' AND UserPw = SHA2('{1}',256)".format(Username,Password)
    cursor.execute(query)
    result = cursor.fetchone()
    if result == None:
        return result
    #Updating to check whether user have expired his paid priveledges
    if (result[3] == 2):
        query = "SELECT OrderDate FROM order_details WHERE order_details.UserID = '{0}' ORDER BY OrderDate LIMIT 1".format(result[0])
        cursor.execute(query)
        receipt = cursor.fetchone()
        #If it expires set it as 1 which is a free user
        if (receipt[0] + dt.timedelta(days = 30)) < dt.datetime.now().date():
            sql = "UPDATE user SET TierID = 1 WHERE UserID = {0}".format(result[0])
            cursor.execute(sql)
            db.commit()
            result = list(result)
            result[3] = 1
    return result

#Function to create the user all password are also hashed in the database using SHA256
def UserCreate(db, cursor, UserName, Password):
    try:
        query = "INSERT INTO user VALUES (%s, %s, SHA2(%s,256), DEFAULT(TierID), DEFAULT(isAdmin),DEFAULT,DEFAULT)"
        val = (0, UserName,Password)
        cursor.execute(query, val)
        db.commit()
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        result = cursor.fetchone()

        return result
    except:
        return False

#Function to insert payment method that is aes256 encrpyted using mysql library
def InsertPaymentMethod(db, cursor, UserID, CardNo, CardExpiryDate):
    query = "UPDATE user SET CardNo = AES_ENCRYPT(%s,%s), CardExpiryDate = %s WHERE UserID = %s"
    val = (CardNo,UserID,CardExpiryDate,UserID)
    cursor.execute(query, val)
    db.commit()
    if cursor.rowcount > 0:
        return True
    else:
        return False

#Fucntion to retrieve user payment details that is decrypted using mysql library
def SelectUserPayment(cursor, UserID):
    query = "SELECT CAST(AES_DECRYPT(CardNo,{0}) as CHAR),CardExpiryDate FROM user WHERE UserID = {0}".format(UserID)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

#Selected articles that the user liked
def SelectLikedArticles(cursor, UserID):
    query = "SELECT a.ArticleID, a.ArticleTitle, a.ArticleDate, c.CategoryName, p.AgencyName " \
            "FROM likedby l, article a, agency p, articlecategory c " \
            "WHERE l.UserID = {0} AND a.ArticleID = l.ArticleID AND a.AgencyID = p.AgencyID AND a.CategoryID = c.CategoryID".format(UserID)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

#Function to upgrade the user and capture the receipt date
def Transact(db,cursor,UserID):
    try:
        #Insert Receipt
        query = "INSERT INTO order_details VALUES (%s,%s,%s,%s)"
        val = (0, 10, dt.datetime.now().date(),UserID)
        cursor.execute(query, val)
        #Update the person's tier
        query = "UPDATE user SET TierID = 2 WHERE UserID = {0}".format(UserID)
        cursor.execute(query)
        db.commit()
        return True
    except:
        return False

#Function to check the tier of the user
def CheckTier(cursor,UserID):
    query = "SELECT TierID FROM user where UserID = {0}".format(UserID)
    cursor.execute(query)
    result = cursor.fetchone()
    return result


#Function to delete the user
def DeleteUser(db,cursor,UserID):
    query = "DELETE FROM user where UserID = {0}".format(UserID)
    cursor.execute(query)
    db.commit()
    if cursor.rowcount > 0:
        return True
    else:
        return False


#print(Transact(db,cursor,8))
#print(UserAuth(db,cursor,"test1","123"))
#print(InsertPaymentMethod(db,cursor,7,"5500 0000 0000 0004","03/21"))
#print (SelectUserPayment(cursor, 7))
#print(UserAuth(cursor,"test","1234"))
#print(UserCreate(db,cursor,"test4","123"))
#print(SelectLikedArticles(cursor,7))
#print(CheckTier(cursor,"6"))
