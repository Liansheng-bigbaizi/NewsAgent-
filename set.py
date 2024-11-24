import nntp
import sys



def Choice(n):
    nntps = nntp.getAddress()
    if n == '1':
        print("当前服务器列表")
        m = 1
        for i in nntps:
            print("{} : {}".format(m, i))
            m += 1

    elif n == '2':
        newAddress = input("请输入新的服务器地址:")
        nntp.addNewAddress(newAddress, nntps)

    elif n == '3':
        print("当前服务器列表")
        m = 1
        for i in nntps:
            print("{} : {}".format(m, i))
            m += 1
        Num = int(input("请输入要删除的服务器地址："))
        nntp.DeleteAddress(Num, nntps)


    elif n == '4':
        print("请选择服务器地址：")
        count = 1
        for i in nntps:
            print('{} : {}'.format(count, i))
            count += 1

        m = int(input())
        serverName = nntps[m - 1]
        groupName = input("请输入想要浏览的组：")
        try:
            nntp.runDefaultSetup(serverName, groupName)
        except Exception as e:
            print("An error exists:{}".format(e))

    elif n == '5':
        try:
            sys.exit()
        except SystemExit as e:
            print("退出成功：{}".format(e))

    else:
        print('请重新输入')