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
    visted = False

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
    maze = 0  # 2D array of nodes
    limit = 0
    state = []
    visitedNodes = []
    startNode = Node(0)  # could be id only pair
    endNode = Node(0)
    solved = 0

    def __init__(self, mazeStr, heristicValue=None):
        self.path.clear()
        self.fullPath.clear()
        rows = mazeStr.split()
        cols = rows[0].split(',')
        self.maze = [[0] * len(cols)] * len(rows)
        self.maze = []
        i = 0
        for x in rows:
            hell = []
            col = x.split(',')
            j = 0
            for y in col:
                node = Node(y)
                node.id = str(i) + "," + str(j)
                hell.append(node)
                if y == 'S':
                    self.startNode = node
                elif y == 'E':
                    self.endNode = node
                j += 1
            self.maze.append(hell.copy())
            i += 1
        self.limit = 30
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

    def test(self):
        for i in range(5):
            for j in range(7):
                print(self.maze[i][j].id)
            print()
        print("TEST OUT")

    def copy(self, node, newNode):
        newNode.value = node.value
        newNode.id = node.id
        newNode.previousNode = node.previousNode
        newNode.up = node.up
        newNode.down = node.down
        newNode.right = node.right
        newNode.left = node.left
        newNode.edgeCost = node.edgeCost
        newNode.gOfN = node.gOfN
        newNode.hOfN = node.hOfN
        newNode.heuristicFn = node.heuristicFn

        return

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
        i = x[0]
        j = x[1]
        newi = int(i)
        newj = int(j)
        if action == "up":
            newi = int(i) - 1
        elif action == "down":
            newi = int(i) + 1
        elif action == "right":
            newj = int(j) + 1
        else:
            newj = int(j) - 1
        '''for k in range(len(self.maze)):
            for z in range(len(self.maze[k])):
                if id == self.maze[k][z].id:
                    return self.maze[k][z]'''
        return self.maze[newi][newj]

    def backtrack(self, node):
        '''if node != None:
            self.path.append(node.id)
            self.backtrack(node.previousNode)
           '''
        self.path.append(self.endNode.id)
        self.path.append(node.id)
        self.totalCost += (self.endNode.hOfN + node.hOfN)
        while node.previousNode != None:
            node = node.previousNode
            self.path.append(node.id)
            self.totalCost += node.hOfN



    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.fullPath.append(self.startNode.id)
        self.recursive_dls(self.startNode, self.limit)
        return self.path[::-1], self.fullPath

    def recursive_dls(self, currentNode, limit):
        if self.isGoal(currentNode):
            self.backtrack(currentNode)
            self.solved = 1
            return self.path, self.fullPath  # backtrack function
        if limit == 0:
            return 1, self.fullPath  # cutoff
        cutOffOccured = 0
        actions = self.getChildren(currentNode)  # up down right left
        foundSolution = False
        for action in actions:
            child = self.MakeMove(currentNode, action)
            if self.solved == 0 and (currentNode.previousNode == None or child.id != currentNode.previousNode.id):
                child.previousNode = currentNode
                self.fullPath.append(child.id)
                result = self.recursive_dls(child, limit - 1)
                if result != 1 and result != 0:  # cutoff
                    foundSolution = True
            else:
                result = 0
            if result == 1:  # cutoff
                cutOffOccured = 1
        if foundSolution:
            return self.path, self.fullPath
        if cutOffOccured:
            return 1, self.fullPath
        if result != 0:  # fail
            return result
        else:
            return 0, self.fullPath  # fail


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

        while (len(Qs) != 0 and len(Qe) != 0):
            if len(Qs) != 0:
                nodeS = Qs.pop(0)
                self.fullPath.append(nodeS.id)
                if nodeS == nodeG or nodeS in Qe:
                    return self.path, self.fullPath
                actions = self.getChildren(nodeS)
                for action in actions:
                    child = self.MakeMove(nodeS, action)
                    if child.visteds == False:
                        child.visteds = True
                        Qs.append(child)

            if len(Qe) != 0:
                nodeG = Qe.pop(0)
                self.fullPath.append(nodeG.id)
                if nodeG == nodeS or nodeG in Qs:
                    return self.path, self.fullPath
                actions = self.getChildren(nodeG)
                for action in actions:
                    child = self.MakeMove(nodeG, action)
                    if child.vistede == False:
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

    #searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    #path, fullPath = searchAlgo.BDS()
    #print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
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