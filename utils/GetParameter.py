from sqlalchemy import text
def getParameter(parameter,connection = None):
    sql = text("select value from parameters where upper(parametername) = upper(:parametername)")
    para = {'parametername' : parameter}
    result = connection.execute(sql,para).fetchall()
    if len(result) == 0:
        raise Exception(f"{parameter} NOT FOUND PLEASE CHECK")
    if len(result) > 2:
        raise Exception(f"More than 1 Value found for {parameter}")
    return result[0][0]