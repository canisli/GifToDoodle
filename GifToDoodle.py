import gradio as gr
from PIL import Image
import requests

import sys, os
import shutil
import glob

fpath = sys.argv[1]
n_frames = 0
duration = 0

if(len(os.listdir('frames_processed/')) == 0):
    with Image.open(fpath) as gif:
        n_frames = gif.n_frames
        duration = gif.duration
        for i in range(gif.n_frames):
            gif.seek(i)
            gif.save('frames_raw/{}.png'.format(i))


    for i in range(n_frames):
        frame_path = 'frames_raw/'+str(i)+'.png'
        data = gr.processing_utils.encode_url_or_file_to_base64(frame_path)
        ai_url = 'https://hf.space/gradioiframe/carolineec/informativedrawings/+/api/predict/'
        r = requests.post(ai_url,  json={'data': [data]})
        print(str(i), str(r.status_code))
        processed_data = r.json()['data'][0]
        output_path = 'frames_processed/'+str(i)+'.png'
        temp = gr.processing_utils.decode_base64_to_file(processed_data, encryption_key=None, file_path=None)
        shutil.copy(temp.name, output_path)

imgs = (Image.open(f) for f in sorted(glob.glob('frames_processed/*.png')))
img = next(imgs)  # extract first image from iterator
img.save(fp='output.gif', format='GIF', append_images=imgs,
         save_all=True, duration=duration, loop=0)


# # upload to ImgBB and get link
# imgbb_url = 'https://api.imgbb.com/1/upload'
        # data = {
        #     'key': '94ef78682d7ba24685e3c33c7d9d5b4b',
        #     'image': base64.b64encode(frame.read())
        # }
        # r = requests.post(imgbb_url, data=data)
        # # print(json.dumps(json.loads(r.content), indent=4))
        # img_url = r.json()['data']['image']['url']
        # print(img_url)
