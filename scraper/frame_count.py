import glob
import pandas as pd
import subprocess
#from subprocess import check_output

#df = pd.read_csv('/Users/xinyue/Documents/college/SA_Work/video_id.csv')

videos = glob.glob('/Users/xinyue/PycharmProjects/youtube_dl/*.mp4')

df = pd.DataFrame()

for file in videos:

    first_file =('/').join(file.split('/')[:-1])
    second_file = file.split('/')[-1]

    third_file = ('\ ').join(second_file.split(' '))
    third_file = third_file.replace("'","\\'")
    third_file = third_file.replace("$", "\\$")
    third_file = third_file.replace("&", "\\&")
    file = first_file+'/'+third_file
    #print(file)
    #subprocess.call('tcprobe -i ' + file, shell=True)
    return_info = subprocess.Popen('ffprobe -select_streams v -show_streams ' + file, shell=True, stdout=subprocess.PIPE)
    find_frame = return_info.communicate()[0]
    find_frame = find_frame.decode("utf-8")
    find_frame = find_frame.split('\n')
    frame = 0
    for i in find_frame:
        if 'nb_frames' in i:
            frame = i.split('=')[1]
            print(frame)

    video_id = second_file.split('-')[-1]
    video_id = video_id.split('.')[0]
    data = {'name': video_id, 'nb_frames': frame}
    df = df.append(data, ignore_index=True)
    df.to_csv('/Users/xinyue/Documents/college/SA_Work/video_frames.csv')
    #output = return_info.poll()
    #print(find_frame)



