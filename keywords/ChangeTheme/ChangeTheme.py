from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import subprocess
import time

class ChangeTheme:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self._builtin = BuiltIn()
        self.device_udid = "a83af8e7"  # Mesmo UDID do seu código original

    @property
    def appium(self):
        return self._builtin.get_library_instance("AppiumLibrary")

    def _execute_adb_command(self, command):
        """Executa comando ADB e retorna o resultado"""
        try:
            full_command = f"adb -s {self.device_udid} {command}"
            result = subprocess.run(
                full_command.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                self._builtin.log(f"Comando ADB executado: {full_command}", "INFO")
                return True, result.stdout.strip()
            else:
                self._builtin.log(f"Erro no comando ADB: {result.stderr}", "ERROR")
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            self._builtin.log(f"Timeout no comando ADB: {command}", "ERROR")
            return False, "Timeout"
        except Exception as e:
            self._builtin.log(f"Erro ao executar comando ADB: {str(e)}", "ERROR")
            return False, str(e)

    def _get_current_theme(self):
        """Tenta deduzir o tema atual usando getprop + settings"""
        success, output = self._execute_adb_command("shell settings get secure ui_night_mode")
        if success:
            return output.strip()
        return None

    def _set_theme_via_adb(self, mode):
        """Define o tema usando comandos ADB

        Args:
            mode (str): "dark" para tema escuro, "light" para tema claro
        """
        cmd_value = "yes" if mode == "dark" else "no"
        command = f"shell cmd uimode night {cmd_value}"
        success, output = self._execute_adb_command(command)

        if not success:
            raise RuntimeError(f"Falha ao definir tema {mode}: {output}")

        self._builtin.log(f"Tema {mode} aplicado via 'cmd uimode'", "INFO")
        time.sleep(1)
        return True

    def _verify_theme_change(self, expected_mode):
        """Verifica se o tema foi alterado corretamente"""
        expected_values = {
            "dark": "2",
            "light": "1"
        }
        
        current_theme = self._get_current_theme()
        if current_theme == expected_values[expected_mode]:
            self._builtin.log(f"Tema {expected_mode} aplicado com sucesso (código: {current_theme})", "INFO")
            return True
        else:
            self._builtin.log(f"Tema não foi aplicado. Esperado: {expected_values[expected_mode]}, Atual: {current_theme}", "WARN")
            return False

    @keyword("Change To Dark Theme")
    def change_to_dark_theme(self, verify=True):
        """Muda para tema escuro usando ADB
        
        Args:
            verify (bool): Se True, verifica se a mudança foi aplicada
        """
        try:
            self._builtin.log("Iniciando mudança para tema escuro via ADB", "INFO")
            
            # Verifica tema atual
            current_theme = self._get_current_theme()
            self._builtin.log(f"Tema atual: {current_theme}", "INFO")
            
            # Se já estiver no tema escuro, não faz nada
            if current_theme == "2":
                self._builtin.log("Dispositivo já está no tema escuro", "INFO")
                return True
            
            # Aplica tema escuro
            self._set_theme_via_adb("dark")
            
            # Verifica se foi aplicado corretamente
            if verify:
                if not self._verify_theme_change("dark"):
                    raise RuntimeError("Tema escuro não foi aplicado corretamente")
            
            self._builtin.log("Tema escuro aplicado com sucesso", "INFO")
            return True
            
        except Exception as e:
            self._builtin.log(f"Erro ao mudar para tema escuro: {str(e)}", "ERROR")
            raise RuntimeError(f"Falha ao mudar para tema escuro: {str(e)}")

    @keyword("Change To Light Theme")
    def change_to_light_theme(self, verify=True):
        """Muda para tema claro usando ADB
        
        Args:
            verify (bool): Se True, verifica se a mudança foi aplicada
        """
        try:
            self._builtin.log("Iniciando mudança para tema claro via ADB", "INFO")
            
            # Verifica tema atual
            current_theme = self._get_current_theme()
            self._builtin.log(f"Tema atual: {current_theme}", "INFO")
            
            # Se já estiver no tema claro, não faz nada
            if current_theme == "1":
                self._builtin.log("Dispositivo já está no tema claro", "INFO")
                return True
            
            # Aplica tema claro
            self._set_theme_via_adb("light")
            
            # Verifica se foi aplicado corretamente
            if verify:
                if not self._verify_theme_change("light"):
                    raise RuntimeError("Tema claro não foi aplicado corretamente")
            
            self._builtin.log("Tema claro aplicado com sucesso", "INFO")
            return True
            
        except Exception as e:
            self._builtin.log(f"Erro ao mudar para tema claro: {str(e)}", "ERROR")
            raise RuntimeError(f"Falha ao mudar para tema claro: {str(e)}")

    @keyword("Get Current Theme")
    def get_current_theme(self):
        """Retorna o tema atual do sistema"""
        try:
            theme_code = self._get_current_theme()
            theme_map = {
                "0": "auto",
                "1": "light", 
                "2": "dark"
            }
            
            theme_name = theme_map.get(theme_code, "unknown")
            self._builtin.log(f"Tema atual: {theme_name} (código: {theme_code})", "INFO")
            return theme_name
            
        except Exception as e:
            self._builtin.log(f"Erro ao obter tema atual: {str(e)}", "ERROR")
            raise RuntimeError(f"Falha ao obter tema atual: {str(e)}")

    @keyword("Toggle Theme")
    def toggle_theme(self):
        """Alterna entre tema claro e escuro"""
        try:
            current_theme = self.get_current_theme()
            
            if current_theme == "dark":
                self.change_to_light_theme()
            elif current_theme == "light":
                self.change_to_dark_theme()
            else:
                # Se estiver em auto, define como escuro
                self.change_to_dark_theme()
                
            self._builtin.log("Tema alternado com sucesso", "INFO")
            return True
            
        except Exception as e:
            self._builtin.log(f"Erro ao alternar tema: {str(e)}", "ERROR")
            raise RuntimeError(f"Falha ao alternar tema: {str(e)}")

    @keyword("Reset Theme To Auto")
    def reset_theme_to_auto(self):
        """Reseta o tema para automático (modo padrão do sistema)"""
        try:
            self._builtin.log("Resetando tema para automático (modo auto)", "INFO")

            command = "shell settings put secure ui_night_mode 0"
            success, output = self._execute_adb_command(command)

            if not success:
                raise RuntimeError(f"Falha ao resetar tema: {output}")

            self._builtin.log("Tema resetado para automático com sucesso", "INFO")
            return True

        except Exception as e:
            self._builtin.log(f"Erro ao resetar tema: {str(e)}", "ERROR")
            raise RuntimeError(f"Falha ao resetar tema: {str(e)}")