import sys

if __name__ == '__main__':
    print('参数个数为:', len(sys.argv), '个参数。')
    print('参数列表:', str(sys.argv))
    print('脚本名为：', sys.argv[0])
    print(sys.argv[1])
    # for i in range(1, len(sys.argv)):
    #     print('参数 %s 为：%s' % (i, sys.argv[i]))
