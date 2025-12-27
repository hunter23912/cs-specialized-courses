import requests
from bs4 import BeautifulSoup
import os

def download_video(url, save_folder='videos'):
    # 创建保存目录
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # 获取网页内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 假设视频标签为 <video> 或 <source>
    video_tags = soup.find_all('video')
    sources = []
    for video in video_tags:
        src = video.get('src')
        if src:
            sources.append(src)
        # 查找 <source> 标签
        for source in video.find_all('source'):
            src = source.get('src')
            if src:
                sources.append(src)

    # 下载视频
    for idx, video_url in enumerate(sources):
        if not video_url.startswith('http'):
            # 拼接完整URL
            video_url = requests.compat.urljoin(url, video_url)
        print(f'正在下载: {video_url}')
        video_data = requests.get(video_url, headers=headers).content
        filename = os.path.join(save_folder, f'video_{idx+1}.mp4')
        with open(filename, 'wb') as f:
            f.write(video_data)
        print(f'已保存为: {filename}')

if __name__ == '__main__':
    target_url = 'https://vod.cc.shu.edu.cn/jy-application-resourcemanage-ui/#/play-video?teclId=10489&teclCode=243-08305143-1001'  # 替换为目标网页
    download_video(target_url)