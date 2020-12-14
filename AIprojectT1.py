from collections import deque
class Node:
    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    left = None
    right = None
    previousNode = None  # Represents value of neighbors(parent).
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function
    visteds = False
    vistede = False
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
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)
    maze = [] # 2D array of nodes
    limit = 10
    state = []
    visitedNodes = []
    startNode = 0
    endNode = 0
 
    def __init__(self, mazeStr, heristicValue=None):
        rows = mazeStr.split()
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
        pass
 
    def test(self):
        for i in range(5):
            for j in range(7):
                if self.maze[i][j].previousNode != None:
                    print(self.maze[i][j].id + " -----> " + self.maze[i][j].previousNode.id)
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
        if (i-1) >= 0 and (self.maze[i-1][j].value == '.'):
            node.up = 1
            children.append("up")
        if (i+1) < len(self.maze) and (self.maze[i+1][j].value == '.'):
            node.down = 1
            children.append("down")
        if (j + 1) < len(self.maze[0]) and (self.maze[i][j+1].value == '.'):
            node.right = 1
            children.append("right")
        if (j-1) >= 0 and (self.maze[i][j-1].value == '.'):
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
            newi -= 1
        elif action == "down":
            newi += 1
        elif action == "right":
            newj += 1
        else:
            newj -= 1
        
        return self.maze[newi][newj]
 
    def backtrack(self,node):
        '''if node != None:
            self.backtrack(node.previousNode)
            self.path.append(node.id)
           '''
        self.path.append(node.id)
     
        while node.previousNode != None:
            node = node.previousNode
            self.path.append(node.id)

    def backtracke(self,node):
        self.path.append(node.id)
     
        while node.nextNode != None:
            node = node.nextNode
            self.path.append(node.id)
 

    def DLS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.recursive_dls(self.startNode, self.limit)
        return self.path[::-1], self.fullPath
 
    def recursive_dls(self, currentNode, limit):
        self.fullPath.append(currentNode.id)
        if self.isGoal(currentNode):
            self.backtrack(currentNode)
            return self.path, self.fullPath  # backtrack function
        if limit == 0:
            return 1  # cutoff
        cutOffOccured = False
        actions = self.getChildren(currentNode)  # up down right left
        for action in actions:
            child = self.MakeMove(currentNode, action)
            if child.id not in self.fullPath:
                child.previousNode = currentNode
                result = self.recursive_dls(child, limit - 1)
                if result == 1:  # cutoff
                    cutOffOccured = True
                elif result != 0:
                    return result
        if cutOffOccured == True:  # cutoff
            return 1
        return 0  # fail
 
    def BDS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        fromStart = []
        fromEnd = []

        self.path.clear()
        self.fullPath.clear()
        Qs = deque()
        Qs.append(self.startNode)
        self.startNode.visteds = True
        Qe = deque()
        Qe.append(self.endNode)
        self.endNode.vistede = True
        end = self.endNode.id
        start = self.startNode.id

        while(len(Qs) != 0 and len(Qe) != 0):
            if len(Qs) != 0:
                node = Qs.popleft()
                #fromStart.append(node.id)
                start = node.id
                self.fullPath.append(node.id)
                if node.id == end or node in Qe:  # Success
                    self.test()
                    #print(fromStart + fromEnd[::-1])
                    self.backtrack(node)
                    self.backtracke(node)
                    #self.backtrack(self.endNode)
                    return self.path, self.fullPath
                actions = self.getChildren(node)  # up down right left
                for action in actions:
                    child = self.MakeMove(node, action)
                    if child.visteds == False:
                        child.previousNode = node
                        child.visteds = True
                        Qs.append(child)
            
            if len(Qe) != 0:
                node = Qe.popleft()
                #fromEnd.append(node.id)
                end = node.id
                self.fullPath.append(node.id)
                if node.id == start or node in Qs:  # Success
                    self.test()
                    #print(fromEnd)
                    self.backtrack(node)
                    self.backtracke(self.endNode)
                    #self.backtrack(self.endNode)
                    return self.path, self.fullPath
                actions = self.getChildren(node)  # up down right left
                for action in actions:
                    child = self.MakeMove(node, action)
                    if child.vistede == False: 
                        child.nextNode = node
                        child.vistede = True
                        Qe.append(child)

        print("Hii :(")
        return 0, self.fullPath  # Failure


 
    def BFS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        return self.path, self.fullPath, self.totalCost
 
 
 
def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DLS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
 
                #######################################################################################
 
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BDS()
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
                #######################################################################################
 
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.', [0, 15, 2, 100, 60, 35, 30, 3
                                                                                                             , 100, 2, 15, 60, 100, 30, 2
                                                                                                             , 100, 2, 2, 2, 40, 30, 2, 2
                                                                                                             , 100, 100, 3, 15, 30, 100, 2
                                                                                                             , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.BFS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
               #######################################################################################
 
 
 
 
main()