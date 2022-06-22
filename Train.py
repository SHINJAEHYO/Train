from datetime import datetime

mytrain = [] #Train_search(), Train_myinfor() 두 함수에서 사용하는 변수이므로 전역변수 선언

with open('c:/TrainList.txt', "r", encoding = 'utf8') as f :
    data = f.read().splitlines() #txt파일 내용을 리스트로 받아와
for n in range(len(data)) :      #이중 리스트로 만들기
    i = data[n].split()    
    data[n] = i  

def typeinfor(): #시간, 출발역, 도착역, 열차종류 입력하는 함수
    global wanttime
    global depsta
    global arrsta
    global trainty
    wanttime = input("시간(hh:mm) : ")
    depsta = input("출발역(서울, 영등포, 부산) : ") 
    arrsta = input("도착역(서울, 부산, 광주) : ")
    trainty = input("열차종류(KTX, 새마을호) : ")

def menu() : #메뉴 출력 함수
    print("\n1.빠른시간 기차 검색 및 예매")
    print("2.전체 기차 리스트 출력")
    print("3.나의 예매 현황 출력 및 예매 취소")
    print("4.프로그램 종료")

def Train_search(): #빠른시간 기차 검색 및 예매
    print("빠른시간 기차 검색 및 예매\n")
    times = []
    timegap = []
    check = 0

    while check < 1:
        typeinfor()  
        for i in range(1,21): #txt파일의 정보와 일치하면 while문 종료
            if depsta == data[i][1] and arrsta == data[i][3] and trainty == data[i][4]:
                check = 1
        if check != 1:        
            print("\n해당 정보가 없습니다. 다시 입력해주세요.\n")
  
    for a in range(1, 21): #입력한 출발역, 도착역, 열차종류가 포함된 모든 시간 저장 리스트
        if depsta == data[a][1] and arrsta == data[a][3] and trainty == data[a][4]:
            times.append(data[a][0])

    for b in range(len(times)): #입력한 시간과 위에서 만든 리스트의 시간들과 차이 저장 리스트
        if wanttime >= times[b]:
            timegap.append(str(datetime.strptime(wanttime,"%H:%M") - datetime.strptime(times[b],"%H:%M")))
        if wanttime < times[b]:        
            timegap.append(str(datetime.strptime(times[b],"%H:%M") - datetime.strptime(wanttime,"%H:%M")))
    
    for c in range(len(times)): #가장 차이가 작은 시간을 booktime에 저장
        if wanttime >= times[c]:
            if str(datetime.strptime(wanttime,"%H:%M") - datetime.strptime(times[c],"%H:%M")) == min(timegap):
                booktime = times[c]
        if wanttime < times[c]:        
            if str(datetime.strptime(times[c],"%H:%M") - datetime.strptime(wanttime,"%H:%M")) == min(timegap):
                booktime = times[c]

    for d in range(1, 21): #booktime과 같은 시간을 가지며 입력받은 조건과 같은 기차표 정보를 booktrain에 저장
        if booktime == data[d][0] and depsta == data[d][1] and arrsta == data[d][3] and trainty == data[d][4]:
            booktrain = data[d]

    print("\n가장 가까운 시간의 열차정보입니다.\n")        
    print(booktrain[0], booktrain[1],"->", booktrain[3], booktrain[4], booktrain[5])

    if booktrain[5] != '매진': #매진일 경우 전좌석 매진 알림 아닐 경우 예매 여부 확인
        YN = int(input("\n예매하시겠습니까?(Yes = 1, No = 0) : "))
    else:
        print("\n전좌석 매진되었습니다.")
        return    

    if YN == 1:
        mytrain.append(booktrain) #나의 예매 현황 리스트에 추가
        for e in range(1, 21): 
            if data[e][0] == booktrain[0] and data[e][1] == booktrain[1] and data[e][3] == booktrain[3] and data[e][4] == booktrain[4]:
                if int(booktrain[5]) - 1 == 0:
                    data[e][5] = "매진"
                else:
                    data[e][5] = int(data[e][5]) - 1
        print("예매 완료 되었습니다.\n")         

           

def Train_print(): #전체 기차 리스트 출력
    for i in range(1,21):
        print(i,"(", data[i][0], data[i][1],"->", data[i][3], data[i][4], data[i][5],")")

def Train_myinfor(): #나의 예매 현황 출력 및 예매 취소
    checknum = 0

    if mytrain == []:
        print("예매내역이 없습니다.")
    else:
        for i in range(len(mytrain)): #mytrain리스트에 저장된 요소 출력
            print(i + 1,"(", mytrain[i][0], mytrain[i][1],"->", mytrain[i][3], mytrain[i][4],")") 

        num = int(input("\n1.예매 취소 / 2. 뒤로 가기 : "))    
        if num == 1:
            delnum = int(input("취소하실 예매내역 번호를 입력하세요. : "))

            while checknum < 1:
                for k in range(1,len(mytrain)+1): #k는 1부터 mytrain에 저장된 리스트 개수 범위 내의 숫자
                    if delnum == k:               #delnum이 위 범위 내에 존재하지 않으면 번호 재입력 무한반복
                        checknum = 1
                if checknum != 1:
                    delnum = int(input("번호를 재입력하세요. : "))
            
            for a in range(1, 21): 
                if data[a][0] == mytrain[delnum-1][0] and data[a][1] == mytrain[delnum-1][1] and data[a][3] == mytrain[delnum-1][3] and data[a][4] == mytrain[delnum-1][4]:
                    if data[a][5] == '매진': #매진일 시 좌석수 1로 초기화
                        data[a][5] = 1
                    else: #매진이 아니면 좌석수 1증가
                        data[a][5] = int(data[a][5]) + 1                
            del mytrain[delnum-1]
            print("예매 취소 되었습니다.")

      

while(1):
    menu()
    num = int(input("\n수행할 기능의 번호를 입력하세요 : "))
    
    if num == 1 :
        Train_search()
    elif num == 2 :
        Train_print()
    elif num == 3 :
        Train_myinfor()
    elif num == 4 :
        exit()
    else:
        print("다시 입력하세요.")
