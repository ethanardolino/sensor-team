# sensor-team
Repo to aggregate all of the materials for the 15.359 S24 "Sensor Subteam." 

## Preliminary setup
There are a couple steps to be done after cloning this repo

### 1. Installing Dependencies
After cloning, be sure to run the following command in your command line:
'''linux
./setup.sh
'''
This will create a virtual environment instance for your local repo, and install the necessary dependencies in the 'venv'.

### 2. venv Alias (optional)
This step is not required, but highly suggested (unless you want to type a tedious command over and over again :) )! The following instructions will go step by step to give aliases to the commands to enter / exit the virtual environment. Without the aliases, the commands are:
```
$ source venv/bin/activate  # 'activate' venv
$ deactivate                # 'deactivate' venv
```

After completing the following instructions, the commands will be simplified to
```
$ va                        # 'activate' venv
$ vd                        # 'deactivate' venv
```
---
First, figure out which type of terminal shell you are using. If you are unsure, then run the command 
```linux
echo $SHELL
```
The output will be ```/bin/_shell_type_```. For instance, a *bash* shell will have the following output
```linux
/bin/bash
```

Next, open the *shell startup file* with a text editor. The *shell startup file* name will vary depending on the type of shell you are using. The following example is for a *bash* shell
```linux
vim ~/.bashrc
```

Lastly, add the following aliases to the file (location does not matter) :
```linux
alias va="source venv/bin/activate"
alias vd="deactivate"
```
