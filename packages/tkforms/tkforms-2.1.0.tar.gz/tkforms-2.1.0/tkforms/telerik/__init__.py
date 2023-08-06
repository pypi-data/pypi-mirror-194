import os
lib = os.path.dirname(__file__).replace("\\", "//")
list = [f'{lib}//'+str(i) for i in os.listdir(lib)]