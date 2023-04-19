from time import sleep
from core.utilities.utilities import Utilities
import pyautogui

class OSUtility(object):
    
    def handle_download_file_IE(self, downloaded_file_path):
        """
        @summary: handle download file on IE 
        @param downloaded_file_path: path of download file 
        @return: True if download file exists / False if download file does not exist
        @author: Tham Nguyen
        @created_date: August 17, 2016
        """
        Utilities.delete_file(downloaded_file_path)
        sleep(1)
        
        pyautogui.hotkey('alt', 'n')
        sleep(2)
        pyautogui.keyDown('tab')
        pyautogui.keyUp('tab')
        sleep(2)
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
        sleep(2)
        pyautogui.keyDown('down')
        pyautogui.keyUp('down') # select Save As
        sleep(2)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter') # Enter
        sleep(3)
        pyautogui.typewrite(downloaded_file_path+'\n')
        sleep(2)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter') # Enter
        sleep(3)   
        
        Utilities.wait_for_file_is_downloaded(downloaded_file_path)
        
        pyautogui.keyDown('alt')
        pyautogui.keyDown('q')
        pyautogui.keyUp('q')
        pyautogui.keyUp('alt') # close notification bar
        
        return Utilities.does_file_existed(downloaded_file_path)
    
    
    def handle_download_file_Edge(self, downloaded_file_path):
        """
        @summary: handle download file on Edge
        @param downloaded_file_path: path of download file 
        @return: True if download file exists / False if download file does not exist
        @author: Tham Nguyen
        @created_date: August 17, 2016
        """
        Utilities.delete_file(downloaded_file_path)
        sleep(1)
        
        pyautogui.hotkey('alt', 'n')
        sleep(2)
        pyautogui.keyDown('tab')
        pyautogui.keyUp('tab')
        sleep(2)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter') # Enter
        sleep(3)
        pyautogui.typewrite(downloaded_file_path)
        sleep(2)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter') # Enter
        sleep(3)   
        
        Utilities.wait_for_file_is_downloaded(downloaded_file_path)
        
        pyautogui.keyDown('alt')
        pyautogui.keyDown('q')
        pyautogui.keyUp('q')
        pyautogui.keyUp('alt') # close notification bar
        
        return Utilities.does_file_existed(downloaded_file_path)
    
    
    def handle_download_file_FF(self, downloaded_file_path):
        """
        @summary: handle download file on Firefox
        @param downloaded_file_path: path of download file 
        @return: True if download file exists / False if download file does not exist
        @author: Tham Nguyen
        @created_date: August 17, 2016
        """
        Utilities.delete_file(downloaded_file_path)
                
        sleep(4)        
        pyautogui.keyDown('left')
        pyautogui.keyUp('left')
        sleep(2)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        sleep(2)        
        
        #Should wait for .exe file NOT .exe.part file  
        Utilities.wait_for_file_is_downloaded(downloaded_file_path)

        return Utilities.does_file_existed(downloaded_file_path)  
    
    
    def wait_for_notification_bar_displayed(self):
        sleep(3) # update later


