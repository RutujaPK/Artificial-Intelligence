from expand import expand



def a_star_search(dis_map, time_map, start, end):
    open = []
    closed=[]
    start_mark = Landmark(None, start)
    end_mark = Landmark(None, end)
    open.append(start_mark)
    while (len(open)>0):
        #pop the first element off the open_list
        my_landmark = open[0]
        index=0
        for iterator, landmark in enumerate(open):
            if landmark.cost < my_landmark.cost:
                index = iterator
                my_landmark = landmark
            elif landmark.cost == my_landmark.cost and landmark.name < my_landmark.name:
                index = iterator
                my_landmark = landmark

        closed.append(my_landmark.name)
        open.pop(index)
        
        if (end_mark.name == my_landmark.name):
            path = []
            helper = my_landmark
            while (helper != None):
                path.insert(0, helper.name)
                helper = helper.parent
            return path

        neighbours = expand(my_landmark.name, time_map)
        
        for neighbour in neighbours:
            if (neighbour in closed):
                continue
            new_landmark = Landmark(my_landmark, neighbour)
            new_landmark.start_dist = my_landmark.start_dist + time_map[my_landmark.name][neighbour]
            new_landmark.end_dist = dis_map[neighbour][end]
            new_landmark.cost = new_landmark.start_dist+new_landmark.end_dist

            helper1 = False
            for i in open:
                if i.name==new_landmark.name:
                    if new_landmark.start_dist < i.start_dist:
                        open.remove(i)
                    else:
                        helper1=True
            if helper1 is True:
                continue
            open.append(new_landmark)

class Landmark:
    def __init__(self, parent=None, name = None):
        self.cost =0 #f
        self.start_dist=0 #g
        self.end_dist = 0 #h
        self.name = name
        self.parent = parent
        
def depth_first_search(time_map, start, end):
    stack = [(start, [start])]
    while stack:
        path = stack.pop(-1)[1]
        node = path[-1]
        if node == end:
            return path
        neighbors = expand(node, time_map)
        for neighbor in neighbors:
            stack.append((neighbor, path+[neighbor]))
    
    #incase there is no path between nodes, return None
    return "No path available"
    
            
    

def breadth_first_search(time_map, start, end):
    
    # keep a track of visited nodes
    visited = []
    # keep tracks of all the paths
    queue = [[start]]
    
    # if start is the goal node then we return the path
    if start == end:
        print ('Start Node and End Node are the same')
        return queue
        
    #keep exploring until all possible paths possible paths are checked
    while queue:
        path = queue.pop(0)
        node = path[-1]
        
        if node == end:
            print(str(path))
            return path
        
        # Condition to check if the current node is present in visited or not
        if node not in visited:
            
            # Loop to iterate over neighbours of the node
            for neighbour in expand(node,time_map):
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
            
            visited.append(node)
            
    #incase there is no path between nodes, return None
    return "No path available"
    
