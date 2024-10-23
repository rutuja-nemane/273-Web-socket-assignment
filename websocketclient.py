import websocket
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

# WebSocket client function
class WebSocketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WebSocket Client")

        self.text_area = scrolledtext.ScrolledText(root, width=50, height=20)
        self.text_area.pack()

        self.start_button = tk.Button(root, text="Start WebSocket", command=self.start_websocket)
        self.start_button.pack()

        self.message_count = 0  # To track the number of messages

    def start_websocket(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp("ws://localhost:8765/",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open  # Correctly pass the on_open function reference
        threading.Thread(target=ws.run_forever).start()

    def on_message(self, ws, message):
        self.message_count += 1
        self.display_message(message)

        # Print to client console
        print(f"Received message: {message}")

        # When the last message is received, display total count
        if self.message_count == 1000:
            self.display_message(f"\nTotal messages received: {self.message_count}")
            print(f"\nTotal messages received: {self.message_count}")  # Print total count to client console

    def on_error(self, ws, error):
        print(error)

    # Modify on_close to accept all four arguments
    def on_close(self, ws, close_status_code, close_msg):
        print("### WebSocket closed ###")
        print(f"Status code: {close_status_code}, Message: {close_msg}")

    def on_open(self, ws):  # Ensure this method accepts the 'ws' argument
        def run():
            for i in range(1000):
                # Sending a message 1000 times
                message = f"Message {i}"
                ws.send(message)
                time.sleep(0.01)  # Slight delay to avoid flooding
            ws.close()

        threading.Thread(target=run).start()

    def display_message(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)


# GUI setup
root = tk.Tk()
app = WebSocketApp(root)
root.mainloop()
