import random
import time


def main():
    while(True):
        iniGame()
        createPlayerList()
        gameStart()
        gamePlay()
        showResult()
        showWinAndLose()
        startNewGame = input('Start a new Game？（y）')
        if startNewGame != 'y':
            break


# 初始化玩家参数
def iniGame():
    global playerCount, cards
    while(True):
        try:
            playerCount = int(input('input user：'))
        except ValueError:
            print('invalid input！')
            continue
        if playerCount < 2:
            print('userInput must larger than 1！')
            continue
        else:
            break
    try:
        decks = int(input('Enter the number of cards：（default is equal to the number of players）'))
    except ValueError:
        print('default values have been used！')
        decks = playerCount
    print('number of players：', playerCount, '，number of cards：', decks)
    cards = getCards(decks)  # 洗牌


# 建立玩家列表
def createPlayerList():
    global playerList
    playerList = []
    for i in range(playerCount):
        playerList += [{'id': '', 'cards': [], 'score': 0}].copy()
        playerList[i]['id'] = 'computer' + str(i+1)
    playerList[playerCount-1]['id'] = 'user'
    random.shuffle(playerList)  # 为各玩家随机排序


# 分2张明牌并计算得分
def gameStart():
    print('divide 2 open cards for each player：')
    for i in range(playerCount):  # 为每个玩家分2张明牌
        deal(playerList[i]['cards'], cards, 2)
        playerList[i]['score'] = getScore(playerList[i]['cards'])  # 计算初始得分
        print(playerList[i]['id'], ' ', getCardName(playerList[i]['cards']),
              ' 得分 ', playerList[i]['score'])
        time.sleep(1.5)


# 按顺序询问玩家是否要牌
def gamePlay():
    for i in range(playerCount):
        print('current', playerList[i]['id'])
        if playerList[i]['id'] == 'user':  # 玩家
            while(True):
                print('currrent hand card：', getCardName(playerList[i]['cards']))
                _isDeal = input('Want cards to continue or not？（y/n）')
                if _isDeal == 'y':
                    deal(playerList[i]['cards'], cards)
                    print('new card：', getCardName(playerList[i]['cards'][-1]))
                    # 重新计算得分:
                    playerList[i]['score'] = getScore(playerList[i]['cards'])
                elif _isDeal == 'n':
                    break
                else:
                    print('please input again！')
        else:  # 电脑
            while(True):
                if isDeal(playerList[i]['score']) == 1:  # 为电脑玩家判断是否要牌
                    deal(playerList[i]['cards'], cards)
                    print('Want cards.')
                    # 重新计算得分:
                    playerList[i]['score'] = getScore(playerList[i]['cards'])
                else:
                    print('Let it go.')
                    break
        time.sleep(1.5)


# 展示最终得分、手牌情况
def showResult():
    print('fianl score：')
    for i in range(playerCount):
        print(playerList[i]['id'], playerList[i]['score'],
              getCardName(playerList[i]['cards']))


# 胜负情况判定
def showWinAndLose():
    loserList = []  # [['id', score], ['id', score], ...]
    winnerList = []  # [['id', score], ['id', score], ...]
    winnerCount = 0
    loserCount = 0
    for i in range(playerCount):
        if playerList[i]['score'] > 21:  # 爆牌直接进入败者列表
            loserList.append([playerList[i]['id'],  playerList[i]['score']])
        else:  # 临时胜者列表
            winnerList.append([playerList[i]['id'], playerList[i]['score']])
    if len(winnerList) == 0:  # 极端情况：全部爆牌
        print('All players show cards：')
        for i in range(len(loserList)):
            print(loserList[i][0], loserList[i][1])
    elif len(loserList) == 0:  # 特殊情况：无人爆牌
        winnerList.sort(key=lambda x: x[1], reverse=True)  # 根据分数值排序胜者列表
        for i in range(len(winnerList)):  # 计算最低分玩家数量
            if i != len(winnerList)-1:
                if winnerList[-i-1][1] == winnerList[-i-2][1]:
                    loserCount = (i+2)
                else:
                    if loserCount == 0:
                        loserCount = 1
                    break
            else:
                loserCount = len(loserList)
        if loserCount == 1:
            loserList.append(winnerList.pop())
        else:
            while(len(loserList) != loserCount):
                loserList.append(winnerList.pop())
        for i in range(len(winnerList)):  # 计算最高分玩家数量
            if i != len(winnerList)-1:
                if winnerList[i][1] == winnerList[i+1][1]:
                    winnerCount = (i+2)
                else:
                    if winnerCount == 0:
                        winnerCount = 1
                    break
            else:
                winnerCount = len(winnerList)
        while(len(winnerList) != winnerCount):
            winnerList.pop()
        print('Win：')
        for i in range(len(winnerList)):
            print(winnerList[i][0], winnerList[i][1])
        print('Fail：')
        for i in range(len(loserList)):
            print(loserList[i][0], loserList[i][1])
    else:  # 一般情况：有人爆牌
        winnerList.sort(key=lambda x: x[1], reverse=True)  # 根据分数值排序胜者列表
        for i in range(len(winnerList)):  # 计算最高分玩家数量
            if i != len(winnerList)-1:
                if winnerList[i][1] == winnerList[i+1][1]:
                    winnerCount = (i+2)
                else:
                    if winnerCount == 0:
                        winnerCount = 1
                    break
            else:
                winnerCount = len(winnerList)
        while(len(winnerList) != winnerCount):
            winnerList.pop()
        print('Win：')
        for i in range(len(winnerList)):
            print(winnerList[i][0], winnerList[i][1])
        print('Fail：')
        for i in range(len(loserList)):
            print(loserList[i][0], loserList[i][1])


# 获取洗好的牌
def getCards(decksNum):
    cardsList = ['Aa', 'Ab', 'Ac', 'Ad',
                 'Ka', 'Kb', 'Kc', 'Kd',
                 'Qa', 'Qb', 'Qc', 'Qd',
                 'Ja', 'Jb', 'Jc', 'Jd',
                 '0a', '0b', '0c', '0d',
                 '9a', '9b', '9c', '9d',
                 '8a', '8b', '8c', '8d',
                 '7a', '7b', '7c', '7d',
                 '6a', '6b', '6c', '6d',
                 '5a', '5b', '5c', '5d',
                 '4a', '4b', '4c', '4d',
                 '3a', '3b', '3c', '3d',
                 '2a', '2b', '2c', '2d']
    cardsList *= decksNum       # 牌副数
    random.shuffle(cardsList)   # 随机洗牌
    return cardsList


# 要牌概率
probDict = {12: 0.92, 13: 0.87, 14: 0.74, 15: 0.5,
            16: 0.205, 17: 0.1294, 18: 0.07580895, 19: 0.033117337}
# 牌名字典
cardNameDict = {'Aa': '黑桃A', 'Ab': '红桃A', 'Ac': '梅花A', 'Ad': '方片A',
                'Ka': '黑桃K', 'Kb': '红桃K', 'Kc': '梅花K', 'Kd': '方片K',
                'Qa': '黑桃Q', 'Qb': '红桃Q', 'Qc': '梅花Q', 'Qd': '方片Q',
                'Ja': '黑桃J', 'Jb': '红桃J', 'Jc': '梅花J', 'Jd': '方片J',
                '0a': '黑桃10', '0b': '红桃10', '0c': '梅花10', '0d': '方片10',
                '9a': '黑桃9', '9b': '红桃9', '9c': '梅花9', '9d': '方片9',
                '8a': '黑桃8', '8b': '红桃8', '8c': '梅花8', '8d': '方片8',
                '7a': '黑桃7', '7b': '红桃7', '7c': '梅花7', '7d': '方片7',
                '6a': '黑桃6', '6b': '红桃6', '6c': '梅花6', '6d': '方片6',
                '5a': '黑桃5', '5b': '红桃5', '5c': '梅花5', '5d': '方片5',
                '4a': '黑桃4', '4b': '红桃4', '4c': '梅花4', '4d': '方片4',
                '3a': '黑桃3', '3b': '红桃3', '3c': '梅花3', '3d': '方片3',
                '2a': '黑桃2', '2b': '红桃2', '2c': '梅花2', '2d': '方片2'}


# 判断是否要牌
def isDeal(currentScore):
    if currentScore > 11:
        if currentScore > 19:
            return 0  # 点数大于19点或已爆牌必定不要牌
        prob = probDict[currentScore]  # 获取要牌概率
        if prob > random.uniform(0, 1):  # 使用投骰子的方式根据概率判断
            return 1
        else:
            return 0
    else:
        return 1  # 点数不大于11必定要牌


# 当前得分
def getScore(cardsList):
    scoreNum = 0
    for i in range(len(cardsList)):
        if cardsList[i][0] == 'A':
            scoreNum += 1
        elif (cardsList[i][0] == '0' or cardsList[i][0] == 'K' or
              cardsList[i][0] == 'Q' or cardsList[i][0] == 'J'):
            scoreNum += 10
        else:
            scoreNum += int(cardsList[i][0])
    return scoreNum


# 分牌函数
def deal(playerCardsList, cardsList, num=1):
    for i in range(num):
        playerCardsList.append(cardsList.pop(0))


# 打印卡牌名字
def getCardName(playerCardsList):
    nameStr = ''
    if isinstance(playerCardsList, str) != 1:
        for i in range(len(playerCardsList)):
            nameStr += cardNameDict[playerCardsList[i]]
            if i != len(playerCardsList):
                nameStr += ' '
    else:
        nameStr = cardNameDict[playerCardsList]
    return nameStr


main()
