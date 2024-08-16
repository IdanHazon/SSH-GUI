import tkinter as tk
from pynput.keyboard import Key, Listener
import paramiko
import time
HOST = "<YOUR-IP-ADDR>"
USERNAME = "<USERNAME>"
PASSWORD = "<PASSWORD>"

def send_action(action, client):
    """
    The function gets the command as string and the client object.
    It initiates the command in the remote machine and updates the information.

    Args:
        action => string, represents the user's input
        client => paramico object of the connection
    
    Returns:
        _stdout => the output of the succesful command
        stderr_content => the error of the unsuccesful command
    """

    _stdin, _stdout,_stderr = client.exec_command(action)

    # Read the content of stderr
    stderr_content = _stderr.read().decode()

    # Check if there is any error and return it
    if stderr_content:
        return stderr_content
    else:
        return _stdout.read().decode()


def on_press(key, textbox, client):
    """
    The function is triggred when the user clicks on the keyboard.
    When the user clicks on the enter button it will call the function
    that sends the data to the remote machine.

    Args:
        key => the key that was clicked
    
    Returns:
        None
    """

    # Checks if the user clicked on Enter
    if key == Key.enter:
        
        # Get the number of lines in the Text widget
        num_lines = int(textbox.index('end-1c').split('.')[0])
        
        # Get the last line using the line number
        last_line = textbox.get(f"{num_lines}.0", f"{num_lines}.end")
        last_line = last_line.replace("[User@Centos7 ~]$ ", "")

        output = send_action(last_line, client)

        time.sleep(0.1)
        textbox.insert(tk.END, output)
        textbox.insert(tk.END, "[User@Centos7 ~]$ ")


def connect_to_machine():
    """
    
    """

    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USERNAME, password=PASSWORD)
    return client


def main():

    client = connect_to_machine()
    window = tk.Tk()
    window.geometry("750x500")
    textbox = tk.Text(window, height = 500, width = 750, background="black", fg="white", font=(10))
    textbox.insert(1.0, "[User@Centos7 ~]$ ")
    textbox.pack()
    listener = Listener(on_press=lambda key: on_press(key, textbox, client))
    listener.start()



    window.mainloop()


if __name__ == '__main__':
    main()
