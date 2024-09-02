import xbmc
import xbmcaddon
import os
import requests
import re
import time

# 애드온 설정 불러오기
addon = xbmcaddon.Addon()
addon_data_path = xbmc.translatePath(addon.getAddonInfo('profile'))

# 파일 경로 설정
file_path = os.path.join(addon_data_path, "test.m3u")

def update_m3u():
    # URL 정의
    urlSBS = 'https://tistory1.daumcdn.net/tistory/2864460/skin/images/CATV_2_76142D8F.m3u8'
    urlMBC = 'https://tistory1.daumcdn.net/tistory/2864460/skin/images/CATV_1_B862A42B.m3u8'
    urlJTBC = 'https://tistory1.daumcdn.net/tistory/2864460/skin/images/CATV_51_5D637AFC.m3u8'
    urlChA = 'https://tistory1.daumcdn.net/tistory/2864460/skin/images/CATV_52_12C896BD.m3u8'
    urlMBN = 'https://www.mbn.co.kr/player/mbnStreamAuth_new_live.mbn?vod_url=https://hls-live.mbn.co.kr/mbn-on-air/600k/playlist.m3u8'

    headerSBS = 'https://tvlive.sbs.co.kr/sbsch6/sbsch62.stream/'
    headerMBC = 'https://live.imnews.imbc.com/imnews/_definst_/live2.stream/playlist.'
    headerJTBC = 'https://jtbclive-cdn.jtbc.co.kr/mobileweb/newmoweb.stream/chunklist.'
    headerCha = 'https://channelaid3.ichannela.com/atv3/chunklist.'
    headerMBN = ''

    requestURL = [urlSBS, urlMBC, urlJTBC, urlChA, urlMBN]
    headerURL = [headerSBS, headerMBC , headerJTBC , headerCha ,  headerMBN]

    targetURL = ['' ,'' ,'' ,'' ,'' ]

    for i in range(0, 4):
        try:
            response = requests.get(requestURL[i])
            urls = re.findall(r'https://\S+', response.text)

            if urls:
                last_url = urls[-1]
                url = last_url
            else:
                xbmc.log("No URL found", xbmc.LOGERROR)
                continue

        except requests.exceptions.RequestException as e:
            xbmc.log(f"Error: {e}", xbmc.LOGERROR)
            continue

        try:
            response = requests.get(url)
            urls = re.findall(r'm3u8\S+', response.text)

            if urls:
                last_url = urls[-1]
                url = last_url
            else:
                xbmc.log("No URL found", xbmc.LOGERROR)
                continue

        except requests.exceptions.RequestException as e:
            xbmc.log(f"Error: {e}", xbmc.LOGERROR)
            continue
        
        url = f"t.{url}"
        targetURL[i] = f"{headerURL[i]}{url}"

    try:
        response = requests.get(requestURL[4])
        urls = re.findall(r'https://\S+', response.text)

        if urls:
            last_url = urls[-1]
            targetURL[4] = last_url
        else:
            xbmc.log("No URL found", xbmc.LOGERROR)

    except requests.exceptions.RequestException as e:
        xbmc.log(f"Error: {e}", xbmc.LOGERROR)

    with open(file_path, "w") as file:
        file.write("#EXTM3U" + "\n")
        file.write("\n")
        file.write('#EXTINF:-1 tvg-id="SBS" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Seoul_Broadcasting_System_logo.svg/225px-Seoul_Broadcasting_System_logo.svg.png" ,SBS' + "\n")
        file.write(targetURL[0] + "\n")
        file.write("\n")
        file.write('#EXTINF:-1 tvg-id="KBS 2" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/KBS_2_logo.svg/512px-KBS_2_logo.svg.png" group-title="General",KBS 2TV' + "\n")
        file.write("http://mytv.dothome.co.kr/ch/public/3.php" + "\n")
        file.write("\n")
        file.write('#EXTINF:-1 tvg-id="KBS 1" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/KBS_1_logo.svg/512px-KBS_1_logo.svg.png" group-title="General",KBS 1TV' + "\n")
        file.write("http://mytv.dothome.co.kr/ch/public/1.php" + "\n")
        file.write("\n")
        file.write('#EXTINF:-1 tvg-id="MBC" tvg-logo="https://imgur.com/U3lsmaA.png" group-title="General",MBC' + "\n")
        file.write(targetURL[1] + "\n")
        file.write("\n")
        file.write('#EXTINF:-1 tvg-id="JTBC" tvg-logo="https://i.imgur.com/VsfGIUk.png" group-title="General",JTBC' + "\n")
        file.write(targetURL[2] + "\n")
        file.write("\n")
        file.write('#EXTINF:-1 tvg-id="채널A" tvg-logo="https://i.imgur.com/Pu29gAN.png" group-title="General",채널A' + "\n")
        file.write(targetURL[3] + "\n")
        file.write("\n")
        file.write('#EXTINF:-1 tvg-id="TVChosun.kr" tvg-logo="https://i.imgur.com/7AzOwd2.png" group-title="General",TV CHOSUN' + "\n")
        file.write("#EXTVLCOPT:http-referrer=http://broadcast.tvchosun.com/onair/on.cstv" + "\n")
        file.write("http://onair.cdn.tvchosun.com/origin1/_definst_/tvchosun_s1/playlist.m3u8" + "\n")
        file.write("\n")
        file.write('#EXTINF:-1 tvg-id="MBN" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/MBN_%EB%A1%9C%EA%B3%A0.png/225px-MBN_%EB%A1%9C%EA%B3%A0.png" group-title="General",MBN' + "\n")
        file.write(targetURL[4] + "\n")

# 스크립트 초기 실행
update_m3u()

# 매 10분마다 스크립트 실행
while not xbmc.abortRequested:
    time.sleep(600)  # 10분 대기
    update_m3u()
