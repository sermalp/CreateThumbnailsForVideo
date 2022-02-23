import numpy as np
import cv2
import os

import inspect
import sys


def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


def tumbnail(file, path):
    print('Подождите...')
    os.chdir(path)

    vidcap = cv2.VideoCapture(path+'\\'+file)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    n=12
    total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    time_line = total_frames / fps

    frames_step = total_frames//n
    time_line_step=time_line//n
    a=[]
    b=[]

    #seconds to 00:00:00
    def sec_to_time(t):
        h=str(t//3600)
        m=(t//60)%60
        s=t%60
        if m<10:
            m='0'+str(m)
        else:
            m=str(m)
        if s<10:
            s='0'+str(s)
        else:
            s=str(s)    
        #print(h+':'+m+':'+s)
        t=h+':'+m+':'+s
        return t

    for i in range(n):
        #here, we set the parameter 1 which is the frame number to the frame (i*frames_step)
        vidcap.set(1,i*frames_step)
        success,image = vidcap.read()
        #уменьшаем картинку 
        scale_percent = 50
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        image=cv2.resize(image, (width, height))

        # вставка текста красного цвета c time_line
        font = cv2.FONT_HERSHEY_COMPLEX    
        t=int(time_line_step)*i    
        image=cv2.putText(image, sec_to_time(t), (100, 30), font, 0.5, color=(0, 0, 255), thickness=0)   
        cv2.imwrite('image'+str(i)+'.jpg',image)
        a.append('image'+str(i)+'.jpg')
    vidcap.release()

    #склеиваем видео по 3 по горизонтали
    def glue (img1,img2,img3,x):
        i1 = cv2.imread(img1)
        i2 = cv2.imread(img2)
        i3 = cv2.imread(img3)    
        vis = np.concatenate((i1, i2, i3), axis=1)
        cv2.imwrite('out'+str(x)+'.png', vis)
        b.append('out'+str(x)+'.png')
    x=0
    while x<len(a):    
        glue(a[x],a[x+1],a[x+2],x)
        x+=3
    #склеиваем видео по вертикали
    def glue2 (img1,img2,img3,img4):
        i1 = cv2.imread(img1)
        i2 = cv2.imread(img2)
        i3 = cv2.imread(img3)
        i4 = cv2.imread(img4) 
        vis = np.concatenate((i1, i2, i3,i4), axis=0)
        cv2.imwrite(file[:-4]+'.jpeg', vis)
    glue2(b[0],b[1],b[2],b[3])

    #уборка
    c=['jpg', 'png']
    for root, dirs, files in os.walk(path):    
        for file in files:
            if file[-3:] in c:
                os.remove(file)

    print('Готово')


video=['wmv', 'mp4', 'avi', 'mov', 'MP4', '.rm', 'mkv']
print('Старт')
#получаем текущий каталог откуда запущен скрипт
dir_start_scr = get_script_dir()
#добавляем к текущему каталогу строку "\video" - это папка поиска видео
dir_search_video = dir_start_scr + '\\video'
#перебираем все файлы в каталогах
for root, dirs, files in os.walk(r''+dir_search_video):    
    for file in files:
        if file[-3:] in video:
            #полный путь до файла
            file_full_path = root+"\\"+file
            print('В обработке:'+file_full_path)
            tumbnail(file, root)