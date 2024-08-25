from netmiko import ConnectHandler







class NetworkController:
    def create_session(self,port: str,os: str,ip_address: str,username: str,password: str) -> dict:

        machine_info = {
            "device_type": os,
            "ip": ip_address,
            "username": username,
            "password": password,
            "port": port,
        }
        # 機器の情報を元にセッションを確立する
        connection = ConnectHandler(**machine_info)
        return connection

    def enter_command(self,connection,command):
        # コマンドを入力しlogを取得する
        result_log = connection.send_command(command)
