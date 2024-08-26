from netmiko import ConnectHandler
import yaml
import multiprocessing
import os
class CollectNetworkMachineInfo(): # ネットワーク機器を操作するメソッド
    def __init__(self,os :str = "cisco",ip_address:str = "127.0.0.1",username :str = "",password:str = "",port_number:str = "22",command_list:list =[],save_dir:str =""):
        self.os:str = os
        self.port_number :str= port_number
        self.ip_address :str= ip_address
        self.username :str= username
        self.password :str= password

        self.command_list :list= command_list
        self.save_dir :str=save_dir
    def _create_session(self) -> ConnectHandler:

        machine_info = {
            "device_type": self.os,
            "ip": self.ip_address,
            "username": self.username,
            "password": self.password,
            "port": self.port_number,
        }
        # 機器の情報を元にセッションを確立する
        connection = ConnectHandler(**machine_info)
        return connection

    def _string_conversion_for_file_names(self,command:str) -> str:
        target_char_list:list = ["\\","/",":","*","?","\"","<",">","|"," ","　"]
        # 取得した文字列からファイル、フォルダー名に使用できない文字列を_に置換する
        for data in target_char_list:
            command = command.replace(data,"_")


        return command

    def _create_log_file(self,command,target_text:str):
        # コマンドをファイル名にそのまま使用する為、使用できない文字列をパースする。
        command = self._string_conversion_for_file_names(command)
        with open(file=f"{self.save_dir}{command}",mode="w",encoding="UTF-8") as file_dir:
            file_dir.write(target_text)

    def _enter_command(self,connection,command) -> str:
        # コマンドを入力しlogを取得する
        result_log = connection.send_command(command)
        self._create_log_file(command = command,target_text=result_log)

        return result_log

    def _debug_enter_command(self,command) -> str:
        # コマンドを入力しlogを取得する
        result_log = "test_log"
        self._create_log_file(command=command, target_text=result_log)

        return result_log

    def main_trigger(self):
        session = self._create_session()
        for command in self.command_list:
            self._enter_command(connection=session,command=command)

        session.disconnect()

    def debug_main_trigger(self):
        for command in self.command_list:
            self._debug_enter_command(command=command)


    def desplay_configuration(self):
        print(self.os,self.ip_address,self.port_number)
        print(self.username,self.password)
        print(self.command_list)
        print(self.save_dir)


class Setup(): # 基幹システムの構築に必要な変数を代入する

    def __init__(self):
        _yaml_controller = ExternalFileController()
        SystemConfiguration.machine_information_yaml = _yaml_controller.laod_yaml(r'.\machine_information.yaml')
        SystemConfiguration.unique_configuration_yaml = _yaml_controller.laod_yaml(r'.\unique_configuration.yaml')
        SystemConfiguration.id_yaml = _yaml_controller.laod_yaml(r'.\id.yaml')


class SystemConfiguration(): # 基幹システムの構築に必要な変数を宣言する
    machine_information_yaml: dict = {}
    unique_configuration_yaml: dict = {}
    target_preset_yaml: dict = {}
    id_yaml: dict = {}

    putting_directory_yaml: dict = {}


class ExternalFileController():# 外部ファイルを扱う処理を管理

    # ディレクトリの情報を元にyamlファイルを読み込む
    def laod_yaml(self,dir_info:str = "") -> dict:
        with open(file=dir_info, encoding='utf-8',mode="r") as yaml_file:
            return yaml.safe_load(yaml_file)

    def update_yaml(self,dir_info:str = "",input_dict:dict = {}):
        with open(file=dir_info, encoding='utf-8',mode="w") as yaml_file:
            yaml.dump(input_dict,
                      yaml_file,
                      default_flow_style=False,
                      allow_unicode=True)


if __name__ == "__main__":
    Setup()
    # ログの取得に必要なインスタンスを格納
    nw_instance:list = []

    # 保存先のディレクトリを作成
    os.mkdir(f"{SystemConfiguration.unique_configuration_yaml["directory_log_stored"]}{SystemConfiguration.id_yaml["log_file_id"]}/")


    try:
        for preset_name in SystemConfiguration.machine_information_yaml:
            os.mkdir(f"{SystemConfiguration.unique_configuration_yaml["directory_log_stored"]}{SystemConfiguration.id_yaml["log_file_id"]}/{preset_name}/")
            auth_type = SystemConfiguration.machine_information_yaml[preset_name]["Authentication"]

            nw_instance.append(
                CollectNetworkMachineInfo(
                    os=SystemConfiguration.machine_information_yaml[preset_name]["os"],
                    ip_address=SystemConfiguration.machine_information_yaml[preset_name]["ip_address"],
                    command_list=SystemConfiguration.machine_information_yaml[preset_name]["command"],
                    username=SystemConfiguration.unique_configuration_yaml["Authentication_list"][auth_type]["username"],
                    password=SystemConfiguration.unique_configuration_yaml["Authentication_list"][auth_type]["password"],
                    save_dir=f"{SystemConfiguration.unique_configuration_yaml["directory_log_stored"]}{SystemConfiguration.id_yaml["log_file_id"]}/{preset_name}/"
                )
            )

        for data in nw_instance:
            data.desplay_configuration()
            data.debug_main_trigger()

        _yaml_controller = ExternalFileController()
        SystemConfiguration.id_yaml["log_file_id"] += 1
        _yaml_controller.update_yaml(r'.\id.yaml',SystemConfiguration.id_yaml)

    except:
        _yaml_controller = ExternalFileController()
        SystemConfiguration.id_yaml["log_file_id"] += 1
        _yaml_controller.update_yaml(r'.\id.yaml',SystemConfiguration.id_yaml)


