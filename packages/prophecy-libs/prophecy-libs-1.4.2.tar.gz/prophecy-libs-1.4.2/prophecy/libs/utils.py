from pyspark.sql.functions import array, lit, struct
def typed_lit(obj):
    if isinstance(obj, list):
        return array([typed_lit(x) for x in obj])
    elif isinstance(obj, dict):
        elementsList = []
        for key, value in obj.items():
            elementsList.append(typed_lit(value).alias(key))
        return struct(elementsList)
    else:
        try:
            # int, float, string
            return lit(obj)
        except:
            # class type
            return typed_lit(obj.__dict__)