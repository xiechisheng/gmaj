import MySQLdb
import hashlib


def mysql_password(str):
    """
    Mysql密码信息--设置
    :return:
    """
    value = hashlib.sha1(str.encode(encoding="UTF-8", errors="strict")).digest()
    value = hashlib.sha1(value).hexdigest()

    pwdStr = "*" + value.upper()

    return pwdStr


def initDatabase():
    """
    数据库信息--初始化
    :return:
    """
    mySQL = MySQLdb.connect(host="10.143.10.214", user="netsin", passwd="netsin", db="gmaj", port=3306, charset="utf8")
    cursorDB = mySQL.cursor()

    try:
        strAdminSQL = "insert into api_user_info(login, password, nickname, dept, longitude, latitude, height, enable, level, position, role, register) values('admin', %s, 'admin', 1, 1, 1, 0, 1, 5, 32767, 10, now())"
        value = (mysql_password("admin"),)
        cursorDB.execute(strAdminSQL, value)
    except Exception as err:
        print("Create admin user information: ", format(err))

    try:
        strDeptRootSQL = "insert into api_dept(name, pid, enable, path, position, register) values('root', 0, 1, '/', 32767, now())"
        cursorDB.execute(strDeptRootSQL)
    except Exception as err:
        print("Create root dept information: ", format(err))

    try:
        strConfigSQL = "insert into api_option_sys(opt_name, opt_key, opt_value, opt_modify)  values('消息推送服务器地址', 'push_server_ip', '192.168.181.53', 1)"
        cursorDB.execute(strConfigSQL)

        strConfigSQL = "insert into api_option_sys(opt_name, opt_key, opt_value, opt_modify)  values('消息推送服务器端口', 'push_server_port', '1883', 1)"
        cursorDB.execute(strConfigSQL)

        strConfigSQL = "insert into api_option_sys(opt_name, opt_key, opt_value, opt_modify)  values('推送心跳(秒)', 'push_client_keepalive', '10', 1)"
        cursorDB.execute(strConfigSQL)

        strConfigSQL = "insert into api_option_sys(opt_name, opt_key, opt_value, opt_modify)  values('监测信息更新时长(秒)', 'iot_update_time' , '10', 1)"
        cursorDB.execute(strConfigSQL)
    except Exception as err:
        print("Create option_sys information: ", format(err))

    mySQL.commit()
    cursorDB.close()
    mySQL.close()


if __name__ == "__main__":
    initDatabase()