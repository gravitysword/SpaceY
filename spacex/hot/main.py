import hot
import table
import time
def time__sleep(t):
    length = 40
    for i in range(t):
        time.sleep(0.99)
        percent = ((i + 1) / t) * 100
        arrow = '█' * int(length * i // t)
        spaces = ' ' * (length - len(arrow))

        print(f'\r等待ing：[{arrow}{spaces}] {percent:.2f}%', end='')


if __name__ == '__main__':
    while True:
        print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}     热搜刷新")
        hot.hot()
        table.view()

        time__sleep(60)



