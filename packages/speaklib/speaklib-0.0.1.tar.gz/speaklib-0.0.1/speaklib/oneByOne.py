class printf(object):
    '''逐字输出'''
    def __init__(self,*things,time=0.05,end="\n"):
        '''输出内容并返回对象'''
        global timer
        for id in things:
            for letter in id:
                print(letter,end='')
                fflush=__import__("sys").stdout.flush 
                fflush()
                timer =__import__("time")
                timer.sleep(time)
            timer.sleep(time*10)
        print(end=end)
    def inputf(self):
        '''输出后调用方法以返回输入值，非必选，建议输出时添加end=''以免输出后换行'''
        return input()
    pass