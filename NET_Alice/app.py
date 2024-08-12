from flask import Flask,render_template,request
from flask.views import View
import yaml

class Setup():
    def __init__(self):
        _yaml_controller = ExternalFileController()
        SystemConfiguration.machine_information_yaml = _yaml_controller.laod_yaml('./resource/system_configuration_file/machine_information.yaml')


class UpdateSystemConfiguration():
    def add_machine_information(self,config_name:str="",ip_address:str ="",os:str = "",
                                authentication:str = "",change_mode:bool = False,
                                command:list = ["show clock","show run"]):

        SystemConfiguration.machine_information_yaml[config_name] = {'ip': ip_address,
                                                                     'os': os,
                                                                     'auth': authentication,
                                                                     'mode': change_mode,
                                                                     'command': command}

    def delet_machine_information(self,config_name:str="") -> tuple:
        return (config_name,SystemConfiguration.machine_information_yaml.pop(config_name))


class SystemConfiguration():
    machine_information_yaml: dict = {}
    unique_configuration_yaml: dict = {}
    target_preset_yaml: dict = {}

    putting_directory_yaml: dict = {}


class ExternalFileController():
    def laod_yaml(self,dir_info:str = "") -> dict:
        with open(file=dir_info, encoding='utf-8',mode="r") as yaml_file:
            return yaml.safe_load(yaml_file)

    def update_Yaml(self,dir_info:str = "",input_dict:dict = {}):
        with open(file=dir_info, encoding='utf-8',mode="w") as yaml_file:
            yaml.dump(input_dict,
                      yaml_file,
                      default_flow_style=False,
                      allow_unicode=True)



app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'aaaad'

@app.route('/index', methods = ["GET" , "POST"])
def index():
    Setup()
    if request.method == "GET":
        return render_template("users.html",comment = "登録情報を入力して下さい")

    # 資料を更新する
    else:
        Setup()
        update_system_config = UpdateSystemConfiguration()
        external_file_controller = ExternalFileController()

        print(request.form['config_name'])
        print(request.form['ip_address'])
        print(request.form['os'])
        print(request.form['change_mode'])
        print(request.form['authentication'])

        command_list:list = []
        for data in request.form['command'].split("\n"):
            if data != "\r" and data != "":
                print(data)
                command_list.append(data.rstrip())
        print(command_list)

        update_system_config.add_machine_information(config_name=request.form['config_name'],
                                                     ip_address=request.form['ip_address'],
                                                     os=request.form['os'],
                                                     change_mode=bool(request.form['change_mode']),
                                                     authentication=request.form['authentication'],
                                                     command=command_list
                                                     )

        external_file_controller.update_Yaml(dir_info='./resource/system_configuration_file/machine_information.yaml',
                                             input_dict=SystemConfiguration.machine_information_yaml)

        return render_template("users.html",comment = "登録が完了しました")

@app.route('/machine_list', methods = ["GET" , "POST"])
def display_machine_list():
    Setup()
    return render_template("display_machine_list.html",
                           machin_indo_dict=SystemConfiguration.machine_information_yaml)



if __name__ == '__main__':
    app.run()

'''

if __name__ == '__main__':
    Setup()
    external_file_controller = ExternalFileController()

    update_system_config = UpdateSystemConfiguration()
    update_system_config.add_machine_information(config_name="aaa",
                                                 ip_address="1.1.1.1",
                                                 os="Windows",
                                                 change_mode=True,
                                                 authentication="crawler",
                                                 command=["show clock","show xxxx"]
                                                 )


    print(SystemConfiguration.machine_information_yaml)



    print(update_system_config.delet_machine_information("aaa"))

    print(SystemConfiguration.machine_information_yaml)

    external_file_controller.update_Yaml(dir_info='./resource/system_configuration_file/machine_information.yaml',
                                         input_dict=SystemConfiguration.machine_information_yaml)

'''