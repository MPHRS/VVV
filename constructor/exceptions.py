class NegativeValueError(Exception):
    def __str__(self):
        return "Some node in grpah is negative"

class GapsMolGraphError(Exception):
    def __str__(self):
        return "Gaps in indexation were detected"
    
class MolGraphSimplicityError(Exception):
    def __str__(self):
        return "Graph is not simple"
    
class MolGraphConnectionError(Exception):
    def __str__(self):
        return "Graph is not connected" 
    
class OutBoxError(Exception):
    def __str__(self):
        return "Some bead occure out of box > 1.5 box"    
        
        