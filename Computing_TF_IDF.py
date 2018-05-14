'''
Created on Apr 6, 2018

@author: VDT     
'''
import random
import json
import math
import glob, os
import threading
import re


def computeIDF(subfolder, stop):
    '''Tính số lần 1 từ xuất hiện trong 20k file'''
    global maxtrixx
    for file in os.listdir('./20_newsgroups/%s'%subfolder):
        with open('./20_newsgroups/%s/%s'%(subfolder, file), 'r') as myfile:
            data = list(set(re.sub('[^a-zA-Z\s]', ' ', myfile.read()).strip().replace("\n","").replace("\t", "").lower()
            .split(" ")))
            for item in data:
                if item not in stop:
                    maxtrixx[item] = maxtrixx.get(item, 0) + 1
                

def compute_tfidf_query(matrix, query):
    if not os.path.exists('./Result_TF_IDF_Query'):
        os.makedirs('./Result_TF_IDF_Query')
    tf_idf = {}
    query2 = list(set(re.sub('[^a-zA-Z\s]', ' ', query).strip().replace("\n","").replace("\t", "").lower()
            .split(" ")))
    for item in query2:
            count = float(query2.count(item))
            tf = count/len(query2)
            idf = 1 + math.log10(19998/(matrix.get(item, 1) + 1)) # if item not exist in maxxtrix ==> just exist in query ==> = 1
            tf_idf[item] = tf*idf
    tf_idf_file = open('./Result_TF_IDF_Query/tf_idf_vector_query.txt','w')
    tf_idf_file.seek(0)
    tf_idf_file.write(json.dumps(tf_idf ))
    tf_idf_file.close()
    return tf_idf
def saveFile(matrix, folder, files):
    tf_idf = {}
    for file in files:
        with open("./20_newsgroups/%s/%s" %(folder, file), 'r') as myfile:
            data2 = list(set(re.sub('[^a-zA-Z\s]', ' ', myfile.read()).strip().replace("\n","").replace("\t", "").lower().split(" ")))
            for item in data2:
                if matrix.get(item, 1) != 1: 
                    count = float(data2.count(item))
                    tf = count/len(data2)
                    idf = 1 + math.log10(19997/matrix[item]) # add 1 in case log = 0
                    tf_idf[item] = tf*idf
        tf_idf_file = open('./TF_IDF_DOCS/%s/%s_%s.txt'%(folder,folder,file),'w')
        tf_idf_file.seek(0)
        tf_idf_file.write(json.dumps(tf_idf))
        tf_idf_file.close()
        tf_idf = {}


def compute_tfidf_doc(matrix, folder):
    '''Mỗi folder có 100 files --> chia ra 3 thread để tính tf-idf và lưu file trong function saveFile()'''

    if not os.path.exists('./TF_IDF_DOCS/%s'%folder):
        os.makedirs('./TF_IDF_DOCS/%s'%folder)
    count = 0
    files = []
    size = len(os.listdir('./20_newsgroups/%s'%folder))
    threads = []
    for file in os.listdir('./20_newsgroups/%s'%folder):
        count += 1
        size -= 1
        files.append(file)
        if count == 400:
            t1 = threading.Thread(target=saveFile, args=(matrix,folder, files,))
            t1.start()
            count = 0
            files = []
            threads.append(t1)
        if size == 0:
            t1 = threading.Thread(target=saveFile, args=(matrix,folder, files,))
            t1.start()
            count = 0
            files = []
            threads.append(t1)
            break
    for t in threads:
        t.join()

maxtrixx = {} # (word : frequency) lưu tần số xuất hiện của tất cả các từ trong 20k file, dùng để tính idf nhanh hơn
def getMatrix():
    global maxtrixx
    stop = []
    with open('./stopwords_en.txt', 'r') as mf:
        stop = mf.read().replace("\n", " ").split(" ")
    
    if not os.path.exists('./CountIDF'):
        print("Computing Inverted Index, please wait 20s....")
        threads = []
        for sub_folder in os.listdir("./20_newsgroups"):
            t1 = threading.Thread(target=computeIDF, args=(os.path.basename(sub_folder),stop,))
            t1.start()
            threads.append(t1)
        for t in threads:
            t.join()
        os.makedirs('./CountIDF')
        count_idf = open('./CountIDF/count_idf.txt','w')
        count_idf.seek(0)
        count_idf.write(json.dumps(maxtrixx))
        count_idf.close()
        print("Done Inverted Index")
    else:
         maxtrixx = json.load(open('./CountIDF/count_idf.txt'))
    
    return maxtrixx

def compute_all_docs(matrix):
    print("Computing tf-idf for all documents... wait about 60s...")
    threads = []
    for subfolder in os.listdir("./20_newsgroups"):
        t1 = threading.Thread(target=compute_tfidf_doc, args=(matrix, subfolder,))
        t1.start()
        threads.append(t1)
    for t in threads:
        t.join()
    print("Done tf-idf")

