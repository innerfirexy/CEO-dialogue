
import pandas as pd
import subprocess


df = pd.read_csv('/Users/xinyue/Documents/college/SA_Work/video_id.csv')[213:]
file1 = open("fail_video.txt","w")
for i,r in df.iterrows():
    if r['video_id'] == 7000109489:
        try:
            video_id = r['video_id']
            part_file = "http://video.cnbc.com/gallery/?video="
            files = part_file+str(video_id)
            subprocess.call('youtube-dl ' + files +' --verbose', shell=True)
        except:
            video_id = r['video_id']
            file1.writelines(video_id + '\n')

file1.close()

#7000109493