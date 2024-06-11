from database.DB_connect import DBConnect
from model.cibo import Cibo
from model.connessione import Connessione


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getNodi(nporzioni):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.food_code,f.display_name
FROM food f,food_pyramid_mod.portion p
where f.food_code =p.food_code 
group by f.food_code,f.display_name 
having count(distinct p.portion_id)>=%s """

        cursor.execute(query,(nporzioni,))

        for row in cursor:
            result.append(Cibo(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCibi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT f.food_code,f.display_name
                FROM food f"""

        cursor.execute(query)

        for row in cursor:
            result.append(Cibo(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getConnessioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.f1 as v1,t2.f2 as v2, count(distinct t1.c1) as peso
                from (select fc.food_code as f1, fc.condiment_code as c1
                from food_condiment fc) as t1,
                (select fc.food_code as f2, fc.condiment_code as c2
                from food_condiment fc) as t2
                where t1.f1!=t2.f2 and t1.c1=t2.c2
                group by t1.f1,t2.f2 """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result
