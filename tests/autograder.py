import json
import csv
import glob
from pprint import pprint
from collections import Counter

from app.app import student as student
TEAM = 1 # enter your team number here

def check_tools(answer, stud):
    score = 0
    expans = dict([[a,a.split()] for a in answer])

    for s in stud:
        if s in answer:
            print s
            score += 1
            answer.remove(s)
            stud.remove(s)

    expans = dict([[a,{'words':a.split(), 'matches':Counter()}] for a in answer])
    expstud = dict([[a,a.split()] for a in stud])
    
    for s in expstud:
        tmpscore = -1
        for word in expans:
            complement = set(expstud[s]) ^ set(expans[word]['words'])
            intersection = set(expstud[s]) & set(expans[word]['words'])
            newscore = float(len(intersection))/(len(intersection)+len(complement))
            print "%s, %s, %d, %d, %f"%(s,word,len(intersection),len(complement),newscore)
            if newscore > tmpscore:
                tmpscore = newscore
                tmpmatch = word
        if tmpscore > 0:
            expans[tmpmatch]['matches'][s] = tmpscore
            stud.remove(s)

    for word in expans:
        match = expans[word]['matches'].most_common(1)
        if len(match) > 0:
            score += expans[word]['matches'].most_common(1)[0][1]

    return score

def check_ingredients(answer,stud):
    scores = []
    score = 0

    for x in range(min([len(answer),len(stud)])):
        for ind in ['name','measurement','quantity','descriptor','preparation','prep-description']:
            if ind in stud[x]:
                print stud[x][ind]
                print answer[x][ind]
                if stud[x][ind] in answer[x][ind]:
                    score += 1
        print "---"
        scores.append(min([score,answer[x]['max']]))
        score = 0

    return sum(scores)

def get_file(fn):
    with open(fn, 'r') as f:
        answer = json.load(f)
    return answer

def main(init=False):
    with open('parsegrades.csv','ab') as csvfile:
        csvwriter = csv.writer(csvfile,delimiter='\t')
        keys = ['ingredients','primary cooking method','cooking methods','cooking tools']
        if init:
            csvwriter.writerow(keys)
        scores = dict(zip(keys,[0]*len(keys)))
        
        tmpmeth = 0
        tmptool = 0
        tmping = 0

        for answer in (get_file(fn) for fn in glob.iglob('../Recipes/*.json')):
            stud = student(answer['url'])
            if type(stud) == str:
                stud = json.loads(stud)
            pprint(stud)
            if type(stud) == dict:            
                tmptool = min([check_tools(answer['cooking tools'],stud['cooking tools']), answer['max']['cooking tools']])/float(answer['max']['cooking tools'])
                scores['cooking tools'] += tmptool
                tmpmeths = min([check_tools(answer['cooking methods'],stud['cooking methods']), answer['max']['cooking methods']])/float(answer['max']['cooking methods'])
                scores['cooking methods'] += tmpmeths
                if stud['primary cooking method'] == answer['primary cooking method']:
                    tmpmeth = 1
                    scores['primary cooking method'] += 1
                stud = stud['ingredients']
                tmping = check_ingredients(answer['ingredients'],stud)/float(answer['max']['ingredients'])
                scores['ingredients'] += tmping
                print "%.3f\t%d\t%.3f\t%.3f"%(tmping,tmpmeth,tmpmeths,tmptool)
            else:
                print "student answer error"
        row = ["Team %d"%TEAM]
        row.extend([scores[k] for k in keys])
        csvwriter.writerow(row)

def main_for_test():
    result = []
    for answer in (get_file(fn) for fn in glob.iglob('tests/Recipes/*.json')):
        stud = student(answer['url'])
        print 'ZZZ' + stud['primary cooking method']
        tmpmeth = 0
        tmptool = 0
        tmping = 0
        tmpmeths = 0
        if type(stud) == str:
            stud = json.loads(stud)
        if type(stud) == dict:
            tmptool = min([check_tools(answer['cooking tools'],stud['cooking tools']), answer['max']['cooking tools']])/float(answer['max']['cooking tools'])
            tmpmeths = min([check_tools(answer['cooking methods'],stud['cooking methods']), answer['max']['cooking methods']])/float(answer['max']['cooking methods'])
            if stud['primary cooking method'] == answer['primary cooking method']:
                tmpmeth = 1
            stud = stud['ingredients']
            tmping = check_ingredients(answer['ingredients'],stud)/float(answer['max']['ingredients'])
        result.append((tmping, tmpmeth, tmpmeths, tmptool))
    return result


if __name__ == '__main__':
    main()