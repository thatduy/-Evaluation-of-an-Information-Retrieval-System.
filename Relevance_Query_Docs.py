'''
Created on Apr 7, 2018

@author: ASUS
'''
import math, os, json
import Computing_TF_IDF
import ComputeAngle 
import threading
import matplotlib.pyplot as plt
from numpy import random
def threadSearch(subfolder, files, vector_query):
    '''Tính góc giữa 2 vector, lưu những kết quả có liên quan vào biến global
        Các thread dùng chung biến global result_search để lưu kết quả
    '''
    global result_search
    for file in files:
        vector_doc = json.load(open('./TF_IDF_DOCS/%s/%s' % (subfolder, file)))
        angles = ComputeAngle.compute_angle(vector_query, vector_doc)
        if angles != 180.0:
            result_search[file] = angles # smaller angle is closesr relevance
        

def search(subfolder, vector_query):
    '''Mỗi folder có 100 files --> chia ra 3 thread để search'''
    count = 0
    files = []
    size = len(os.listdir('./TF_IDF_DOCS/%s'%subfolder))
    threads = []
    for file in os.listdir('./TF_IDF_DOCS/%s'%subfolder):
        count = count + 1
        size = size - 1
        files.append(file)
        if count == 400:
            t = threading.Thread(target=threadSearch, args=(subfolder, files, vector_query))
            t.start()
            count = 0
            files = []
            threads.append(t)
        if size == 0:
            t = threading.Thread(target=threadSearch, args=(subfolder, files, vector_query))
            t.start()
            count = 0
            files = []
            files = []
            threads.append(t)
    for t1 in threads:
        t1.join()

def thread_search(query, category):
    '''Search mỗi folder bằng 1 thread --> có 20 threads'''
    vector_query = Computing_TF_IDF.compute_tfidf_query(matrix, query)
    global result_search
    precisions = []
    recalls = []
    threads = []
    for subfolder in os.listdir("./TF_IDF_DOCS"):
        t1 = threading.Thread(target=search,  args=(subfolder, vector_query))
        t1.start()
        threads.append(t1)
    for t in threads:
        t.join()
    sorted_matrix = sorted(result_search.items(), key=lambda x:x[1])
    i = 0.0
    relevance_docs = 0
    for relevance_file in sorted_matrix:
        i += 1
        if relevance_file[0].split("_")[0] == category:
            relevance_docs += 1
            precisions.append(relevance_docs/1000.0)
            recalls.append(relevance_docs/i)
            '''No need compute F-measure coz it is unuse'''
            #Fmeasure = 2/(1/(relevance_docs/1000.0) + 1/(relevance_docs/i))
    '''Draw graphy'''
    plt.plot(precisions, recalls)
    plt.axis([0, 1, 0, 1])
    plt.show()
    print(sorted_matrix[:20]) 


result_search = {}
print('Searching....')
matrix = Computing_TF_IDF.getMatrix()
if not os.path.exists('./TF_IDF_DOCS'):
    Computing_TF_IDF.compute_all_docs(matrix)

queryList = []
'''Đọc các query đã build sẵn, mỗi query có dạng "query::category" '''
with open('./Set_Of_Querys/querys.txt', 'r') as mf:
    queryList = mf.read().replace("\n", "").split(";")
line = random.choice(queryList)
query = line.split("::")[0]
category = line.split("::")[1]
print(query)
print(category)
thread_search(query, category)

