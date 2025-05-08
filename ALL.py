from djitellopy import Tello
import time
import os
from PIL import Image

#Директория
if not os.path.exists('tello_photos'):
    os.makedirs('tello_photos')

# Инициализация на дрона
tello = Tello()
tello.connect()

# Батерия
print(f"Battery: {tello.get_battery()}%")

#Старт на Стрийм
tello.streamon()

# Полита
tello.takeoff()
time.sleep(2)

try:
    # Параметри на движение
    move_distance = 20  # 20 cm
    total_horizontal_distance = 200  # 2 meters = 200 cm

    #Брояч на снимки
    photo_counter = 0


    for i in range(int(total_horizontal_distance / move_distance) + 1):
        # Hover completely
        tello.send_rc_control(0, 0, 0, 0)
        time.sleep(0.5)  # Stabilize hover

        # Снимка
        frame = tello.get_frame_read().frame
        img = Image.fromarray(frame)

        # Генерира име на снимка
        photo_counter += 1
        filename = f"tello_left_{photo_counter}.jpg"
        full_path = os.path.join('tello_photos', filename)

        # Запазва снимка
        img.save(full_path)
        print(f"Saved picture {photo_counter}: {full_path}")


        if i < int(total_horizontal_distance / move_distance):
            tello.move_left(move_distance)
            time.sleep(1)




    for i in range(int(total_horizontal_distance / move_distance) + 1):
        tello.send_rc_control(0, 0, 0, 0)
        time.sleep(0.5)

        frame = tello.get_frame_read().frame
        img = Image.fromarray(frame)

        photo_counter += 1
        filename = f"tello_right_{photo_counter}.jpg"
        full_path = os.path.join('tello_photos', filename)

        img.save(full_path)
        print(f"Saved picture {photo_counter}: {full_path}")

        if i < int(total_horizontal_distance / move_distance):
            tello.move_right(move_distance)
            time.sleep(1)

    print(f"Successfully captured {photo_counter} pictures!")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Приземява
    tello.land()
    tello.streamoff()
    print("Flight completed")