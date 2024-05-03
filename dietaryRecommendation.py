import math
# **輸入 Input**

# 1. 提示使用者輸入**「性別、年齡、身高（公分）、體重（公斤）、體脂率（百分比）、活動因子、壓力因子」**。

# **輸出 Output**

# 1. 根據使用者輸入的資料，計算並顯示以下結果：
#     - BMI
#     - 除脂體重
#     - 體重狀態（是否超重）
#     - 基礎代謝率（BMR）
#     - 總熱量消耗（TDEE）
#     - 低碳飲食法三大營養素的建議克數

# 檢查數字


class InputNotPositiveIntergerException(Exception):
    pass


def checkNumber(text):
    try:
        number = float(text)
    except ValueError:
        raise InputNotPositiveIntergerException("請輸入合規數字")

    if number <= 0:
        raise InputNotPositiveIntergerException("輸入數字不得小於等於零")

    return number


# 檢查性別是否輸入為中文
class NonChineseException(Exception):
    pass


def checkChinese(text):
    if text not in ['男', '女']:
        raise NonChineseException("輸入的文字必須是中文生理性別")


# BMI的輸入
def bmi(weight, height, bodyFatPer):
    try:

        if weight == 0:
            print('體重不該為零')
        else:
            meterHeight = height/100.0
            bmi = weight/meterHeight**2
            weightWithOutFat = weight * (100-bodyFatPer)/100.0
            print('您的BMI為 : ', round(bmi, 2))
            print('您的除脂體重為 : ', weightWithOutFat)
            if bmi < 18.5:
                print('您的體重狀態為 : 體重過輕')
            elif 18.5 <= bmi < 24:
                print('您的體重狀態為 : 正常')
            elif 24 <= bmi < 27:
                print('您的體重狀態為 : 過重')
            elif 27 <= bmi < 30:
                print('您的體重狀態為 : 輕度肥胖')
            elif 30 <= bmi < 35:
                print('您的體重狀態為 : 中度肥胖')
            else:
                print('您的體重狀態為 : 重度肥胖')
        print('您的體脂率為 : ', bodyFatPer, '%')
    except ZeroDivisionError:
        print("身高不能為零。")


# bmr計算
def bmr(gender, age, weight, height):
    if gender == '男':
        bmr = 66 + (13.7*weight+5*height-6.8*age)
        print('您的基礎代謝率為 : ', round(bmr, 2))
    else:
        bmr = 665 + (9.6*weight+1.8*height-4.7*age)
        print('您的基礎代謝率為 : ', round(bmr, 2))
    return bmr


# tdde計算
def tdee(bmr, pressFactor, activeFactor):
    tdee = pressFactor * bmr * activeFactor
    print('您的總熱量消耗為 : ', round(tdee, 2))
    return tdee


# 低碳飲食計算
def lowCarbonDietNutrition(tdee):
    print('\n您的低碳飲食法三大營養素建議克數為 : ')
    print('碳水化合物 : ', math.floor(tdee * 0.2 / 4))
    print('蛋白質 : ', math.ceil(tdee * 0.3 / 4))
    print('脂肪 : ', math.ceil(tdee * 0.5 / 5))


try:
    gender = input('請輸入性別(男/女) : ')
    checkChinese(gender)

    bodyInfoAsk = dict(age="請輸入年齡 : ", weight="請輸入體重(公斤) : ",
                       height="請輸入身高(公分) : ", bodyFatPer="請輸入體脂率(百分比) : ",
                       activeFactor="請輸入活動因子 : ", pressFactor="請輸入壓力因子 : ")
    bodyInfo = {}

    for key, value in bodyInfoAsk.items():
        inputInfo = checkNumber(input(value))
        bodyInfo[key] = inputInfo

    print('\n#-----您的健康飲食推薦報告-----#\n')

    bmi(bodyInfo['weight'], bodyInfo['height'], bodyInfo['bodyFatPer'])
    bmr = bmr(gender, bodyInfo['age'], bodyInfo['weight'], bodyInfo['height'])
    tdee = tdee(bmr, bodyInfo['pressFactor'], bodyInfo['activeFactor'])
    lowCarbonDietNutrition(tdee)

except InputNotPositiveIntergerException as e:
    print(f'錯誤 : {e}')
except NonChineseException as e1:
    print(f'錯誤 : {e1}')
