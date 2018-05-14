
import math, os, json
import re
def compute_angle(vector_query, vector_doc):
    product = 0
    lenght_query = 0
    lenght_doc = 0 

    for term in vector_query.keys():
        product = product + vector_query[term]* vector_doc.get(term, 0)
        lenght_query =  lenght_query + vector_query[term]**2
        lenght_doc =  lenght_doc + vector_doc.get(term, 0)**2
    lenght_query = math.sqrt(lenght_query)
    lenght_doc = math.sqrt(lenght_doc)
    lenght = lenght_query*lenght_doc
    if lenght == 0:
        cos = -1
    else:
        cos = product/lenght
    return math.acos(cos) * 180/math.pi
