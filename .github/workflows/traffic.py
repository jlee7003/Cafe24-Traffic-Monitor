import requests
from bs4 import BeautifulSoup
import os

# ===== 설정값 =====
CAFE24_TRAFFIC_URL = os.getenv("CAFE24_TRAFFIC_URL")  # GitHub Secret에서 가져옴
COOKIE = os.getenv("CAFE24_COOKIE")                   # GitHub Secret
LIMIT = 80                                            # 초과 시 카톡 알림 기준 %
KAKAO_TOKEN = os.getenv("KAKAO_TOKEN")                # GitHub Secret
# ==================

def get_traffic_percent():
    headers = {
        "Cookie": COOKIE,
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(CAFE24_TRAFFIC_URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # ★★★ 여기 부분은 나중에 네 카페24 HTML을 보고 딱 맞춰 수정해줄게 ★★★
    elem = soup.select_one(".traffic-percent")
    if not elem:
        raise Exception("트래픽 %를 찾을 수 없음. HTML 구조 확인 필요")

    percent = elem.text.replace("%", "")
    return float(percent)

def send_kakao_message(msg):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {KAKAO_TOKEN}"
    }
    data = {
        "template_object": f"""{{
            "object_type":"text",
            "text":"{msg}",
            "link":{{}}
        }}"""
    }
    requests.post(url, headers=headers, data=data)

def main():
    traffic = get_traffic_percent()
    print(f"현재 트래픽: {traffic}%")

    if traffic >= LIMIT:
        send_kakao_message(f"🚨 카페24 트래픽 경고! 현재 트래픽 {traffic}% 입니다.")
        print("카카오톡 알림 전송됨")
    else:
        print("정상 범위")

if __name__ == "__main__":
    main()
