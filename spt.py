import argparse
import re
import time


class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.rule = None
        self.nextTrie = None


class Trie:
    def __init__(self):
        node = Node()
        self.start = node
        self.count = 0

    def addNode(self, node, prefix):

        if len(prefix) > 0:
            t = prefix.pop(0)
            if t == '0':
                if node.left is None:
                    node.left = Node()
                return self.addNode(node.left, prefix)
            elif t == '1':
                if node.right is None:
                    node.right = Node()
                return self.addNode(node.right, prefix)
        else:
            node.nextTrie = "Should have value"
            return node

    def insert(self, prefix):
        return self.addNode(self.start, prefix)


def insert(node, prefix, rule):

    if len(prefix):
        t = prefix.pop(0)
        if t == '0':
            if node.left is None:
                node.left = Node()
            return insert(node.left, prefix, rule)
        elif t == '1':
            if node.right is None:
                node.right = Node()
            return insert(node.right, prefix, rule)
    else:
        node.rule = rule
        return node


def match1(prefix, node, nextTrie):
    # print(prefix)

    # print("inside matching")
    if node and len(prefix):
        t = prefix.pop(0)
        # print(node.nextTrie)
        if node.nextTrie:
            # print("has next Tire")
            nextTrie.append(node.nextTrie)

        if t == "0":
            # print("0", end="")
            match1(prefix, node.left, nextTrie)
        elif t == "1":
            # print("1", end="")
            match1(prefix, node.right, nextTrie)
        # else:
        #     print("reached end of string")

        return nextTrie
    else:
        # print("Reached ENd")
        return nextTrie


def match2(prefix, node, ruleList):
    if node and len(prefix):
        if node.rule:
            ruleList.append(node.rule)
            # print(ruleList)
        t = prefix.pop(0)
        if t == "0":
            # if node.left:
            match2(prefix, node.left, ruleList)
        elif t == "1":
            # if node.right:
            match2(prefix, node.right, ruleList)

    return ruleList


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str)
    parser.add_argument('-i', type=str)
    parser.add_argument('-o', type=str)

    args = parser.parse_args()

    ruleTable = {}
    F1rule = {}
    trie = Trie()
    F1set = {}
    F2set = {}

    with open(args.p, 'r') as ruleFile:
        count = 1
        for line in ruleFile:
            ruleAdd = line.split(' ')
            ruleNum = int(ruleAdd[0])
            ruleTable[ruleNum] = {'F1': [], 'F2': []}

            F1 = ruleAdd[1].split('.')
            F1 = (bin(int(F1[0]))[2:]).zfill(8) + (bin(int(F1[1]))[2:]).zfill(8)
            ruleTable[ruleNum]['F1'] = F1[0:int(ruleAdd[2])]

            F2 = ruleAdd[3].split('.')
            F2 = (bin(int(F2[0]))[2:]).zfill(8) + (bin(int(F2[1]))[2:]).zfill(8)
            ruleTable[ruleNum]['F2'] = F2[0:int(ruleAdd[4])]
            if ruleTable[ruleNum]['F1'] in F1set:
                F1set[ruleTable[ruleNum]['F1']].add(ruleNum)
            else:
                F1set[ruleTable[ruleNum]['F1']] = {ruleNum, }

            prefix = []
            prefix[:0] = ruleTable[ruleNum]['F1']
            F2set[count] = trie.insert(prefix)
            count += 1
            if ruleTable[ruleNum]['F1'] in F1rule:
                F1rule[ruleTable[ruleNum]['F1']].add(ruleNum)
            else:
                F1rule[ruleTable[ruleNum]['F1']] = {ruleNum, }

        for key1, value1 in F1set.items():
            # print("matching for ", key1)
            for key2, value2 in F1set.items():
                key2 = '^' + key2
                if re.findall(key2, key1):
                    F1set[key1] = F1set[key1].union(value2)
                    # print(F1set[key1])

        # pprint(F1set)
        # Create tire 2
        for key, value in F1set.items():
            tempNode = Node()
            for ruleL2 in value:
                prefix = []
                prefix[:0] = ruleTable[ruleL2]['F2']
                insert(tempNode, prefix, ruleL2)

            # insert in tire 2
            for i in F1rule[key]:
                F2set[i].nextTrie = tempNode

    with open(args.i, 'r') as inputFile:
        totalTime = 0
        with open(args.o, 'w+') as outputFile:
            head = ["Address 1", "Address 2", "No. of Matches", "Rules matched", "Search Time (micro sec)"]
            outputFile.write(
                f"{head[0]:12} {head[1]:12} {head[2]:18} {head[3]:18} {head[4]:12}\n")
            count = 0
            lineNo = 0
            for line in inputFile:
                begin = time.perf_counter()
                lineNo += 1
                address = line.split(' ')

                address1 = address[0].split('.')
                address2 = address[1].split('.')
                address1bin = (bin(int(address1[0]))[2:]).zfill(8) + (bin(int(address1[1]))[2:]).zfill(8)
                address2bin = (bin(int(address2[0]))[2:]).zfill(8) + (bin(int(address2[1]))[2:]).zfill(8)

                prefix1 = []
                prefix2 = []

                prefix1[:0] = address1bin
                prefix2[:0] = address2bin

                nextTrie = match1(prefix1, trie.start, [])
                ad1 = str(int(address1[0]))+ '.' + str(int(address1[1]))
                ad2 = str(int(address2[0]))+ '.'  + str(int(address2[1]))


                if len(nextTrie):
                    result = match2(prefix2, nextTrie[-1], [])
                    if len(result):
                        resulttemp = str(result)
                        end = time.perf_counter()
                        totalTime += end - begin
                        tempStr = f"{ad1:>8} {ad2:>12} {len(result):>10} {resulttemp:>20} {int((end - begin)*1000000):25}\n"
                        outputFile.write(tempStr)

                    else:
                        resulttemp = str(result)
                        end = time.perf_counter()
                        totalTime += end - begin
                        tempStr = f"{ad1:>8} {ad2:>12} {0:>10} {resulttemp:>20} {int((end - begin)*1000000):25}\n"
                        outputFile.write(tempStr)
                else:
                    resulttemp = str([])
                    end = time.perf_counter()
                    totalTime += end - begin

                    tempStr = f"{ad1:>8} {ad2:>12} {0:>10} {resulttemp:>20} {int((end - begin)*1000000):25}\n"
                    outputFile.write(tempStr)

            outputFile.write(f"\n Average Search time is: {int(totalTime/lineNo*1000000)} (micro sec)")
