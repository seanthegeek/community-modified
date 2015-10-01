from lib.cuckoo.common.abstracts import Signature

class PowershellCommand(Signature):
    name = "powershell_command"
    description = "Attempts to execute a powershell command with suspicious parameter/s"
    severity = 2
    confidence = 70
    weight = 0
    categories = ["generic"]
    authors = ["Kevin Ross"]
    minimum = "1.2"
    evented = True

    def __init__(self, *args, **kwargs):
        Signature.__init__(self, *args, **kwargs)

    filter_apinames = set(["CreateProcessInternalW","ShellExecuteExW"])

    def on_call(self, call, process):
        if call["api"] == "CreateProcessInternalW":
            cmdline = self.get_argument(call, "CommandLine").lower()
            if "powershell.exe" in cmdline and "bypass" in cmdline:
                self.data.append({"execution_policy" : "Attempts to bypass execution policy"})
                self.severity = 3
                self.weight += 1
        elif call["api"] == "ShellExecuteExW":
            filepath = self.get_argument(call, "FilePath").lower()
            params = self.get_argument(call, "Parameters").lower()
            if "powershell.exe" in filepath and "bypass" in params:
                self.data.append({"execution_policy" : "Attempts to bypass execution policy"})
                self.severity = 3
                self.weight += 1

        if call["api"] == "CreateProcessInternalW":
            cmdline = self.get_argument(call, "CommandLine").lower()
            if "powershell.exe" in cmdline and "-nop" in cmdline:
                self.data.append({"user_profile" : "Does not load current user profile"})
                self.severity = 3
                self.weight += 1
        elif call["api"] == "ShellExecuteExW":
            filepath = self.get_argument(call, "FilePath").lower()
            params = self.get_argument(call, "Parameters").lower()
            if "powershell.exe" in filepath and "-nop" in params:
                self.data.append({"user_profile" : "Does not load current user profile"})
                self.severity = 3
                self.weight += 1

        if call["api"] == "CreateProcessInternalW":
            cmdline = self.get_argument(call, "CommandLine").lower()
            if "powershell.exe" in cmdline and "-w" in cmdline and "hidden" in cmdline:
                self.data.append({"hidden_window" : "Attempts to execute command with a hidden window"})
                self.weight += 1
        elif call["api"] == "ShellExecuteExW":
            filepath = self.get_argument(call, "FilePath").lower()
            params = self.get_argument(call, "Parameters").lower()
            if "powershell.exe" in filepath and "-w" in params and "hidden" in params:
                self.data.append({"hidden_window" : "Attempts to execute command with a hidden window"})
                self.weight += 1

        if call["api"] == "CreateProcessInternalW":
            cmdline = self.get_argument(call, "CommandLine").lower()
            if "powershell.exe" in cmdline and "-enc" in cmdline:
                self.data.append({"b64_encoded" : "Uses a Base64 encoded command value"})
                self.weight += 1
        elif call["api"] == "ShellExecuteExW":
            filepath = self.get_argument(call, "FilePath").lower()
            params = self.get_argument(call, "Parameters").lower()
            if "powershell.exe" in filepath and "-enc" in params:
                self.data.append({"b64_encoded" : "Uses a Base64 encoded command value"})
                self.weight += 1

        if self.weight:
            return True
        return False
