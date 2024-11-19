from pyecharts.charts import Line, Grid
from pyecharts import options as opts
from pyecharts.options import TextStyleOpts
import json
from pyecharts.commons.utils import JsCode

import os
import sys
sys.path.append("/".join(os.path.abspath(__file__).split("\\")[:-3]))
from utils import sql


def get_hot(platform):
    data_sql = sql.query_hot(platform)

    data = {i["time"]: json.loads(i["data"])
            for i in data_sql}
    time_len = len(data)
    table_data = {
        "time": [t for t in data],
        "name": {data[time][i]["name"]: [None] * time_len
                 for time in data for i in range(len(data[time]))
                 }
    }
    for j, time in enumerate(data):
        si = data[time]
        for i in range(len(si)):
            name = si[i]["name"]
            table_data["name"][name][j] = int(si[i]["rank"])
    return table_data


def create_table(platform, key):
    table_data = get_hot(platform)
    times = table_data['time']

    line = Line(init_opts=opts.InitOpts(width="1500px", height="800px", theme='dark'))

    line.add_xaxis(times)

    for name in table_data['name']:
        width_1 = 2
        for i in key:
            if i in name:
                width_1 = 15

        line.add_yaxis(
            name,
            y_axis=table_data["name"][name],
            label_opts=opts.LabelOpts(
                is_show=True,
                position="inside",
                font_size=15,
                color="#fff",
                font_style="bold",
                formatter=JsCode("""
                    function(params) {
                        let index = params.dataIndex;
                        if (index % 6 === 1) {return params.seriesName + ' ' + params.value[1];}
                         else {return '                           ';}
                        }"""),
            ),
            linestyle_opts=opts.LineStyleOpts(width=width_1)
        )

    line.set_global_opts(
        yaxis_opts=opts.AxisOpts(is_inverse=True),
        title_opts=opts.TitleOpts(title=f"{platform}热搜指数", title_textstyle_opts=opts.TextStyleOpts(font_size=40)),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            axis_pointer_type="line",
            border_width=3,
            border_color="white",
            padding=10,
            trigger_on="mousemove",
            textstyle_opts=TextStyleOpts(font_size=20, font_style="bold", color="#000")
        ),
        legend_opts=opts.LegendOpts(is_show=False),
        datazoom_opts=[
            opts.DataZoomOpts(is_show=True, type_="slider", orient="horizontal", ),
            opts.DataZoomOpts(is_show=True, type_="slider", orient="vertical"),
        ]
    )

    line.render(f"../views/hot/data/{platform}.html")


def view():
    with open("config/key.json", "r",encoding='utf-8') as f:
        key = json.load(f)['key']

    platform = ["baidu", "bili", "douyin", "kuaishou", "toutiao", "weibo", "zhihu"]
    for i in platform:
        create_table(i, key)


if __name__ == '__main__':
    create_table("zhihu", ["知乎", "知乎周刊"])
