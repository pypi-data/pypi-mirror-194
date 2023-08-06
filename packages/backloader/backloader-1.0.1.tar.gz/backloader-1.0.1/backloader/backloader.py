class backloader():
  def bl_init():
    from alive_progress import alive_bar
    from termcolor import colored
    import re
    import importlib
    # Read the contents of the file
    with open('module.json', 'r') as f:
        json_data = f.read()
    
    # Use regex to extract the project names
    project_names = re.findall(r'"project":"([^"]+)"', json_data)
    
    import os
    with alive_bar(5000) as bar:
      for mod in project_names:
        if importlib.util.find_spec(mod) is not None:
          try:
            print(f"[ baS ] [ LOAD ] {mod}")
            importlib.import_module(mod.replace("-", "_"))
          except ImportError:
            print(f"[ baS ] [ NOTFOUND ] {mod}")
            try:
              print(f"[ baS ] [ GET ] {mod}")
              os.system(f"pip install {mod} > /dev/null 2>&1")
              print(colored("[ baS ] [ OK ]", 'green'))
              print(f"[ baS ] [ LOAD ] {mod}")
              importlib.import_module(mod.replace("-", "_"))
              print(colored("[ baS ] [ OK ]", 'green'))
            except Exception as err: print(colored(f"[ baS ] [ ERROR ] {err}: {mod}", 'red', attrs=['bold']))
      
        print(colored(f"[ baS ] FINISH {mod} {importlib.util.find_spec(mod)}", 'green', attrs=['bold']))
        bar()
    