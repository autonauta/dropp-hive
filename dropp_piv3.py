import tkinter as tk
from PIL import ImageTk, Image
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import time
import json
#from gpiozero import LED


# Load .env variables
load_dotenv()
HIVE_ID = os.getenv("HIVE_ID")
BROKER = os.getenv("BROKER")
BROKER_PORT = int(os.getenv("BROKER_PORT"))
BROKER_USER = os.getenv("BROKER_USER")
BROKER_PASSWORD = os.getenv("BROKER_PASSWORD")
SUB_TOPIC = "pinhives/" + HIVE_ID
PUB_TOPIC = "api/LATAM"
COURIER_SELECTED = ""
PHONE_NUMBER = ""
SIZE_SELECTED = ""
LOCKER_SET = ""
#lock1 = LED(17)
#lock2 = LED(27)

# MQTT CLIENT SETTINGS
client = mqtt.Client(HIVE_ID, clean_session=True, transport="tcp")
client.username_pw_set(username=BROKER_USER, password=BROKER_PASSWORD)


# Function that defines the actions when connected to BROKER


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(SUB_TOPIC)

# Function that send delivery request to server


def send_delivery(courier, phone, size):
    global HIVE_ID
    DELIVERY_MESSAGE = json.dumps({"hive_id": "{}".format(HIVE_ID), "courier": "{}".format(courier),
                                   "phone":  "{}".format(phone), "size": "{}".format(size)})
    client.publish(PUB_TOPIC, DELIVERY_MESSAGE)

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    global time_label, PHONE_NUMBER
    print("Message arrived from server")
    payload = json.loads(msg.payload)
    message = payload["message"]
    user_phone = payload["user_phone"]
    user_name = payload["user_name"]
    print(message)
    if message == "response":
        if user_phone == PHONE_NUMBER:
            Confirmation_label_text.set("USER: " + user_name)
            Confirmation_label2_text.set("PHONE: " + user_phone)
            Confirmation_label3_text.set("LOCKER: " + "locker 1")
            Confirmation_label.grid(columnspan=5, rowspan=1, column=2, row=3)
            Confirmation_label2.grid(columnspan=5, rowspan=1, column=2, row=4)
            Confirmation_label3.grid(columnspan=5, rowspan=1, column=2, row=5)
            Confirmation_label3.after(5000, back_original_state)
        else:
            Confirmation_label_text.set("USER: " + "doesnt exist")
            Confirmation_label2_text.set("PHONE: " + "0")
            Confirmation_label3_text.set("LOCKER: " + "0")
            Confirmation_label.grid(columnspan=5, rowspan=1, column=2, row=3)
            Confirmation_label2.grid(columnspan=5, rowspan=1, column=2, row=4)
            Confirmation_label3.grid(columnspan=5, rowspan=1, column=2, row=5)
            Confirmation_label3.after(5000, back_original_state)


client.connect(BROKER, BROKER_PORT, keepalive=3600)

client.on_connect = on_connect
client.on_message = on_message

App_state = 0


# Function of Delivery button


def delivery_clicked():
    Button_delivery.grid_forget()
    Button_pickup.grid_forget()
    Button_estafeta.grid(columnspan=2, rowspan=2, column=0, row=3)
    Button_dhl.grid(columnspan=2, rowspan=2, column=2, row=3)
    Button_ups.grid(columnspan=2, rowspan=2, column=4, row=3)
    Button_other.grid(columnspan=2, rowspan=2, column=6, row=3)

    Button_back.grid(columnspan=2, column=0, row=7)
    global App_state
    App_state = 1


def pickup_clicked():
    Button_delivery.grid_forget()
    Button_pickup.grid_forget()

    Button_back.grid(columnspan=2, column=0, row=7)
    global App_state
    App_state = 1


def courier_selected(courier):
    global App_state
    global COURIER_SELECTED
    COURIER_SELECTED = courier
    Button_estafeta.grid_forget()
    Button_dhl.grid_forget()
    Button_ups.grid_forget()
    Button_other.grid_forget()
    Phone_entry.grid(columnspan=4, rowspan=2, column=1, row=3)
    Button_1.grid(columnspan=2, rowspan=1, column=5, row=2)
    Button_2.grid(columnspan=2, rowspan=1, column=6, row=2)
    Button_3.grid(columnspan=2, rowspan=1, column=7, row=2)
    Button_4.grid(columnspan=2, rowspan=1, column=5, row=4)
    Button_5.grid(columnspan=2, rowspan=1, column=6, row=4)
    Button_6.grid(columnspan=2, rowspan=1, column=7, row=4)
    Button_7.grid(columnspan=2, rowspan=1, column=5, row=6)
    Button_8.grid(columnspan=2, rowspan=1, column=6, row=6)
    Button_9.grid(columnspan=2, rowspan=1, column=7, row=6)
    Button_0.grid(columnspan=2, rowspan=1, column=6, row=7)
    Button_clear.grid(columnspan=2, rowspan=1, column=7, row=7)
    Button_OK.grid(columnspan=2, rowspan=1, column=5, row=7)
    App_state = 2


def response_label_off():
    Response_label.grid_forget()


def button_ok():
    global PHONE_NUMBER
    PHONE_NUMBER = Phone_entry.get()
    if len(PHONE_NUMBER) <= 0:
        print("No se intrdujo ningun numero")
        Response_label_text.set("Can't be empty")
        Response_label.grid(columnspan=3, rowspan=2, column=1, row=5)
        Response_label.after(3000, response_label_off)
    elif len(PHONE_NUMBER) < 10 or len(PHONE_NUMBER) > 10:
        print("menor o mayor a 10")
        Response_label_text.set("Enter 10 digits number")
        Response_label.grid(columnspan=3, rowspan=2, column=1, row=5)
        Response_label.after(3000, response_label_off)
    elif len(PHONE_NUMBER) == 10:
        Phone_entry.delete(0, 'end')

        Button_1.grid_forget()
        Button_2.grid_forget()
        Button_3.grid_forget()
        Button_4.grid_forget()
        Button_5.grid_forget()
        Button_6.grid_forget()
        Button_7.grid_forget()
        Button_8.grid_forget()
        Button_9.grid_forget()
        Button_0.grid_forget()
        Button_clear.grid_forget()
        Button_OK.grid_forget()
        Phone_entry.grid_forget()

        Button_small.grid(columnspan=3, rowspan=3, column=1, row=2)
        Button_big.grid(columnspan=3, rowspan=3, column=5, row=2)

        App_state = 3


def button_click(button):
    global PHONE_NUMBER
    global App_state
    if button == "clear":
        Phone_entry.delete(0, 'end')
    else:
        current = Phone_entry.get()
        Phone_entry.delete(0, 'end')
        Phone_entry.insert(0, str(current) + str(button))


def back_original_state():
    global App_state, PHONE_NUMBER
    PHONE_NUMBER = ""
    Confirmation_label.grid_forget()
    Confirmation_label2.grid_forget()
    Confirmation_label3.grid_forget()
    Button_delivery.grid(columnspan=3, rowspan=3, column=1, row=2)
    Button_pickup.grid(columnspan=3, rowspan=3, column=5, row=2)
    App_state = 0


def size_select(size):
    global SIZE_SELECTED, COURIER_SELECTED, PHONE_NUMBER, LOCKER_SET, App_state
    if size == "s":
        SIZE_SELECTED = "s"
    elif size == "b":
        SIZE_SELECTED = "b"
    send_delivery(COURIER_SELECTED, PHONE_NUMBER, SIZE_SELECTED)
    Button_back.grid_forget()
    Button_small.grid_forget()
    Button_big.grid_forget()


def back(state):
    global App_state
    if state == 1:
        Button_estafeta.grid_forget()
        Button_dhl.grid_forget()
        Button_ups.grid_forget()
        Button_other.grid_forget()
        Button_back.grid_forget()
        Button_delivery.grid(columnspan=3, rowspan=3, column=1, row=2)
        Button_pickup.grid(columnspan=3, rowspan=3, column=5, row=2)

        App_state = 0

    elif state == 2:
        Button_1.grid_forget()
        Button_2.grid_forget()
        Button_3.grid_forget()
        Button_4.grid_forget()
        Button_5.grid_forget()
        Button_6.grid_forget()
        Button_7.grid_forget()
        Button_8.grid_forget()
        Button_9.grid_forget()
        Button_0.grid_forget()
        Button_clear.grid_forget()
        Button_OK.grid_forget()
        Phone_entry.delete(0, 'end')
        Phone_entry.grid_forget()

        Button_estafeta.grid(columnspan=2, rowspan=2, column=0, row=3)
        Button_dhl.grid(columnspan=2, rowspan=2, column=2, row=3)
        Button_ups.grid(columnspan=2, rowspan=2, column=4, row=3)
        Button_other.grid(columnspan=2, rowspan=2, column=6, row=3)

        App_state = 1

    elif state == 3:
        Button_small.grid_forget()
        Button_big.grid_forget()

        Phone_entry.grid(columnspan=4, rowspan=2, column=1, row=3)
        Button_1.grid(columnspan=2, rowspan=1, column=5, row=2)
        Button_2.grid(columnspan=2, rowspan=1, column=6, row=2)
        Button_3.grid(columnspan=2, rowspan=1, column=7, row=2)
        Button_4.grid(columnspan=2, rowspan=1, column=5, row=4)
        Button_5.grid(columnspan=2, rowspan=1, column=6, row=4)
        Button_6.grid(columnspan=2, rowspan=1, column=7, row=4)
        Button_7.grid(columnspan=2, rowspan=1, column=5, row=6)
        Button_8.grid(columnspan=2, rowspan=1, column=6, row=6)
        Button_9.grid(columnspan=2, rowspan=1, column=7, row=6)
        Button_0.grid(columnspan=2, rowspan=1, column=6, row=7)
        Button_clear.grid(columnspan=2, rowspan=1, column=7, row=7)
        Button_OK.grid(columnspan=2, rowspan=1, column=5, row=7)

        App_state = 2


# Functions of screens
# START OF GUI -----------------------------------------------------------------------------------
# GUI Definition and settings
root = tk.Tk()
root.title("Dropp")
root.attributes('-fullscreen', True)


canvas1 = tk.Canvas(root, width=800, height=480,
                    bg="#1f4c7d", highlightthickness=1)
canvas1.grid(columnspan=9, rowspan=8)
# Set Logo
logo = ImageTk.PhotoImage(Image.open('./img/logo_w.png'))
logo_label = tk.Label(image=logo, bg='#1f4c7d')
logo_label.image = logo

# Set loading Label
loading_label = tk.Label(text="LOADING...", fg="white",
                         bg="#1f4c7d", font=("Raleway", 40))

# Set time Label
time_label = tk.Label(text="12:00",
                      height=1, fg="white", bg="#1f4c7d", font=("Raleway", 25))

# Set response label
Response_label_text = tk.StringVar()
Response_label = tk.Label(textvariable=Response_label_text, fg="red",
                          bg="#1f4c7d", font=("Raleway", 15))
Response_label_text.set("PRUEBA")
# Confirmation label
Confirmation_label_text = tk.StringVar()
Confirmation_label = tk.Label(textvariable=Confirmation_label_text, fg="white",
                              bg="#1f4c7d", font=("Raleway", 20))

Confirmation_label2_text = tk.StringVar()
Confirmation_label2 = tk.Label(textvariable=Confirmation_label2_text, fg="white",
                               bg="#1f4c7d", font=("Raleway", 20))

Confirmation_label3_text = tk.StringVar()
Confirmation_label3 = tk.Label(textvariable=Confirmation_label3_text, fg="white",
                               bg="#1f4c7d", font=("Raleway", 20))

# Set main buttons
Button_delivery_text = tk.StringVar()
Button_delivery = tk.Button(root, width="20", height="4",
                            textvariable=Button_delivery_text, bg="#e57655", fg="white", font=("Raleway", 20), command=lambda: delivery_clicked())
Button_delivery_text.set("Delivery")

Button_pickup_text = tk.StringVar()
Button_pickup = tk.Button(root, width="20", height="4",
                          textvariable=Button_pickup_text, bg="#e57655", fg="white", font=("Raleway", 20), command=lambda: pickup_clicked())
Button_pickup_text.set("Pickup")

# Set courier buttons
Button_estafeta_text = tk.StringVar()
Button_estafeta = tk.Button(root, width="10", height="3",
                            textvariable=Button_estafeta_text, bg="#e57655", fg="#1f4c7d", font=("Raleway", 10), command=lambda: courier_selected("estafeta"))
Button_estafeta_text.set("Estafeta")
Button_dhl_text = tk.StringVar()
Button_dhl = tk.Button(root, width="10", height="3", textvariable=Button_dhl_text,
                       bg="#e57655", fg="#1f4c7d", font=("Raleway", 10), command=lambda: courier_selected("dhl"))
Button_dhl_text.set("DHL")
Button_ups_text = tk.StringVar()
Button_ups = tk.Button(root, width="10", height="3", textvariable=Button_ups_text,
                       bg="#e57655", fg="#1f4c7d", font=("Raleway", 10), command=lambda: courier_selected("ups"))
Button_ups_text.set("UPS")
Button_other_text = tk.StringVar()
Button_other = tk.Button(root, width="10", height="3", textvariable=Button_other_text,
                         bg="#e57655", fg="#1f4c7d", font=("Raleway", 10), command=lambda: courier_selected("other"))
Button_other_text.set("OTHER")
# Set navigation buttons
Button_back_text = tk.StringVar()
Button_back = tk.Button(root, width="10", height="3", textvariable=Button_back_text,
                        bg="#1f4c7d", fg="white", font=("Raleway", 8), command=lambda: back(App_state))
Button_back_text.set("<< Regresar")

Button_1 = tk.Button(root, text=1, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("1"))
Button_2 = tk.Button(root, text=2, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("2"))
Button_3 = tk.Button(root, text=3, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("3"))
Button_4 = tk.Button(root, text=4, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("4"))
Button_5 = tk.Button(root, text=5, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("5"))
Button_6 = tk.Button(root, text=6, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("6"))
Button_7 = tk.Button(root, text=7, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("7"))
Button_8 = tk.Button(root, text=8, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("8"))
Button_9 = tk.Button(root, text=9, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("9"))
Button_0 = tk.Button(root, text=0, width="5", height="2",
                     bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("0"))
Button_clear = tk.Button(root, text="DEL", width="5", height="2",
                         bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_click("clear"))
Button_OK = tk.Button(root, text="OK", width="5", height="2",
                      bg="#1f4c7d", fg="#e57655", font=("Raleway", 20), command=lambda: button_ok())

Phone_entry = tk.Entry(root, width=20, borderwidth=1,
                       bg="#e57655", fg="#1f4c7d", font=("Raleway", 20))

Button_small = tk.Button(root, width="20", height="4",
                         text="small", bg="#e57655", fg="white", font=("Raleway", 20), command=lambda: size_select("s"))
Button_big = tk.Button(root, width="20", height="4",
                       text="big", bg="#e57655", fg="white", font=("Raleway", 20), command=lambda: size_select("b"))

# Display logo on screen
logo_label.grid(columnspan=3, column=0, row=0)
# Dsiplay time Label on screen
time_label.grid(columnspan=2, column=7, row=0)
Button_delivery.grid(columnspan=3, rowspan=3, column=1, row=2)
Button_pickup.grid(columnspan=3, rowspan=3, column=5, row=2)


client.loop_start()
root.mainloop()
