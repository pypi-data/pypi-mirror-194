import os,sys
from PIL import Image
from PIL import ImageTk
import tkinter.font, tkinter.ttk
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import threading
import cv2
import traceback
import time 
from ftplib import FTP 
import configparser
import logging
import numpy as np

class Fk_viewer(object):
    
    def __init__(self,env):
        
        logging.basicConfig(filename="recoding_file/em.log",filemode='a',
                            level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt="%m/%d/%Y %I:%M:%S %p %Z")
        self.env=env.upper()
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')
        self.window = tk.Tk() 
        self.window.geometry(self.config[self.env]['GEOMETRY'])
        self.window.attributes("-fullscreen", True)
        self.window.bind("<F11>", lambda event: self.window.attributes("-fullscreen",
                                    not self.window.attributes("-fullscreen")))
        self.window.bind("<Escape>", lambda event: self.window.attributes("-fullscreen", False))
        self.window.title("EM_transfer:Suncom Co.,Ltd.") 
        # self.file_name=""
        # self.file_name_s=""
        # self.path_file_name=""
        # self.path_file_name_s=""
        self.path=self.config[self.env]['PATH']
        self.target_path=self.config[self.env]['TARGET_PATH']
        try:
            if self.env=="DEFAULT":
                self.view = cv2.VideoCapture(int(self.config[self.env]['VIDEOCAPTURE']))
            else:
                self.view = cv2.VideoCapture(self.config[self.env]['VIDEOCAPTURE'])
        except cv2.error as ex:
            logging.error(ex)
            time.sleep(5)
        w = round(self.view.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
        h = round(self.view.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height
        fps = self.view.get(cv2.CAP_PROP_FPS) #frame per second
        logging.info(f"Checking... for receivied IP camera info to being: ,{w},{h},{fps}")
        self.txt_idx=1
        # self.image=np.array([])
        self.out=None
        self.t_img=None
        self.thread_seq=None
        self.thread_file_trans=None
        self.file_exist=False
        self.out_set=None
        self.num=0

        self.entryText1 = tk.StringVar() 
        self.entryText2 = tk.StringVar()
        self.entryText3 = tk.StringVar()

        frame=tk.Frame(self.window)
        self.cframe=tk.Frame(self.window)
        frame1=tk.Frame(frame)
        frame2=tk.Frame(frame)
        frame3=tk.Frame(frame)
        frame4=tk.Frame(self.cframe)
        frame5=tk.Frame(frame)
        frame6=tk.Frame(frame)
        frame7=tk.Frame(frame)
  
        lfont = tkinter.font.Font(family="맑은 고딕", size=12 , weight = "bold")
        lfont1 = tkinter.font.Font(family="맑은 고딕", size=20 , weight = "bold")
        lfont2 = tkinter.font.Font(family="맑은 고딕", size=16 , weight = "bold")
        label1 = tk.Label(frame1, text = "  녹화시각    :  ", font = lfont)
        label2 = tk.Label(frame2, text = "  파일이름    :  ", font = lfont)
        label4 = tk.Label(frame6, text = "  이미지수신상태    :  ", font = lfont)
        label5 = tk.Label(frame7, text = "  이미지전송상태    :  ", font = lfont)
        self.cur_time = tk.Entry(frame1, textvariable = self.entryText1,width=30,font=lfont)
        self.entryText1.set('Recording does not start')
        self.f_name = tk.Entry(frame2, textvariable = self.entryText2,width=30,font=lfont)
        self.entryText2.set('Recording does not start')
          
        startingbtn = tk.Button(frame4, width=25,height=3, font=lfont2,text = "녹화시작", command = self.start_recoding)
        stopingbtn = tk.Button(frame4, width=25,height=3,font=lfont2,text = "녹화중지", command = self.stop_recoding_btn)
        self.label3 = tk.Label(self.cframe, text="녹화 준비 중", foreground="red",font=lfont1,compound="center")
        self.exe_text = scrolledtext.ScrolledText(master=frame3,width=60,height=12)  
        self.trans_text = scrolledtext.ScrolledText(master=frame5,width=60,height=12)  
        self.window.protocol("WM_DELETE_WINDOW", self.winclose)
          
        maginx = 10
        maginy = 10
  
        radx = 10
        rady = 5
          
        frame1.pack(anchor= "w", ipadx = maginx, ipady =maginy)
        frame2.pack(anchor= "w", ipadx = maginx, ipady =maginy)
        frame6.pack(anchor= "w", ipadx = maginx, ipady =maginy)
        frame3.pack(anchor= "w", ipadx = maginx, ipady =rady)
        frame7.pack(anchor= "w", ipadx = maginx, ipady =maginy)
        frame5.pack(anchor= "w", ipadx = maginx, ipady =rady)
        frame4.pack(side="bottom", ipadx = radx, ipady =maginy)
        
        self.cframe.pack(side="left", fill="both", expand=True)
        frame.pack(side="right", anchor= "n")
          
        self.label3.pack(side="top",anchor="w", fill = "both" , expand=True)
        
        label1.pack(side= "left" )       
        self.cur_time.pack(side= "left")
          
        label2.pack(side= "left")      
        self.f_name.pack(side= "left" )
        label4.pack(side= "left" )
        label5.pack(side= "left" )
        self.exe_text.pack(side= "left")
        self.trans_text.pack(side= "left")  
        startingbtn.pack(side= "left",  padx = 5, pady =5)
        stopingbtn.pack(side= "left",  padx = 5, pady =5)     
        self.tt=True
        if self.thread_file_trans is None or not self.thread_file_trans.is_alive():
            self.thread_file_trans=threading.Thread(target=self.file_conveyance, args=())
            self.thread_file_trans.daemon=True
            self.thread_file_trans.start()
        startingbtn.invoke()
        self.window.mainloop()
        
    def winclose(self):
        self.tt=False
        self.window.destroy()
  
    def start_recoding(self):
        self.tt=True
        if self.thread_seq is None or not self.thread_seq.is_alive():
            self.thread_on=True
            self.out_set=True
            self.thread_seq=threading.Thread(target=self.start_recoding1, args=())
            # self.thread_seq.daemon=True
            self.thread_seq.start()
        
        if self.thread_file_trans is None or not self.thread_file_trans.is_alive():
            self.thread_file_trans=threading.Thread(target=self.file_conveyance, args=())
            # self.thread_file_trans.daemon=True
            self.thread_file_trans.start()

    def start_recoding1(self):
        ii=0
        while True:
            if self.out_set==False:
                break
            time.sleep(1)
            if self.thread_on==False:
                break
            if self.out is None or not self.out.isOpened():
                if self.t_img is None or not self.t_img.is_alive():
                    logging.info(f"cnt: {ii+1}")
                    try:
                        if not self.view.isOpened():
                            if self.env=="DEFAULT":
                                self.view = cv2.VideoCapture(0)
                            else:
                                self.view = cv2.VideoCapture(self.config[self.env]['VIDEOCAPTURE'])
                    except cv2.error as ex:
                        logging.error(f'Traceback error: {ex},{traceback.print_exc()}')
                        # traceback.print_exc()
                    self.t_img = threading.Thread(target=self.sample_viewThread, args=())
                    # self.t_img.daemon =True
                    self.t_img.start()
                                
    def sample_viewThread(self):
        #print("txt_dix: ",txt_idx)
        fr =[]
        idx=1
        mbyte_cnt=0
        snap_freq = int(self.config[self.env]['SNAP_FREQ'])
        setting_frame_cnt=int(self.config[self.env]['SETTING_FRAME_CNT'])
        (file_name, file_name_s,path_file_name,path_file_name_s)=self.setting_file_name()
        
        w = round(self.view.get(cv2.CAP_PROP_FRAME_WIDTH)) # width
        h = round(self.view.get(cv2.CAP_PROP_FRAME_HEIGHT)) #height
        if self.config[self.env]['FPS']=="AUTO":
            fps = self.view.get(cv2.CAP_PROP_FPS) #frame per second
        else: fps = int(self.config[self.env]['FPS_SET']) 
        codec_tmp=self.config[self.env]['CODEC']
        fourcc = cv2.VideoWriter_fourcc(*codec_tmp) #fourcc
        delay = round(1000/fps)
        logging.info(f"{file_name} Checking... for going to be saved file")
            
        if not self.view.isOpened() and not self.out.isOpened():
            logging.error("Check to IP camera states or File isn't opend!!")
            self.stop_recoding_btn()
        try:
            if self.out is None or not self.out.isOpened():
                if not self.out is None:
                    self.out.release()
                self.out = cv2.VideoWriter(
                    filename=path_file_name,
                    fourcc=fourcc,
                    # apiPreference=cv2.CAP_FFMPEG,
                    fps=float(fps),
                    frameSize=(w, h),
                    isColor=True)#path_file_name, fourcc, fps, (w,h))
                # logging.error(self.out.isOpened())
        except cv2.error as ex:
            logging.exception(f'Traceback error: {ex}, {traceback.print_exc()}')
            
        try:
            while True:
                ret, fr = self.view.read()
                if not ret:
                    fr=[]
                    self.view.release()
                    self.out.release()
                    break
                if ret and idx <=setting_frame_cnt and self.out_set==True:#self.out.isOpened():
                    mbyte_cnt+=sys.getsizeof(fr)
                    exe_idx = float(self.exe_text.index("end"))-1
                    self.exe_text.delete(exe_idx,"end")
                    self.exe_text.insert("end","\n")
                    self.update_progress(idx/setting_frame_cnt,file_name,self.exe_text)
                    self.exe_text.see("end")
                    if self.out.isOpened():
                        self.out.write(fr)
                    else:
                        break
                    if idx % snap_freq==0:
                        image = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(image)
                        image = image.resize((700, 400))
                        image = ImageTk.PhotoImage(image)
                        # self.image=image
                        self.label3.config(text="녹화중...")
                        self.label3.configure(image=image)
                        self.label3.image=image
                    cv2.waitKey(delay=delay)
                    
                else:
                    self.stop_recoding(file_name,file_name_s,path_file_name,path_file_name_s)
                    file_size=(os.path.getsize(path_file_name_s))/1024/1024
                    self.exe_text.insert("end", 
                                         f'\nThe file {file_name}({round(file_size,2)}MB) saved sucessfully\n\n')
                    self.exe_text.see("end")
                    logging.info(f'The file {file_name}({round(file_size,2)}MB) saved sucessfully')
                    break
                idx+=1
        except(KeyboardInterrupt, SystemExit):
                logging.exception('Exit dut to keyboard interrupt')
        except Exception as ex:
            logging.exception(f'Traceback error: {ex}')
            traceback.print_exc()
        finally:
            #self.view.release()
            self.out.release()
            
    def setting_file_name(self):
        self.label3.config(text="녹화 준비중...")
        # self.label3.configure(image="")
        self.image=[]
        d=datetime.now()
        self.entryText1.set(d)
        
        file_name= f"f{d.strftime('%Y%m%d%H%M%S')}.mp4"
        file_name_s= f"fc{d.strftime('%Y%m%d%H%M%S')}.mp4"
        
        path_file_name=os.path.join(self.path,file_name)
        path_file_name_s=os.path.join(self.path,file_name_s)
        self.entryText2.set(file_name) 
        return file_name,file_name_s,path_file_name,path_file_name_s       
    
    def stop_recoding_btn(self):
        d=datetime.now()
        self.entryText1.set(d)
        file_name= ''
        self.entryText2.set(file_name)
        #self.view.release()
        self.label3.config(text="녹화 중지됨 !")
        self.label3.configure(image=[])#self.image)
        self.image=[]#self.image
        self.label3.pack()
        self.thread_on=False
        self.out_set=False
        # self.out.release()
            
    def stop_recoding(self,file_name,file_name_s,path_file_name,path_file_name_s):
        d=datetime.now()
        self.entryText1.set(d)
        file_name= ''
        self.entryText2.set(file_name)
        #self.view.release()
        self.out.release()
        self.label3.config(text="녹화 중지됨 !")
        self.label3.configure(image=[])#self.image)
        self.image=[]#self.image
        self.label3.pack()
        if os.path.isfile(path_file_name):
            os.rename(path_file_name,path_file_name_s)
            
    def update_progress(self,progress,file_name,tk_text):
        barLength = 10 # Modify this to change the length of the progress bar
        status = ""
        if isinstance(progress, int):
            progress = float(progress)
        if not isinstance(progress, float):
            progress = 0
            status = "error: progress var must be float"
        if progress < 0:
            progress = 0
            status = "Halt..."
        if progress >= 1:
            progress = 1
            status = "Done..."
        block = int(round(barLength*progress))
        text = " {3} is [{0}] {1}% in process {2}".format( "#"*block + "-"*(barLength-block),
                                                           round(progress*100,2), status,file_name)
        #sys.stdout.write(text)
        tk_text.insert("end",text)
        sys.stdout.flush()
        return text
    
    def sumof_progress(self,num,total,file_tr_name):
        self.num = self.num+num
        trans_idx = float(self.trans_text.index("end"))-1
        self.trans_text.delete(trans_idx,"end")
        self.trans_text.insert("end","\n")
        self.update_progress(self.num/total,file_tr_name,self.trans_text)
        self.trans_text.see("end")
        
    def file_conveyance(self):
        while True:
            if self.tt==False:
                break
            try:
                time.sleep(1)
                file_tmp=[f for (dirpath, dirnames, filenames) in os.walk(self.path) for f in filenames if "fc" in f]
                if len(file_tmp):
                    logging.info(f"file_name : {file_tmp} and cnt:{len(file_tmp)}")
                # if file_tmp:
                #     self.file_exist=True
                
                if len(file_tmp):#self.file_exist:
                    file_tr_name=file_tmp[0]
                    #for file_tr_name in file_tmp:
                    file_path = os.path.join(self.path,file_tr_name)
                    total=os.path.getsize(file_path)
                    host=self.config[self.env]['FTP_SERVER_IP']
                    try:
                    # with open(file_path ,mode='rb') as uploadfile:
                        with FTP(host) as session:
                            # session.connect(self.config[self.env]['FTP_SERVER_IP'], 21) 
                            session.login(self.config[self.env]['FTP_ID'],
                                        self.config[self.env]['FTP_PASS'])

                            # file_path = os.path.join(self.path,file_tr_name)
                            with open(file_path ,mode='rb') as uploadfile:
                                session.encoding='utf-8'
                                total=os.path.getsize(file_path)
                                session.storbinary("STOR " + f"{self.target_path}/{file_tr_name}",
                                                uploadfile)#,20480,
                                                # callback=lambda sent: self.sumof_progress(len(sent),
                                                #                                             total,
                                                #                                             file_tr_name))
                                self.num=0
                                self.trans_text.insert("end", f"{file_tr_name} ({round(total/1024/1024,2)}MB) was transfered successfully.\n")
                                self.trans_text.see("end")
                        try:
                            file= os.path.join(self.path,file_tr_name)
                            if os.path.isfile(file):
                                os.remove(file)
                                self.trans_text.see("end")
                            else: pass
                        except Exception as ex:
                            logging.exception(f'Traceback error: {ex}')
                            traceback.print_exc()
                    
                    except(KeyboardInterrupt, SystemExit):
                        logging.exception('Exit dut to keyboard interrupt')
                    except Exception as ex:
                        logging.exception(f'Traceback error: {ex}')
                    
               
            except(KeyboardInterrupt, SystemExit):
                    logging.exception('Exit dut to keyboard interrupt')
            except Exception as ex:
                logging.exception(f'Traceback error: {ex}')
                traceback.print_exc()
                

if __name__ == "__main__":
    env = sys.argv[1] if len(sys.argv) >= 2 else "DEFAULT"
    t = Fk_viewer(env)

