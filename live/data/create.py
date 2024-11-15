import json

def main():
    with open('../config/index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    with open('..//config/rooms.json', 'r', encoding='utf-8') as f:
        rooms = json.load(f)["rooms"]
    img = ""
    for name in rooms:
        include_img = f'''
        <div class="grid-item">
        <p> {name} </p>
        <img src="data/{name}.jpeg" alt="图片1">
        </div>'''
        img += include_img
    index_html = index_html.replace("<!-- 图片部分 -->", img)
    with open('../../views/live/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
main()

