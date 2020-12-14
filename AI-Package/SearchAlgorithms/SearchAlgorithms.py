class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors(parent).
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = 0  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function
    vistede = False
    visteds = False
    nextNode = None

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = 0  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)
    maze = []  # 2D array of nodes
    limit = 10
    startNode = 0  # could be id only pair
    endNode = 0

    def __init__(self, mazeStr, heristicValue=None):
        self.path.clear()
        self.fullPath.clear()
        rows = mazeStr.split()
        self.maze = []
        i = 0
        for r in rows:
            rowLine = []
            cols = r.split(',')
            j = 0
            for c in cols:
                node = Node(c)
                node.id = str(i) + "," + str(j)
                rowLine.append(node)
                if c == 'S':
                    self.startNode = node
                elif c == 'E':
                    self.endNode = node
                j += 1
            self.maze.append(rowLine.copy())
            i += 1
        #heuristic
        if(heristicValue != None):
            self.mapHeuristics(heristicValue)
        pass

    def mapHeuristics(self,heristicValue):
        k = 0
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                self.maze[i][j].hOfN = heristicValue[k]
                k+=1

    def isGoal(self, node):
        x = node.id.split(",")
        i = int(x[0])
        j = int(x[1])
        if (i - 1) >= 0 and self.maze[i - 1][j].value == 'E':
            return 1
        if (i + 1) < len(self.maze) and self.maze[i + 1][j].value == 'E':
            return 1
        if (j + 1) < len(self.maze[0]) and self.maze[i][j + 1].value == 'E':
            return 1
        if (j - 1) >= 0 and self.maze[i][j - 1].value == 'E':
            return 1
        return 0

    def getChildren(self, node):
        x = node.id.split(",")
        i = int(x[0])
        j = int(x[1])
        children = []
        if (i - 1) >= 0 and (self.maze[i - 1][j].value == '.'):
            node.up = 1
            children.append("up")
        if (i + 1) < len(self.maze) and (self.maze[i + 1][j].value == '.'):
            node.down = 1
            children.append("down")
        if (j + 1) < len(self.maze[0]) and (self.maze[i][j + 1].value == '.'):
            node.right = 1
            children.append("right")
        if (j - 1) >= 0 and (self.maze[i][j - 1].value == '.'):
            node.left = 1
            children.append("left")

        return children

    def MakeMove(self, Statenode, action):
        x = Statenode.id.split(",")
        newi = int(x[0])
        newj = int(x[1])
        if action == "up":
            newi -= 1
        elif action == "down":
            newi += 1
        elif action == "right":
            newj += 1
        else:
            newj -= 1
        
        return self.maze[newi][newj]

    def backtrack(self, node):
        self.path.append(node.id)
        self.totalCost += (self.endNode.hOfN + node.hOfN)
        temp = node
        while temp.previousNode != None:
            temp = temp.previousNode
            self.path.append(temp.id)
            self.totalCost += temp.hOfN
        
        while temp.nextNode != None:
            temp = temp.nextNode
            self.path.append(temp.id)

    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.fullPath.append(self.startNode.id)
        self.recursive_dls(self.startNode, self.limit)
        return self.path[::-1], self.fullPath

    def recursive_dls(self, currentNode, limit):
        self.fullPath.append(currentNode.id)
        if self.isGoal(currentNode):
            self.path.append(self.endNode.id)
            self.backtrack(currentNode)  # backtrack function
            return self.path, self.fullPath
        if limit == 0:
            return 1  # Cutoff
        cutOffOccured = False
        actions = self.getChildren(currentNode)  # up down right left
        for action in actions:
            child = self.MakeMove(currentNode, action)
            if child.id not in self.fullPath:
                child.previousNode = currentNode
                result = self.recursive_dls(child, limit - 1)
                if result == 1:  # Cutoff
                    cutOffOccured = True
                elif result != 0:
                    return result
        if cutOffOccured == True:  # Cutoff
            return 1
        return 0  # Failure
    
    def BDS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.path.clear()
        self.fullPath.clear()
        Qs = []
        Qe = []

        Qs.append(self.startNode)
        Qe.append(self.endNode)

        self.startNode.visteds = True
        self.endNode.vistede = True

        nodeS = self.startNode
        nodeG = self.endNode

        while(len(Qs) != 0 and len(Qe) != 0):
            if len(Qs) != 0:
                nodeS = Qs.pop(0)
                self.fullPath.append(nodeS.id)
                if nodeS == nodeG or nodeS in Qe:  # Success
                    self.backtrack(nodeS)
                    self.path.reverse()
                    self.backtrack(nodeG)
                    return self.path, self.fullPath
                actions = self.getChildren(nodeS)
                for action in actions:
                    child = self.MakeMove(nodeS, action)
                    if child.visteds == False:
                        child.previousNode = nodeS
                        child.visteds = True
                        Qs.append(child)
            
            if len(Qe) != 0:
                nodeG = Qe.pop(0)
                self.fullPath.append(nodeG.id)
                if nodeG == nodeS or nodeG in Qs:  # Success
                    self.backtrack(nodeS)
                    self.path.reverse()
                    self.backtrack(nodeG)
                    return self.path, self.fullPath
                actions = self.getChildren(nodeG)
                for action in actions:
                    child = self.MakeMove(nodeG, action)
                    if child.vistede == False:
                        child.nextNode = nodeG
                        child.vistede = True
                        Qe.append(child)

        return 0  # Failure

    def helpSort(self, node):
        return node.hOfN

    def BFS(self):
        closedlist = []
        openlist = [self.startNode]
        while len(openlist) != 0:
            if(len(openlist) == 0):
                return 0 , self.fullPath , self.totalCost #fail
            openlist.sort(key = self.helpSort)
            n = openlist[0]
            if self.isGoal(n):
                self.fullPath.append(n.id)
                self.fullPath.append(self.endNode.id)
                self.path.append(self.endNode.id)
                self.backtrack(n)
                return self.path[::-1] , self.fullPath , self.totalCost
            actions = self.getChildren(n)
            for action in actions:
                child = self.MakeMove(n, action)
                if child not in openlist and child not in closedlist:
                    child.previousNode = n
                    openlist.append(child)
            openlist.pop(0)
            closedlist.append(n)
            self.fullPath.append(n.id)


def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DLS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

    #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BDS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
    #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.',
                                  [0, 15, 2, 100, 60, 35, 30, 3
                                      , 100, 2, 15, 60, 100, 30, 2
                                      , 100, 2, 2, 2, 40, 30, 2, 2
                                      , 100, 100, 3, 15, 30, 100, 2
                                      , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.BFS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
    #######################################################################################


main()