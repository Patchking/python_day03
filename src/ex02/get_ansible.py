import yaml
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("filename", help = "Enter todo.yml", type = str)
    args = parser.parse_args()
    todoyaml = None
    try:
        with open(args.filename, "r") as file:
            todoyaml = yaml.load(file, Loader = yaml.FullLoader)
    except Exception as e:
        print("Something went wrong")
        exit()
    
    #Base pattern to yaml
    send_command = {
        "name": "Eliot's book for ansible",
        "hosts": "all",
        "become": "yes",
        "tasks": [
            {
                "name": "Intall packages",
                "ansible.builtin.package": {
                    "name": [],
                    "state": "present"
                }
            }
        ]
    }

    #Parse and add packages to install
    for task in todoyaml["server"]["install_packages"]:
        send_command["tasks"][0]["ansible.builtin.package"]["name"].append(task)

    #Add copy command for evilcorp.html to let everthing work as planned
    send_command["tasks"].append({
        "name": "Copy html file",
        "copy": {
            "src": "evilcorp.html",
            "dest": "/root/evilcorp.html"
        }
    })

    #Parse and add install task
    for task in todoyaml["server"]["exploit_files"]:
        install_command = {
            "name": "Copy py files",
            "copy": {
                "src": task,
                "dest": f"/root/{task}"
            }
        }
        send_command["tasks"].append(install_command)

    #Parse and add execute task
    for task in todoyaml["server"]["exploit_files"]:
        run_command = {
            "name": "Execute command",
            "command": f"python3 /root/{task}"
        }
        if task == "consumer.py":
            run_command["command"] += " -e " + ','.join([guy for guy in todoyaml["bad_guys"]])
            send_command["tasks"].append(run_command)
        elif task == "exploit.py":
            send_command["tasks"].append(run_command)

    #Write down in deploy.yml
    try:
        with open("deploy.yml", "w") as file:
            yaml.dump([send_command], file)
    except Exception as e:
        print("Something went wrong")
        exit()


if __name__ == "__main__":
    main()
