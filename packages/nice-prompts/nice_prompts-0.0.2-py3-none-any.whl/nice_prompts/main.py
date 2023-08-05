from blessed import Terminal
import sys

class NicePrompt:
    """Make nice prompts to gather input from the user e.g. multiple choice

    Args:
        terminal (blessed.Terminal): Supply a blessed terminal to use. Defaults to a new blessed terminal
    
    """
    def __init__(self, terminal=Terminal()):
        self.terminal = terminal
    
    def selection(self, options):
        """Choose an item from a dictionary of options. Keys are availiable
        options, values are what the function will return if that option is selected

        Args:
            options (dict): A dictionary of options. Keys are availiable 
                options, values are what the function will return if that option 
                is selected

        Returns:
            Object: The value from the options dictionary that the user selected
        """
        _ = self.terminal

        selected = 0


        for c, i in enumerate(options.keys()):
            if c == selected:
                print(f"{_.lightgreen} 🭬 {_.normal}{i}")
            else:
                print(f" ◦ {i}")

        
        p = _.move_up(len(options))

        with _.cbreak():
            while True:
                val = _.inkey()
                if val.code == 343 or val.lower() == " ":
                    break
                if val.code == 258:
                    selected += 1
                    if selected > len(options)-1:
                        selected = 0
                if val.code == 259:
                    selected -= 1
                    if selected < 0:
                        selected = len(options)-1
                
                p = _.move_up(len(options))
                print(p, end='')
                sys.stdout.flush()

                for c, i in enumerate(options.keys()):
                    if c == selected:
                        print(f"{_.lightgreen} 🭬 {_.normal}{i}")
                    else:
                        print(f" ◦ {i}")
                
        
        return options[list(options.keys())[selected]]



    def multiselection(self, options, amount=-1, required=1):
        """Choose some items from a dictionary of options. Keys are availiable
        options, values are what the function will return if that option is selected

        Args:
            options (dict): A dictionary of options. Keys are availiable 
                options, values are what the function will return if that option 
                is selected

            amount (int, optional): The max amount of items the user can 
                select. Leave out for no limit.

            required (int, optional): The minimum amount of items the user can select. Defaults to 1.

        Returns:
            list[Object]: A list of the values from the options dictionary that the user selected
        """
        if amount == -1:
            amount = len(options)
        
        _ = self.terminal

        selected = 0

        chosen = []
        p = ''
        def print_list():
            nonlocal p
            print(p, end='')
            sys.stdout.flush()
            maxstr = f"Max {amount}." if amount < len(options) else ""
            if len(chosen) >= required:
                outof = f"/{required} required" if required > 0 else ""
                a = f"{_.lightgreen}{len(chosen)}{_.normal}{outof}. {maxstr}"
            else:
                a = f"{_.red}{len(chosen)}{_.normal}/{required} required. {maxstr}"
            print(f"Press space to choose an option, enter to finish. Selected {a}")
            for c, i in enumerate(options.keys()):
                if c == selected and c in chosen:
                    print(f"{_.lightgreen} 🭬 {i}{_.normal}")
                elif c == selected:
                    print(f"{_.lightgreen} 🭬 {_.normal}{i}")
                elif c in chosen:
                    print(f"{_.lightgreen} • {i}{_.normal}")
                else:
                    print(f" ◦ {i}")

            p = _.move_up(len(options)+1)
            

        print_list()
        with _.cbreak():
            while True:
                val = _.inkey()
                if val.code == 343 and len(chosen) >= required:
                    break
                if val.lower() == " ":
                    if not (selected in chosen) and len(chosen) != amount:
                        chosen.append(selected)
                    elif selected in chosen:
                        chosen.remove(selected)
                if val.code == 258:
                    selected += 1
                    if selected > len(options)-1:
                        selected = 0
                if val.code == 259:
                    selected -= 1
                    if selected < 0:
                        selected = len(options)-1
                
                print_list()
        
        return [options[list(options.keys())[i]] for i in chosen]