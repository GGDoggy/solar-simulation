import requests
import urllib.parse

planets = [
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune"
]
para_exam = {
    'format':"text",
    # 'COMMAND':"'mars bary'",
    'OBJ_DATA':"'YES'",
    'MAKE_EPHEM':"'YES'",
    'EPHEM_TYPE':"'VECTORS'",
    'CENTER':"'@sun'",
    'REF_PLANE':"'ECLIPTIC'",
    'START_TIME':"'2005-01-01'",
    'STOP_TIME':"'2025-01-01'",
    'STEP_SIZE':"'1d'",
    'QUANTITIES':"'1'"
}


# for planet in planets:
#     para = para_exam.copy()
#     para.update({'COMMAND': f"'{planet} bary'"})
#     url_para = urllib.parse.urlencode(para)
#     print(url_para)

#     req = requests.get("https://ssd.jpl.nasa.gov/api/horizons.api?" + url_para)
#     with open(f"{planet}.get.txt", "w", encoding="utf-8") as file:
#         file.write(req.content.decode("utf-8"))
        
        
para_exam.update({"COMMAND": "sun"})
para_exam.pop("CENTER")
url_para = urllib.parse.urlencode(para_exam)
print(url_para)
req = requests.get("https://ssd.jpl.nasa.gov/api/horizons.api?" + url_para)
with open("sun_from_earth.get.txt", "w", encoding="utf-8") as file:
    file.write(req.content.decode("utf-8"))