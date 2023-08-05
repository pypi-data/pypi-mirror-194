import pyautogui
import keyboard

class HappyDataScientist:
    def __init__(self):
        pass

    # Program status
    programStatus = 0

    @staticmethod
    def __on_press(key):
        print(key.name)
        keyboard.unhook_all()  # Stop listening to keyboard
        HappyDataScientist.programStatus = 1

    @staticmethod
    def startworking():
        """
        Your mouse will start to draw rectangle on the screen automatically. Press any key to stop.

        Parameters:
        -----------
        None

        Returns:
        -----------
        None

        """
        print('Press any key to stop working')
        screen_width, screen_height = pyautogui.size()
        center_x = round(screen_width / 2)
        center_y = round(screen_height / 2)
        pointA = (center_x - 100, center_y - 100)
        pointB = (center_x + 100, center_y - 100)
        pointC = (center_x + 100, center_y + 100)
        pointD = (center_x - 100, center_y + 100)

        # Actively listing to the keyboard
        keyboard.on_press(HappyDataScientist.__on_press)

        n = 1
        while True:
            if HappyDataScientist.programStatus == 1:
                break
            if n == 1:
                start_x, start_y = pointA[0], pointA[1]
                end_x, end_y = pointB[0], pointB[1]
            elif n == 2:
                start_x, start_y = pointB[0], pointB[1]
                end_x, end_y = pointC[0], pointC[1]
            elif n == 3:
                start_x, start_y = pointC[0], pointC[1]
                end_x, end_y = pointD[0], pointD[1]
            else:
                start_x, start_y = pointD[0], pointD[1]
                end_x, end_y = pointA[0], pointA[1]
            # Move the cursor
            pyautogui.moveTo(start_x, start_y)
            pyautogui.moveTo(end_x, end_y, duration=1.5)
            n = (n + 1) % 4








