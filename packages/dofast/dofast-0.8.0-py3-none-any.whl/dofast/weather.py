import codefast as cf

from dofast.toolkits.telegram import tg_bot


class Weather:
    def __init__(self):
        self.api = 'http://t.weather.itboy.net/api/weather/city/101010100'
        self.type_color_map = {
            '晴': 'forestgreen',
            '多云': 'gold',
            '阴': 'gold',
            '小雨': 'firebrick1',
            '阵雨': 'firebrick1',
            '中雨': 'firebrick2',
            '大雨': 'firebrick3',
            '暴雨': 'firebrick4'
        }

    def r_data(self):
        return cf.net.get(self.api).json()['data']['forecast'][0]

    def _daily(self, markdown: bool = False):
        text = '\n'.join('| {} | {} |'.format(k, v)
                         for k, v in self.r_data().items())
        if markdown:
            text = '```|K|V|' + text
            text = text + '```'
        return text

    @cf.utils.retry(initial_wait=5)
    @tg_bot(use_proxy=False)
    def daily(self):
        return '\n'.join('{:<10} {}'.format(k, v)
                         for k, v in self.r_data().items())


def entry():
    Weather().daily()


if __name__ == '__main__':
    wea = Weather()
    cf.say(wea.daily())
