# -*- coding:utf-8 -*-

from lxml import etree
import requests


class WeatherSearch(object):
    def __init__(self, key):
        self.KEYS = [u'天气', u'查询天气', 'tianqi', 'chaxuntianqi', 'weather', '2']
        self.key = key if key not in self.KEYS else u'北京天气'
        self.url = 'http://www.baidu.com/s?wd=%s' % self.key

    def search(self):
        # ℃ ☀⛅☁⛈❄ ☂️☔️⏱⏲⏰ 😦😦😦
        # ☀⛅☁⛈☃⛄❄☔☂
        try:
            response = requests.get(self.url)
        # 判断响应体内容
        except Exception as e:
            print(e)
        else:
            data = etree.HTML(response.content)
            # 日期
            today = data.xpath('//p[@class="op_weather4_twoicon_date"]/text()')[0].strip()
            for i in range(1, 6):
                aqi = data.xpath('//span[@class="op_weather4_twoicon_aqi_level_%d_bg '
                                 'op_weather4_twoicon_realtime_quality_today"]//span/text()' % i)
                if aqi:
                    break
            # 空气质量         //span[@class="op_weather4_twoicon_aqi_level_3_bg op_weather4_twoicon_realtime_quality_today"]
            aqi_level = aqi[1]
            # 空气指数
            aqi_num = aqi[0]
            # 实时温度
            degree = data.xpath('//span[@class="op_weather4_twoicon_shishi_title"]/text()')[0]
            # 地区
            try:
                location = data.xpath('//h3[@class="t c-gap-bottom-small"]//em/text()')[0]
                if u'天气' == location:
                    location = u'北京天气'
            except:
                # l = data.xpath('//div[@class="op_weather4_twoicon_open  OP_LOG_BTN"]/text()')[0]
                l = data.xpath('//h3[@class="t c-gap-bottom-small"]/a/text()')[0]
                r_index = l.find(u'预')
                location = l[:r_index]
            # 温度区间
            # 共五天
            degree_range = data.xpath('//p[@class="op_weather4_twoicon_temp"]/text()')
            # 天气情况
            # 共五天
            if location == u'北京天气':
                forecast = data.xpath('//p[@class="op_weather4_twoicon_weath"]/@title')
            else:
                forecast = data.xpath('//p[@class="op_weather4_twoicon_weath"]/text()')
            forecast = self.judge(forecast)
            # 风
            # 共五天
            wind = data.xpath('//p[@class="op_weather4_twoicon_wind"]/text()')

            # 添加限行信息
            if u'北京' in self.key:
                try:
                    traffic_response = requests.get('http://www.baidu.com/s?wd=北京限行')
                except Exception as e:
                    print(e)
                else:
                    traffic_data = etree.HTML(traffic_response.content)
                    # 共四天
                    date = traffic_data.xpath('//div[@class="op_traffic_title"]/text()')
                    # xpath匹配限号，共四天
                    num_1 = u'和'.join(traffic_data.xpath('//div[@class="op_traffic_left"]/div[2]/text()'))
                    num_2 = u'和'.join(traffic_data.xpath('//div[@class="op_traffic_right"][1]/div[2]/text()'))
                    num_3 = u'和'.join(traffic_data.xpath('//div[@class="op_traffic_right"][2]/div[2]/text()'))
                    result_today = u'%s\n%s尾号: %s\n%s情况如下:\n实时空气质量: %s %s\n实时温度:%s℃\n温度区间: %s\n预计天气变化: %s\n风力情况: %s\n\n' % (
                        today, date[0], num_1, location, aqi_num, aqi_level, degree, degree_range[0], forecast[0], wind[0])
                    result_tomorrow = u'%s尾号: %s\n明天%s情况如下:\n温度区间: %s\n预计天气变化: %s\n风力情况: %s\n\n' % (
                        date[1], num_2, location, degree_range[1], forecast[1], wind[1])
                    result_the_day_after_tomorrow = u'%s尾号: %s\n后天%s情况如下:\n温度区间: %s\n预计天气变化: %s\n风力情况: %s\n\n' % (
                        date[2], num_3, location, degree_range[2], forecast[2], wind[2])
            else:
                result_today = u'%s\n%s情况如下:\n实时空气质量: %s %s\n实时温度:%s℃\n温度区间: %s\n预计天气变化: %s\n风力情况: %s\n\n' % (
                    today, location, aqi_num, aqi_level, degree, degree_range[0], forecast[0], wind[0])
                result_tomorrow = u'明天%s情况如下:\n温度区间: %s\n预计天气变化: %s\n风力情况: %s\n\n' % (
                    location, degree_range[1], forecast[1], wind[1])
                result_the_day_after_tomorrow = u'后天%s情况如下:\n温度区间: %s\n预计天气变化: %s\n风力情况: %s\n\n' % (
                    location, degree_range[2], forecast[2], wind[2])
            return u'☀⛅☁⛈☃⛄❄☔☂\n' + result_today + result_tomorrow + result_the_day_after_tomorrow

    def judge(self, li):
        li_f = []
        for status in li[:3]:
            status = status.strip()
            if u'晴' == status or u'转晴' in status:
                status += u'☀'
            elif u'多云' == status or u'阴' == status or u'转阴' in status:
                status += u'☁'
            elif u'转多云' in status or u'间多云' in status:
                status += u'⛅'
            elif u'转小雨' in status or u'小雨' == status:
                status += u'☔'
            elif u'雨' in status:
                status += u'⛈'
            elif u'雪' in status:
                status += u'❄'
            else:
                li_f.append(status)
            li_f.append(status)
        return li_f
s = WeatherSearch("beijingtianqi")

if __name__ == '__main__':
    s = WeatherSearch("tianqi")
    print(s.search())

