from hotKeyword import *

def distance_level(content):
    hotKeyword("사회적 거리두기")
    content = content['userRequest']['utterance']
    #print(content)
    dataSend = {
      "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type" : "basicCard",
                        "items": [
                            {
                                "title" : "사회적 거리두기",
                                "description" : "현재 사회적 거리두기 2단계입니다.",
                                "thumbnail": {
                                    "imageUrl": "https://user-images.githubusercontent.com/71917474/101108676-6960d200-3618-11eb-80d6-83a9a68069c5.jpg"},
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "지역별 안내",
                                        "webLinkUrl": "http://ncov.mohw.go.kr/duBoardList.do?brdId=2&brdGubun=29&flowId=main"},
                                    {
                                        "action": "share",
                                        "label": "공유하기"}
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    }

    return dataSend