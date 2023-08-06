import codefast as cf

from dofast import api


class BotHelper:
    def __init__(self):
        ...

    def draw_weather_image(self):
        type_color_map = {
            '晴': 'forestgreen',
            '多云': 'gold',
            '阴': 'gold',
            '小雨': 'firebrick1',
            '阵雨': 'firebrick1',
            '中雨': 'firebrick2',
            '大雨': 'firebrick3',
            '暴雨': 'firebrick4'
        }
        data = api.weather.r_data()
        text = '''digraph D{aHtmlTable [shape=plaintext,label=<<table border='0' cellborder='1' CELLSPACING='0' CELLPADDING='4' style='rounded'>'''
        for e in data.items():
            k, v = e[0].upper(), e[-1]
            color = type_color_map.get(v)
            if color:
                text += f'<tr><td>{k}</td><td BGCOLOR="{color}">{v}</td></tr>'
            else:
                text += f'<tr><td>{k}</td><td>{v}</td></tr>'

        text += '''\n</table>>];}'''
        dot_file = '/tmp/weather.dot'
        cf.io.write(text, dot_file)
        cf.shell(f'dot -Tpng {dot_file} -o /tmp/weather.png')
        cf.io.rm(dot_file)
